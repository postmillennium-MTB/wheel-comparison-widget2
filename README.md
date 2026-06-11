# Rear Wheel Comparison: 148 vs 157 — v2

**Interactive browser widget comparing 148 mm (Boost) and 157 mm (Super Boost) rear axle standards using Mode Matrix structural analysis.**

Live widget: [postmillennium-mtb.github.io/wheel-comparison-widget2](https://postmillennium-mtb.github.io/wheel-comparison-widget2)

---

## What this tool does

This widget lets you select a real hub from each axle standard, choose wheel size and spoke gauge, and see how the two builds compare across four structural metrics: lateral stiffness, lateral strength, radial strength, and buckling margin. All four are computed from the geometry you enter — not looked up from a table.

The intended audience is two groups who often want the same answer for different reasons: wheel builders and bike engineers who want to check the math, and riders trying to understand whether the 157 standard offers a meaningful structural advantage for their specific hub and build.

---

## Theory and source code

### The Ford (2018) Mode Matrix method

The physics engine is a direct JavaScript port of **Matt Ford's open-source `bike-wheel-calc` library**, available at [github.com/dashdotrobot/bike-wheel-calc](https://github.com/dashdotrobot/bike-wheel-calc).

Ford's method treats the bicycle wheel as a curved beam (the rim) supported by an elastic foundation (the spoke bed). Deflection under an arbitrary load is solved by expanding the response into Fourier modes — mathematically, a sum over "shapes" the rim can deform into — and computing how stiff the wheel is against each shape. The total compliance at any point is the sum of compliances across all modes. The more modes included, the more accurate the result; the widget defaults to N = 24, at which point the answer has converged to better than 0.1%.

The core reference is:

> Ford, M.T. (2018). *A Theoretical Analysis of the Bicycle Wheel.* PhD thesis, Northwestern University. Available via: [github.com/dashdotrobot/bike-wheel-calc](https://github.com/dashdotrobot/bike-wheel-calc)

### Exact library functions reproduced

The four computed metrics correspond to specific functions in the Ford library:

| Widget metric | Library function | Key settings |
|---|---|---|
| Tension ratio NDS/DS | `BicycleWheel.apply_tension(T_right=T_DS)` | Equilibrium balance |
| Lateral stiffness K_lat | `theory.calc_lat_stiff()` | N=24, smeared spokes, tension softening, no radial coupling, r0=False |
| Radial stiffness K_rad | `theory.calc_rad_stiff()` | Same settings |
| Critical buckling tension T_c | `theory.calc_buckling_tension()` | Linear approximation, N=24 |

"Smeared spokes" (the Smith–Pippard approximation) replaces the discrete spoke pattern with a continuous elastic foundation of equivalent stiffness, which is the standard approach for the Mode Matrix method. The widget does not currently support fully-discrete spoke calculations.

### Model assumptions and their implications

Every analytical model makes simplifying assumptions. The ones that matter most for this widget are listed here explicitly, with their practical consequences.

**Rim centroid radius.** Spoke geometry is computed from the rim's structural centroid, which sits approximately 11 mm radially inward from the spoke nipple seat (ERD/2). Ford §3.2 derives this from rim cross-section geometry. Using ERD/2 directly instead would introduce a ~3–4% error in spoke length that propagates through every stiffness and strength calculation. This 11 mm value is fixed for all rims in the widget; users with significantly different rim profiles may wish to note this.

**Smeared spokes.** The continuous spoke foundation is accurate when the number of spokes is large enough that the circumferential spacing is small relative to the rim's characteristic deformation length — satisfied for typical 28–36 spoke wheels.

**No spoke offset.** The model assumes the spoke nipple sits at the rim's shear center (b = 0). For most double-wall MTB rims, the offset is small and its effect on overall stiffness is negligible.

**No warping stiffness.** The rim's warping constant I_warp is set to zero, consistent with the library's default for thin-walled closed sections where warping is suppressed.

**No shear center offset (y0 = 0).** The rim is treated as having its shear center at the centroid. For symmetric rims this is exact; for C-channel profiles it introduces a small error.

**3-cross lacing, fixed.** Lacing pattern is not currently a user parameter. The crossing angle is computed as (2π / (Ns/2)) × 3 for both sides.

**Steel spokes, E = 210 GPa.** Titanium or carbon spokes would require a different Young's modulus. The widget does not support non-steel spokes.

---

## What each metric means

### Tension balance (NDS/DS ratio)

The most fundamental constraint on a dished rear wheel. Because the rim sits closer to the non-drive-side (NDS) flange on a cassette hub, the NDS spokes run at a steeper lateral angle. To keep the rim centered axially, the NDS spokes must therefore carry less tension than the drive-side (DS) spokes — the ratio is set by geometry alone, not by the builder.

**How it is calculated.** The widget applies the tension equilibrium condition from Ford §2.3: axial force balance requires T_NDS / T_DS = sin(α_DS) / sin(α_NDS), where α is the lateral angle of each spoke. This is identical to `BicycleWheel.apply_tension(T_right=T_DS)` in the library, and it agrees with the library to floating-point precision.

**What the number means.** A ratio of 66% means the NDS spokes carry 66 kgf for every 100 kgf on the DS. Wider axles (157 vs 148) push the flanges further apart and typically improve the ratio, because the NDS offset increases relative to the DS offset. Larger flange diameters can raise it further.

**Editorial note on thresholds.** The widget displays the ratio without a pass/fail line. Dished MTB rear wheels in this dataset land between 62–82% under standard conditions. The often-cited "80% target" appears in wheel building guides as a quality aspiration, not a structural requirement from Ford's analysis, and most production Boost hubs do not reach it. Labeling builds below 80% as "failing" would flag the majority of wheels in common use; this widget instead lets the numbers speak.

### Lateral stiffness K_lat (N/mm)

How hard it is to push the rim sideways at the contact patch with a unit force. Higher is stiffer. Under the Mode Matrix method, the value accounts for both the rim's resistance to bending and torsion and the spoke bed's resistance to lateral displacement. The tension-softening effect — whereby pre-tension in the spokes actually reduces lateral stiffness slightly via hoop compression — is included.

Across the 20 hubs in this dataset at standard build conditions (29 in, 32H, 2.0 mm spokes, 100 kgf DS tension, DT Swiss TK540 rim), K_lat ranges from **57.9 to 82.6 N/mm for 148** builds and **63.0 to 102.5 N/mm for 157** builds. The variation within each standard is as large as the difference between standards — meaning hub geometry and wheel size matter as much as the axle width.

### Lateral strength F_lat (kgf)

The sideways load at the rim contact patch at which the first spoke on the low-tension side reaches zero pre-tension. This is the onset of spoke slack, not wheel collapse. Beyond this point, the slack spoke can no longer resist rim motion; repeated loading in this regime leads to fatigue and eventual wheel failure.

**This is not a library output.** The Ford library computes stiffnesses and buckling loads; it does not define a "lateral strength" in this sense. The formula used here is:

```
u_slack = T_side × L_side / (EA_side × |n_u,side|)
F_lat   = K_lat × min(u_slack_DS, u_slack_NDS)
```

Where `u_slack` is the lateral rim deflection that bleeds off all pre-tension in the governing spoke, and the governing side (almost always NDS) is reported on the widget. This is a first-order linear approximation. The actual load at which a spoke first goes slack in a real wheel may differ due to spoke bedding, nipple friction, and local load concentration. Use this as a relative comparison between the two builds, not as an absolute failure prediction.

### Radial strength F_rad (kgf)

The downward load at the contact patch at which the first spoke on the bottom of the wheel reaches zero pre-tension. Computed by the same linearized approach as F_lat, using the radial direction cosines and the radial stiffness K_rad.

### Buckling tension T_c (kgf)

The spoke tension at which the rim becomes elastically unstable — it would buckle laterally ("taco") rather than simply deflect. Ford §5 derives this from the mode at which the lateral stiffness matrix becomes singular. The widget uses the linear approximation (`calc_buckling_tension(approx='linear')`).

The table shows two representations of T_c:

- **T_c avg** — the critical average radial spoke tension, which is the quantity directly computed by the Ford method. This is the natural output of the library.
- **T_c as DS** — the equivalent DS tension at the buckling point, derived by scaling: T_c(DS) = T_c(avg) × (T_DS / T_avg). This is the number a builder can compare to their tensiometer.

**The "Used" column** is current average tension ÷ T_c avg, expressed as a percentage. The ✓ / ! / ✕ thresholds (below 70% / 70–85% / above 85%) are this widget's editorial choice for a comfort margin. They are not thresholds defined in Ford's analysis. The critical buckling tension is always a theoretical maximum under idealized conditions; real wheels should be built well below it.

---

## Hub geometry data

### Source and confidence

Hub flange dimensions — center-to-flange offsets (DS and NDS) and flange pitch circle diameters — are compiled from **manufacturer documentation and published specifications**. All values are in millimeters.

No measurements in this dataset were taken with calipers by the widget author. Hub geometry is inherently difficult to measure and varies slightly between production batches. If you have caliper measurements from a specific hub and they differ from the values here, the measured values should be considered more reliable. The widget accepts any geometry values via the advanced panel if you want to compare directly.

**Known correction (v2).** The Hope Pro5 150/157 geometry in v1 of this widget was incorrect (nds = 28.0 mm, sourced in error). The corrected value (nds = 39.6 mm) is used in v2. This correction substantially changes the results for this hub: with the wrong geometry, the 148 version appeared stiffer than the 157, which created an interesting counter-narrative; with the correct geometry, the 157 is stiffer as expected from physics. The v1 repo and its validation artifacts should not be used as reference.

### Hub catalogue (standard build conditions: 29 in, 32H, 2.0 mm, 100 kgf DS, DT Swiss TK540 rim defaults)

| Hub | Std | NDS/DS ratio | K_lat (N/mm) | K_rad (N/mm) | T_c avg (kgf) | Baseline |
|---|---|---|---|---|---|---|
| Onyx 148 MFU | 148 | 62.4% | 74.1 | 4731 | 154.1 | PASS |
| SPANK HEX J-TYPE BOOST R148 | 148 | 68.0% | 78.4 | 4739 | 160.6 | PASS |
| CK 148x12 CENTERLOCK REAR | 148 | 66.4% | 74.4 | 4738 | 155.6 | PASS |
| project 321 G3 148x12 | 148 | 69.1% | 57.9 | 4750 | 137.6 | PASS |
| Hydra Mountain 6 Bolt Rear 148 | 148 | 66.1% | 81.6 | 4735 | 163.8 | PASS |
| I9 Hydra Centerlock Rear 148 | 148 | 62.2% | 82.6 | 4730 | 164.0 | PASS |
| I9 1/1 Mountain 6 Bolt 148 | 148 | 62.5% | 75.6 | 4740 | 155.9 | PASS |
| Hope Pro5 148 6 bolt | 148 | 64.9% | 68.4 | 4743 | 148.3 | PASS |
| Erase MTB IS 148x12 V2 j-bend | 148 | 66.3% | 80.6 | 4729 | 162.8 | PASS |
| Hadley 148x12 | 148 | 62.2% | 75.2 | 4736 | 155.3 | PASS |
| Onyx 150/157 | 157 | 66.6% | 95.2 | 4715 | 180.4 | PASS |
| Onyx 150/157 Vesper | 157 | 65.8% | 93.7 | 4711 | 178.3 | PASS |
| SPANK HEX J-TYPE R150/157 | 157 | 75.2% | 93.6 | 4726 | 180.9 | PASS |
| CK 157 SB CENTERLOCK REAR | 157 | 71.8% | 94.8 | 4722 | 181.4 | PASS |
| project 321 G3 157 SB | 157 | 81.6% | 63.0 | 4744 | 146.7 | PASS |
| I9 Hydra 6 Bolt 150/157 | 157 | 71.1% | 97.7 | 4722 | 184.7 | PASS |
| I9 Hydra Centerlock 157 SB | 157 | 65.9% | 101.8 | 4715 | 188.4 | PASS |
| Hope Pro5 157 SB 6 bolt | 157 | 68.6% | 89.7 | 4727 | 174.2 | PASS |
| Erase MTB IS 157x12 v2 j-bend | 157 | 70.0% | 102.5 | 4712 | 190.4 | PASS |
| Hadley 150/157 | 157 | 66.6% | 97.0 | 4723 | 182.7 | PASS |

"PASS" means the widget value matched the `bike-wheel-calc` Python library to < 10⁻¹² % (floating-point noise).

### Notable results worth examining

**project 321 G3 148 vs 157.** Both versions of this hub use an unusually narrow NDS offset (32 mm) for their respective standards. The 157 version reaches the highest tension ratio in the 157 group (81.6%) but has the lowest lateral stiffness in the 157 group (63.0 N/mm) — because while the ratio is excellent, the narrow NDS offset means the NDS spoke angle is steep and the absolute stiffness contribution is reduced. This is a good illustration of why no single metric tells the full story.

**I9 Hydra Centerlock 157 SB.** The highest lateral stiffness in the dataset (101.8 N/mm) and one of the highest buckling margins (188.4 kgf), owing to a notably wide NDS offset (43 mm) that gives the NDS spokes excellent lateral bracing geometry.

**Axle standard is not the only driver.** The 148 range (57.9–82.6 N/mm) and 157 range (63.0–102.5 N/mm) overlap. A well-specified 148 build with a high-quality hub and large-flanged hubs can outperform a poorly specified 157 build. What the 157 standard enables is a structural ceiling that is simply not available at 148 mm — the best 157 hubs reach about 25% higher lateral stiffness than the best 148 hubs in this dataset.

---

## Rim defaults (DT Swiss TK540)

The widget's default rim properties are derived from acoustic modal testing literature for the DT Swiss TK540, a widely used alloy double-wall MTB rim:

| Parameter | Symbol | Default | Range for alloy double-wall |
|---|---|---|---|
| Lateral bending stiffness | EI_lat | 50 N·m² | 40–80 N·m² |
| Radial (in-plane) bending stiffness | EI_rad | 150 N·m² | 100–300 N·m² |
| Torsional stiffness | GJ | 22 N·m² | 15–35 N·m² |
| Axial (hoop) stiffness | EA_rim | 11.5 MN | 8–15 MN |

GJ is the most influential rim parameter for lateral stiffness, not EI_lat, because the rim's curvature couples bending and torsion (Ford §3.4). Changing GJ from its default has a larger effect on K_lat than changing EI_lat by the same proportion. Users experimenting with rim parameters should treat GJ changes as the primary sensitivity.

Both wheels always share the same rim defaults. This is intentional: it isolates the effect of hub geometry and axle width, which is the comparison the widget is designed to make.

---

## Validation

### Approach

The widget's physics engine is a direct JavaScript port of Ford's Python library. To confirm the port is correct, the engine was extracted from the shipped `index.html` and run against the Python library across the full 20-hub catalogue, using the same inputs, and the outputs were compared numerically.

### Results

All 20 hubs passed. Worst-case absolute percentage difference across all hubs and all four metrics: **1.13 × 10⁻¹³ %** — well below any meaningful threshold, and consistent with floating-point arithmetic operating on identical formulas.

The validation results are stored in [`validation_baseline_v4_2026-06-11.csv`](./validation_baseline_v4_2026-06-11.csv), which contains the side-by-side library and widget outputs for every hub, with the diff column confirming the match.

### What the validation does and does not establish

The validation confirms that the JavaScript engine faithfully reproduces Matt Ford's Python library under the same model assumptions. It does **not** independently validate Ford's model against physical measurements on real wheels — that is the work Ford's thesis itself undertakes, and readers interested in the theoretical foundations and experimental comparisons should consult the original work.

The strength metrics (F_lat, F_rad) are **not** compared against the library, because they are not library outputs. They are transparent, first-principles calculations built on top of the validated stiffnesses. Their formulas are fully documented in the code comments.

### Re-running the validation

If you modify the engine and want to re-run the congruence check, you need Python 3, Node.js, and the `bikewheelcalc` library installed from source:

```bash
git clone https://github.com/dashdotrobot/bike-wheel-calc.git
pip install ./bike-wheel-calc
```

The validation logic is the `congruence.py` script from the v1 repository's validation folder, updated to read hub data from the shipped `index.html` rather than a separate file. The key point is that the script should always extract the engine from the deployed `index.html` — not from a separate copy — so that validation is always testing exactly what users are running.

---

## Differences from v1

| Item | v1 | v2 |
|---|---|---|
| Engine | Rewritten engine (incomplete port); did not match its own validation baseline | Direct port of Ford library; matches to floating-point precision |
| Hub geometry: Hope Pro5 157 | nds = 28.0 mm (incorrect) | nds = 39.6 mm (corrected) |
| Strength model (F_lat) | NDS slack load computed with Ns/2 factor (unconservative by ~16×) | First-spoke-slack threshold on K_lat; formula documented in code |
| Verdict statements | Inverted in the case where 148 wins (named wrong hub as winner) | Fixed; winner always named with positive adjective, verified both directions |
| Mobile layout | Fixed three-column grid, no responsive breakpoints | Mobile-first; stacks to single column below 560 px |
| Colorblindness | Status communicated by red/amber/green only | Okabe–Ito colorblind-safe palette; status always paired with symbol + word |
| Tension ratio threshold | ≥ 80% shown as target, triggering amber/red on most hubs | No pass/fail line; displayed with context note on typical real-world range |
| Validation CSV | Dated 2025-05-26; produced by a different version of the engine than was deployed | Generated from the shipped `index.html` on 2026-06-11; always current |

---

## What this widget does not do

**It does not model real-world loading.** A rim load in service is not a single point force at the contact patch — it is distributed, dynamic, and varies with terrain, rider weight, and speed. First-spoke-slack is a meaningful structural threshold, but it is not the same as a fatigue limit or a field failure prediction.

**It does not account for spoke fatigue.** Spokes fail in fatigue at the nipple or J-bend, at loads well below their tensile strength. The model does not include any fatigue life prediction.

**It does not model rim asymmetry or offset drilling.** Some rims use offset spoke holes (e.g., DT Swiss asymmetric rims) to improve the tension balance. The model treats the rim as symmetric; the asymmetry's effect on spoke geometry would need to be folded into the hub offset values manually.

**It does not compare weight, bearing quality, engagement, or cost.** Those are real decision factors in hub selection that are completely outside the scope of this tool.

---

## Files in this repository

| File | Description |
|---|---|
| `index.html` | The complete widget — all HTML, CSS, and JavaScript in a single file. The physics engine is in the `<script id="engine">` tag. |
| `validation_baseline_v4_2026-06-11.csv` | Congruence test results: widget vs `bike-wheel-calc` library, all 20 hubs, four metrics each. All rows PASS. |
| `README.md` | This document. |

---

## License and attribution

The physics engine is a port of Matt Ford's `bike-wheel-calc`, which is licensed under the MIT License. The original library and its documentation are available at [github.com/dashdotrobot/bike-wheel-calc](https://github.com/dashdotrobot/bike-wheel-calc).

Widget UI, hub data compilation, strength metric formulas, and this README: © PostMillennium MTB / RedFoxRun, 2026.

---

## Contact and corrections

Hub geometry corrections, methodology questions, or requests to add hubs: open an issue in this repository or reach out via Pinkbike.

If you have caliper measurements for a hub already in the catalogue and they differ from the values listed, please open an issue with the source of the values (manufacturer drawing, personal measurement, etc.) — corrections with documented sources are prioritized.
