#!/usr/bin/env python3
"""python3 tools/compare-baselines.py <old.csv> <new.csv>  -> markdown table of changes, by hub (matched by row order for
the first 20 rows = the June hub list, then by id-free name for any remaining). Prints K (stiffness) and T_c / F (strength) separately."""
import csv, sys, statistics as st
old = list(csv.DictReader(open(sys.argv[1]))); new = list(csv.DictReader(open(sys.argv[2])))
# June rows are in the widget's hub order: 10x 148 then 10x 157; new file lists 15x 148 then 15x 157
o148 = [r for r in old if r["axle_standard"] == "148"]; o157 = [r for r in old if r["axle_standard"] == "157"]
n148 = [r for r in new if r["axle_standard"] == "148"]; n157 = [r for r in new if r["axle_standard"] == "157"]
ids148 = [0,1,2,3,4,5,6,7,8,9]; ids157 = [0,1,2,3,4,5,6,7,8,9]
pairs = list(zip(o148, n148[:10])) + list(zip(o157, n157[:10]))
f = lambda r, k: float(r[k])
print("| Hub (June name → now) | K_lat N/mm | K_rad N/mm | T_c kgf | ratio % |"); print("|---|---|---|---|---|")
dk, dr, dt = [], [], []
for o, n in pairs:
    a = [(f(o,"wid_K_lat_Nmm"), f(n,"wid_K_lat_Nmm")), (f(o,"wid_K_rad_Nmm"), f(n,"wid_K_rad_Nmm")), (f(o,"wid_T_c_kgf"), f(n,"wid_T_c_kgf"))]
    dk.append(a[0][1]/a[0][0]-1); dr.append(a[1][1]/a[1][0]-1); dt.append(a[2][1]/a[2][0]-1)
    print(f"| {o['case_id']} → {n['case_id']} | {a[0][0]:.1f} → {a[0][1]:.1f} ({dk[-1]*100:+.0f}%) | {a[1][0]:.0f} → {a[1][1]:.0f} ({dr[-1]*100:+.0f}%) | {a[2][0]:.1f} → {a[2][1]:.1f} ({dt[-1]*100:+.0f}%) | {f(o,'wid_ratio_pct'):.2f} → {f(n,'wid_ratio_pct'):.2f} |")
for nm, v in (("K_lat", dk), ("K_rad", dr), ("T_c", dt)):
    print(f"\n{nm}: median {st.median(v)*100:+.1f}%, range {min(v)*100:+.1f}% to {max(v)*100:+.1f}%")
