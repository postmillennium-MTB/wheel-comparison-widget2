#!/usr/bin/env python3
"""Writes a dated validation baseline CSV for the widget, in the column layout of
validation_baseline_v4_2026-06-11.csv (extra F_lat / F_rad columns appended at the
end so older files still diff by column name).

  node tools/make-validation-baseline.mjs > engine_out.json
  python3 tools/make_validation_baseline.py engine_out.json <wheel-physics-core checkout> <out.csv> <date>

wid_* = the widget's own engine (index.html <script id="engine">), run at the
widget's shipped rim defaults. lib_* = Matthew Ford's bike-wheel-calc (MIT, the
core's pinned submodule), unmodified, built with the same helpers as
wheel-physics-core/validation/reference.py. Build: ERD 600, 32 spokes, 2.0 mm,
100 kgf DS, 24 modes -- the June 2026 baseline's build.
Stiffness (K_lat, K_rad) and strength (F_lat, F_rad, T_c) are separate columns.
"""
import csv, json, sys
from pathlib import Path
import numpy as np

eng_json, core, out_csv, date = sys.argv[1:5]
core = Path(core).resolve()
sys.path.insert(0, str(core / "validation"))
sys.path.insert(0, str(core / "third-party/dashdotrobot/bike-wheel-calc"))
from reference import build_wheel, first_slack, N_MODES  # core's own builder
from bikewheelcalc.theory import calc_lat_stiff, calc_rad_stiff, calc_buckling_tension_modematrix
from bikewheelcalc.mode_matrix import ModeMatrix

d = json.load(open(eng_json))
rim = d["rim"]
RC = {"EIL": rim["eil"], "EIR": rim["eir"], "GJ": rim["gj"], "EA_rim": rim["ea"] * 1e6}
cat_rc = json.load(open(core / "validation/hub_catalogue.json"))["rim_constants"]
assert all(abs(cat_rc[k] - RC[k]) < 1e-9 for k in RC), ("core fixture rim differs", cat_rc, RC)

# June 2026 baseline row order -> widget hub ids (names were revised since)
JUNE = ["h1","h5","h6","h8","h10","h12","h14","h15","h17","h20","h2","h3","h4","h7","h9","h11","h13","h16","h18","h19"]
june = {r["case_id"]: r for r in csv.DictReader(open(sys.argv[5]))} if len(sys.argv) > 5 else {}
june_rows = list(june.values())
june_by_id = dict(zip(JUNE, june_rows))

def pd(a, b):
    return 0.0 if a == b else 100.0 * abs(a - b) / max(abs(a), abs(b))

cols = ["widget_version","generated","case_id","hub_name","axle_standard","erd_mm","tDS_kgf","spk_mm","Ns","N",
        "EIL_Nm2","EIR_Nm2","GJ_Nm2","EA_rim_MN","hub_ds_mm","hub_nds_mm","hub_pds_mm","hub_pnds_mm",
        "lib_ratio_pct","wid_ratio_pct","lib_K_lat_Nmm","wid_K_lat_Nmm","lib_K_rad_Nmm","wid_K_rad_Nmm",
        "lib_T_c_kgf","wid_T_c_kgf","max_abs_diff_pct","pass_fail","notes",
        "lib_F_lat_kgf","wid_F_lat_kgf","lib_F_rad_kgf","wid_F_rad_kgf"]
NOTE = ("engine from shipped index.html (script#engine, node vm); reference = unmodified dashdotrobot/bike-wheel-calc "
        "(submodule 6fc380c via wheel-physics-core, built with validation/reference.py helpers); "
        "default rim = Ford-measured DT Swiss TK540 (EI_lat 260 / EI_rad 211 / GJ 75 N.m2, EA 7.2 MN), NOT the June 50/150/22/11.5; "
        "T_c = discrete-spoke buckling; F_lat/F_rad = first spoke slack, discrete spokes (both new since June)")
rows = []
for h in d["hubs"]:
    hub = {"ds": h["ds"], "nds": h["nds"], "pds": h["pds"], "pnds": h["pnds"], "std": h["std"], "name": h["name"]}
    w = build_wheel(hub, RC, 600.0, 32, 100.0)
    t_ds = max(w.spokes[0].tension, w.spokes[1].tension); t_nds = min(w.spokes[0].tension, w.spokes[1].tension)
    kw = dict(N=N_MODES, smeared_spokes=True, tension=True, buckling=True, coupling=False, r0=False)
    lib = {"ratio": 100 * t_nds / t_ds,
           "K_lat": calc_lat_stiff(w, **kw) / 1000, "K_rad": calc_rad_stiff(w, **kw) / 1000,
           "T_c": calc_buckling_tension_modematrix(w, smeared_spokes=False, coupling=True, r0=False, N=N_MODES) / 9.81}
    mm = ModeMatrix(w, N=N_MODES)
    K = mm.K_rim(tension=True, r0=False) + mm.K_spk(tension=True, smeared_spokes=False)
    lib["F_lat"] = first_slack(w, mm, K, 0) / 9.81; lib["F_rad"] = first_slack(w, mm, K, 1) / 9.81
    r = h["r"]
    wid = {"ratio": r["ratio"], "K_lat": r["K_lat"], "K_rad": r["K_rad"], "T_c": r["T_c"], "F_lat": r["F_lat"], "F_rad": r["F_rad"]}
    mx = max(pd(lib[k], wid[k]) for k in lib)
    j = june_by_id.get(h["id"])
    note = NOTE + ("" if j else "; hub added since June baseline")
    if j and (float(j["hub_ds_mm"]), float(j["hub_nds_mm"])) != (h["ds"], h["nds"]):
        note += f"; geometry changed since June (ds {j['hub_ds_mm']}->{h['ds']} mm)"
    rows.append({"widget_version": "v4", "generated": date, "case_id": h["name"], "hub_name": h["name"], "axle_standard": h["std"],
        "erd_mm": 600, "tDS_kgf": 100, "spk_mm": 2.0, "Ns": 32, "N": 24, "EIL_Nm2": rim["eil"], "EIR_Nm2": rim["eir"],
        "GJ_Nm2": rim["gj"], "EA_rim_MN": rim["ea"], "hub_ds_mm": h["ds"], "hub_nds_mm": h["nds"], "hub_pds_mm": h["pds"], "hub_pnds_mm": h["pnds"],
        "lib_ratio_pct": f"{lib['ratio']:.6f}", "wid_ratio_pct": f"{wid['ratio']:.6f}",
        "lib_K_lat_Nmm": f"{lib['K_lat']:.6f}", "wid_K_lat_Nmm": f"{wid['K_lat']:.6f}",
        "lib_K_rad_Nmm": f"{lib['K_rad']:.6f}", "wid_K_rad_Nmm": f"{wid['K_rad']:.6f}",
        "lib_T_c_kgf": f"{lib['T_c']:.6f}", "wid_T_c_kgf": f"{wid['T_c']:.6f}",
        "max_abs_diff_pct": f"{mx:.2e}", "pass_fail": "PASS" if mx < 1e-6 else "FAIL", "notes": note,
        "lib_F_lat_kgf": f"{lib['F_lat']:.6f}", "wid_F_lat_kgf": f"{wid['F_lat']:.6f}",
        "lib_F_rad_kgf": f"{lib['F_rad']:.6f}", "wid_F_rad_kgf": f"{wid['F_rad']:.6f}"})
with open(out_csv, "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=cols); wr.writeheader(); wr.writerows(rows)
print(len(rows), "rows;", sum(r["pass_fail"] == "PASS" for r in rows), "PASS; worst", max(float(r["max_abs_diff_pct"]) for r in rows))
