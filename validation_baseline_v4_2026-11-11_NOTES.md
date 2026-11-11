# Validation baseline, 2026-11-11

Physics: Matthew Ford's Mode Matrix method (*Reinventing the Wheel*, PhD thesis, Northwestern University, 2018; `bike-wheel-calc`, MIT).

**Default rim changed since the June baseline.** The 2026-06-11 and 2026-08-20 files use the old placeholder rim (EI_lat 50 / EI_rad 150 / GJ 22 N·m², EA 11.5 MN), which was labelled "DT Swiss TK540" but was not its measured values. This file uses the **DT Swiss TK540 as measured by Ford** (lateral 260 / radial 211 / torsional 75 N·m², EA 7.2 MN from its 550 g mass), now the widget default (widget2 #21, wheel-physics-core #24). **Differences from June are expected.** See the comparison below.

File: [`validation_baseline_v4_2026-11-11.csv`](./validation_baseline_v4_2026-11-11.csv). Same first 29 columns as the June file, plus `lib_/wid_F_lat_kgf` and `lib_/wid_F_rad_kgf` at the end (strength figures; the June file predates them). Diff by column name.

## At a glance

| | |
|---|---|
| What was checked | The engine in `index.html` (`<script id="engine">`) vs Ford's unmodified `bike-wheel-calc`, 30 catalogue hubs |
| Build | ERD 600 mm, 32 spokes, 2.0 mm, 100 kgf DS, 24 modes (the June build) |
| Result | **30 / 30 PASS**, worst difference 1.6 × 10⁻¹⁰ % (in the CSV's `max_abs_diff_pct`; core's own T_c tolerance is 1e-7 % because Ford's function uses scipy `eig`) |
| Reference code | `bike-wheel-calc` at core's pinned submodule commit 6fc380c, built with `wheel-physics-core/validation/reference.py`'s helpers (K_lat/K_rad smeared as in the June file; T_c = discrete-spoke `calc_buckling_tension_modematrix`; F_lat/F_rad = first spoke slack from Ford's `ModeMatrix`, as in core `validation/`) |
| Layout | Follows wheel-physics-core `validation/README.md` (core #26) |
| Limit | Agreement shows the port reproduces Ford's code on the same inputs. It does not check the inputs (rim, spokes, hub dimensions); wheel-physics-core's `validation/input-check-2026-11-10/` traces those. |

## What changed versus June, and why

Stiffness (K_lat, K_rad: load per unit deflection) and strength (T_c, F_lat, F_rad: load at which something gives out) are reported separately; a stiffer wheel is not automatically a stronger one.

Three causes, separated by re-running today's engine on the old rim:

1. **Rim: TK540 measured values (the large effect).** Onyx 148 as example: with the old rim today's engine gives K_lat 74.1 N/mm, K_rad 4731 N/mm, identical to June's, so the stiffness code did not change. Moving to the TK540 gives K_lat 125.3 (+69%) and K_rad 5123 (+8%).
2. **Buckling tension method.** June's `T_c` was the smeared-spoke linear approximation. Since the October 2026 switch the engine uses Ford's discrete-spoke buckling (core #13), which is 4–11% lower: Onyx 148 on the old rim, 154.1 → 142.8 kgf (−7%). Then the TK540 takes it to 299.3 kgf. The T_c column therefore mixes the method change and the rim change.
3. **Hub geometry and names.** Hub names were revised (the CSV `case_id`s differ; rows matched by hub order). Project 321 G3 157 drive-side flange offset corrected 26.0 → 26.5 mm (tension ratio 81.63 → 83.18%); it is the only geometry change among the 20 June hubs. Ten hubs are new since June (OneUp, KOM Xeno, DMR Zone, DT Swiss 350, e*thirteen Sidekick, each in 148 and 157).

Summary over the 20 June hubs (same build):

- **K_lat (lateral stiffness):** median +67%, range +63% to +83% (largest for Project 321 G3, which also had the geometry fix). 
- **K_rad (radial stiffness):** +8.3% for every hub.
- **T_c (buckling tension, strength-side):** median +99%, range +91% to +107%.
- **Tension ratio (NDS/DS %):** unchanged (depends only on hub and spoke geometry), except Project 321 G3 157.
- **First spoke slack, new columns (all 30 hubs, TK540):** F_lat median 38.3 kgf (30.4 to 46.0), F_rad median 176 kgf (153 to 211). No June values exist. On the old rim the median F_lat was 22.5 kgf and F_rad 180 kgf, so the rim raises lateral strength a lot and radial strength hardly at all. Radial strength of this build is governed by spoke tension, not rim stiffness.
- **Margin to buckling:** at 100 kgf DS the median T/T_c falls from 54% (old rim) to 26% (TK540).

Full per-hub table (June → now):

| Hub (June name → now) | K_lat N/mm | K_rad N/mm | T_c kgf | ratio % |
|---|---|---|---|---|
| Onyx 148 MFU → Onyx MFU 148x12 | 74.1 → 125.3 (+69%) | 4731 → 5123 (+8%) | 154.1 → 299.3 (+94%) | 62.40 → 62.40 |
| SPANK HEX J-TYPE BOOST R148 → Spank Hex J-Type 148x12 | 78.4 → 132.6 (+69%) | 4739 → 5132 (+8%) | 160.6 → 319.1 (+99%) | 68.04 → 68.04 |
| CK 148x12 CENTERLOCK REAR → CK Centerlock 148x12 | 74.4 → 126.7 (+70%) | 4738 → 5131 (+8%) | 155.6 → 305.6 (+96%) | 66.38 → 66.38 |
| project 321 G3 148x12 → Project 321 G3 148x12 | 57.9 → 104.1 (+80%) | 4750 → 5143 (+8%) | 137.6 → 263.0 (+91%) | 69.14 → 69.14 |
| Hydra Mountain 6 Bolt Rear 148 → I9 Hydra Mountain 6-Bolt 148x12 | 81.6 → 136.7 (+68%) | 4735 → 5127 (+8%) | 163.8 → 325.7 (+99%) | 66.15 → 66.15 |
| I9 Hydra Centerlock Rear 148 → I9 Hydra Centerlock 148x12 | 82.6 → 137.4 (+66%) | 4730 → 5122 (+8%) | 164.0 → 323.4 (+97%) | 62.20 → 62.20 |
| I9 1/1 Mountain 6 Bolt 148 → I9 1/1 Mountain 6-Bolt 148x12 | 75.6 → 127.4 (+69%) | 4740 → 5133 (+8%) | 155.9 → 303.9 (+95%) | 62.51 → 62.51 |
| Hope Pro5 148 6 bolt → Hope Pro5 6-Bolt 148x12 | 68.4 → 117.8 (+72%) | 4743 → 5137 (+8%) | 148.3 → 286.9 (+94%) | 64.89 → 64.89 |
| Erase MTB IS 148x12 V2 j-bend → Erase MTB IS V2 148x12 | 80.6 → 135.5 (+68%) | 4729 → 5121 (+8%) | 162.8 → 323.1 (+98%) | 66.28 → 66.28 |
| Hadley 148x12 → Hadley 148x12 | 75.2 → 126.8 (+69%) | 4736 → 5129 (+8%) | 155.3 → 302.4 (+95%) | 62.23 → 62.23 |
| Onyx 150/157 → Onyx 157x12 | 95.2 → 156.5 (+64%) | 4715 → 5105 (+8%) | 180.4 → 366.3 (+103%) | 66.58 → 66.58 |
| Onyx 150/157 Vesper → Onyx Vesper 157x12 | 93.7 → 154.1 (+64%) | 4711 → 5101 (+8%) | 178.3 → 360.4 (+102%) | 65.76 → 65.76 |
| SPANK HEX J-TYPE R150/157 → Spank Hex J-Type 157x12 | 93.6 → 156.0 (+67%) | 4726 → 5118 (+8%) | 180.9 → 373.1 (+106%) | 75.18 → 75.18 |
| CK 157 SB CENTERLOCK REAR → CK Centerlock 157x12 | 94.8 → 157.0 (+66%) | 4722 → 5114 (+8%) | 181.4 → 372.3 (+105%) | 71.77 → 71.77 |
| project 321 G3 157 SB → Project 321 G3 157x12 | 63.0 → 115.6 (+83%) | 4744 → 5137 (+8%) | 146.7 → 293.1 (+100%) | 81.63 → 83.18 |
| I9 Hydra 6 Bolt 150/157 → I9 Hydra 6-Bolt 157x12 | 97.7 → 160.9 (+65%) | 4722 → 5114 (+8%) | 184.7 → 380.3 (+106%) | 71.13 → 71.13 |
| I9 Hydra Centerlock 157 SB → I9 Hydra Centerlock 157x12 | 101.8 → 165.8 (+63%) | 4715 → 5105 (+8%) | 188.4 → 385.7 (+105%) | 65.85 → 65.85 |
| Hope Pro5 157 SB 6 bolt → Hope Pro5 6-Bolt 157x12 | 89.7 → 148.8 (+66%) | 4727 → 5119 (+8%) | 174.2 → 352.7 (+102%) | 68.56 → 68.56 |
| Erase MTB IS 157x12 v2 j-bend → Erase MTB IS V2 157x12 | 102.5 → 167.7 (+64%) | 4712 → 5103 (+8%) | 190.4 → 393.5 (+107%) | 69.97 → 69.97 |
| Hadley 150/157 → Hadley 157x12 | 97.0 → 159.0 (+64%) | 4723 → 5115 (+8%) | 182.7 → 372.2 (+104%) | 66.61 → 66.61 |

K_lat: median +67.1%, range +62.8% to +83.3%

K_rad: median +8.3%, range +8.3% to +8.3%

T_c: median +99.3%, range +91.1% to +106.6%
