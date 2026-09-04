# Rear Wheel Comparison: 148 vs 157 — v2

**Interactive browser widget comparing 148 mm (Boost) and 157 mm (Super Boost) rear axle standards using Mode Matrix structural analysis.**

Live widget: [postmillennium-mtb.github.io/wheel-comparison-widget2](https://postmillennium-mtb.github.io/wheel-comparison-widget2)

---

## What this tool does

This widget lets you select a real hub from each axle standard, choose wheel size and spoke gauge, and see how the two builds compare across four structural metrics: lateral stiffness, lateral strength, radial strength, and buckling margin. All four are computed from the geometry you enter — not looked up from a table.

The result the widget is built around — lateral strength, F_lat — is surfaced as a single headline verdict at the top of the comparison column ("157x12 wheel wins," followed by the percentage), with the raw kgf for both builds shown underneath it. Every other metric lives in the cards below, available but deliberately secondary; the point of the tool is that one number, and the layout says so.

A **"Compare two at random"** button sits above the headline. It rolls one wheel size (25% chance each, applied to both sides so the size itself isn't a variable) and one hub per side from the full catalogue, resetting everything else — spoke gauge, spoke count, tension, rim properties — to default first, so the roll is always an apples-to-apples comparison of hub geometry alone.

The intended audience is two groups who often want the same answer for different reasons: wheel builders and bike engineers who want to check the math, and riders trying to understand whether the 157 standard offers a meaningful structural advantage for their specific hub and build.

---

## Interface

**Headline verdict.** The card at the top of the comparison column is the tool's focal point: which axle standard wins on lateral strength, by how much, and the two raw kgf values it's built from. Its color tracks whichever side won (amber for 148, blue for 157), and it restates the exact wheel size, spoke count, and DS tension it was computed under, so a screenshot of just that card is self-explanatory without the rest of the page.

**Card headers.** Each side's config card leads with the numeric axle standard ("148x12" / "157x12") set large and centered, with the marketing nickname ("Boost axle" / "Super Boost axle") in smaller type beneath it. The nickname carries a hover tooltip with its trademark trivia — "Boost is a marketing nickname from Trek, circa 2014/2015" and "Super Boost is a marketing nickname from Pivot, circa 2016" — so the jargon stays in the UI but is explained on demand rather than assumed.

**Compare two at random.** Rerolls if it happens to land on the exact setup already on screen. The resulting comparison updates the shareable link like any manual change, so an interesting random pairing can be copied and sent as-is.

**Secondary cards.** Radial strength, lateral stiffness, and tension balance are expanded by default. **Buckling margin is collapsed by default** — it's the metric readers reach for least often, so it starts out of the way and opens on tap.

**Shareable link.** "Copy link" packs every current setting — both hubs, wheel sizes, spoke gauges, and any advanced rim/tension overrides — into the URL hash, so a copied link reproduces the exact comparison for whoever opens it.

**DS tension is set per side, not shared.** It used to be one control for both wheels. That broke once wheel size became independently selectable per side (26–32"): buckling tension drops as a wheel gets larger, so one shared absolute tension was a different fraction of "how close to buckling" on each side whenever the two sizes differed — silently making the larger wheel look stronger or weaker depending on where that shared value happened to fall on its curve, for reasons that had nothing to do with the hubs being compared. Each side now defaults to 120 kgf, or 100 kgf at 32" specifically — a size where 120 kgf pushes most of this catalogue close enough to its own modeled buckling limit that the comparison stops being about hub geometry — and can be moved independently. Changing a side's wheel size updates its tension to that size's default automatically, unless you've set that side's tension by hand, in which case your choice is kept.

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

**Straight-gauge spokes only.** Each spoke's diameter is constant along its full length. Real butted spokes (e.g. 2.0–1.5–2.0) have thicker ends than their nominal middle gauge, giving them higher effective axial stiffness than a straight-gauge spoke of the same nominal diameter. This mainly affects F_lat at thin gauges — see the caution under "Lateral strength F_lat" below.

---

## What each metric means

### Tension balance (NDS/DS ratio)

The most fundamental constraint on a dished rear wheel. Because the rim sits closer to the non-drive-side (NDS) flange on a cassette hub, the NDS spokes run at a steeper lateral angle. To keep the rim centered axially, the NDS spokes must therefore carry less tension than the drive-side (DS) spokes — the ratio is set by geometry alone, not by the builder.

**How it is calculated.** The widget applies the tension equilibrium condition from Ford §2.3: axial force balance requires T_NDS / T_DS = sin(α_DS) / sin(α_NDS), where α is the lateral angle of each spoke. This is identical to `BicycleWheel.apply_tension(T_right=T_DS)` in the library, and it agrees with the library to floating-point precision.

**What the number means.** A ratio of 66% means the NDS spokes carry 66 kgf for every 100 kgf on the DS. Wider axles (157 vs 148) push the flanges further apart and typically improve the ratio, because the NDS offset increases relative to the DS offset. Larger flange diameters can raise it further.

**Editorial note on thresholds.** The widget displays the ratio without a pass/fail line. Dished MTB rear wheels in this dataset land between 61–96% under standard conditions, though that top figure needs context: the only entries above 82% are hubs that are barely dished to begin with (the Hope Pro5 150 converted to 157, at 95.8%), not well-balanced versions of conventional ones. The often-cited "80% target" appears in wheel building guides as a quality aspiration, not a structural requirement from Ford's analysis, and most production Boost hubs do not reach it. Labeling builds below 80% as "failing" would flag the majority of wheels in common use; this widget instead lets the numbers speak.

### Lateral stiffness K_lat (N/mm)

How hard it is to push the rim sideways at the contact patch with a unit force. Higher is stiffer. Under the Mode Matrix method, the value accounts for both the rim's resistance to bending and torsion and the spoke bed's resistance to lateral displacement. The tension-softening effect — whereby pre-tension in the spokes actually reduces lateral stiffness slightly via hoop compression — is included.

Across the 25 hubs in this dataset at standard build conditions (29 in, 32H, 2.0 mm spokes, 100 kgf DS tension, DT Swiss TK540 rim), K_lat ranges from **53.6 to 82.6 N/mm for 148** builds and **50.8 to 102.5 N/mm for 157** builds. The variation within each standard is as large as the difference between standards — meaning hub geometry and wheel size matter as much as the axle width.

### Lateral strength F_lat (kgf)

The sideways load at the rim contact patch at which the first spoke on the low-tension side reaches zero pre-tension. This is the onset of spoke slack, not wheel collapse. Beyond this point, the slack spoke can no longer resist rim motion; repeated loading in this regime leads to fatigue and eventual wheel failure.

**This is not a library output.** The Ford library computes stiffnesses and buckling loads; it does not define a "lateral strength" in this sense. The formula used here is:

```
u_slack = T_side × L_side / (EA_side × |n_u,side|)
F_lat   = K_lat × min(u_slack_DS, u_slack_NDS)
```

Where `u_slack` is the lateral rim deflection that bleeds off all pre-tension in the governing spoke, and the governing side (almost always NDS) is reported on the widget. This is a first-order linear approximation. The actual load at which a spoke first goes slack in a real wheel may differ due to spoke bedding, nipple friction, and local load concentration. Use this as a relative comparison between the two builds, not as an absolute failure prediction.

**Caution: thinning the governing spoke's gauge always raises F_lat, with no ceiling.** Because `u_slack` scales with `1 / EA_side` and cross-sectional area falls as the square of diameter, thinning the governing spoke (almost always NDS) increases F_lat at an *accelerating* rate — each 0.1 mm step buys more than the last. Taken to its limit the formula implies an infinitely thin spoke gives an infinitely strong wheel, which is obviously not physical. Two things are actually happening when you do this in the widget:

- **The tradeoff is real but lives in a different card.** A thinner, stretchier NDS spoke genuinely does stay tensioned through more deflection — this is the real-world reason NDS-side bladed or butted spokes are common on dished rear wheels. But it comes at the cost of lateral stiffness (K_lat), which drops steadily as gauge thins. F_lat only tells half the story; check K_lat alongside it before reading a thin-NDS build as an unqualified win.
- **The model has no term that bounds the gain.** F_lat has no yield criterion, no fatigue term, and assumes straight-gauge spokes rather than the butted (e.g. 2.0–1.5–2.0) spokes typically paired with thin NDS gauges — a butted spoke's thicker ends raise its effective axial stiffness above straight-gauge 1.5 mm, so the widget likely overstates the F_lat gain at thin gauges, more so the thinner you go. Spoke tensile stress also isn't modeled; at fixed tension, thinning the spoke raises its stress roughly as `1/d²`.

In short: F_lat correctly ranks two builds at a fixed spoke gauge, but it should not be used to justify going to unrealistically thin NDS spokes in isolation. Cross-check against K_lat, and treat straight-gauge results at 1.5–1.6 mm as an upper-bound estimate rather than a build recommendation.

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

### Primary source documents

Manufacturer documents the entries in this catalogue were read from directly. Links are to the manufacturers' own files, not to mirrors or third-party spoke-calculator databases.

| Source | Covers | Link |
|---|---|---|
| KOM, *2023v8.0 Hub Spoke Offset, Pitch Circle Diameter and Spoke Seat Offset for KOM Xeno Hubs* | Both KOM Xeno entries | [PDF](https://a57737a1-faee-44f3-9d3e-369eef96078a.filesusr.com/ugd/f3b2d6_b44b975756194f24bea35c5b5da6b68a.pdf?index=true) |
| Hope Technology, *Pro5 PCD — J-Bend, 2025* | Both Hope Pro5 entries, and the 2026-09 correction below | [PDF](https://www.hopetech.com/webtop/modules/_repository/1/documents/Pro5_PCD_J_Bend_2025.pdf) |
| OneUp Components, rear hub product pages | OneUp 148 entry / OneUp 157 entry | [148x12](https://www.oneupcomponents.com/products/rear-hub) · [157x12](https://www.oneupcomponents.com/products/rear-hub-157x12) |

The KOM link is a direct file URL from KOM's site and carries a generated filename, so it is the kind of link that rots; the document is identified above by its full title and version (2023v8.0) so it stays findable if the URL moves. Entries predating this table were compiled from manufacturer specifications without the source file being recorded at the time — a gap worth closing as those hubs are next revisited.

No measurements in this dataset were taken with calipers by the widget author. Hub geometry is inherently difficult to measure and varies slightly between production batches. If you have caliper measurements from a specific hub and they differ from the values here, the measured values should be considered more reliable. The widget accepts any geometry values via the advanced panel if you want to compare directly.

**Addition (2026-09), KOM.** The two KOM Xeno rear hubs were taken from KOM's own technical document *"2023v8.0 Hub Spoke Offset, Pitch Circle Diameter and Spoke Seat Offset for KOM Xeno Hubs"* ([PDF](https://a57737a1-faee-44f3-9d3e-369eef96078a.filesusr.com/ugd/f3b2d6_b44b975756194f24bea35c5b5da6b68a.pdf?index=true)), which lists "Spoke PCD Left & Right", "Flange Offset Left" and "Flange Offset Right" per model. Left maps to the non-drive side and right to the drive side; the document's own front-hub rows confirm that reading, since they place the left flange *closer* to centre (23.5 mm vs 34.0 mm), which is only correct if left is the disc side. KOM publishes identical geometry for the 28-hole and 32-hole versions of each model, so one catalogue entry covers both — spoke count is a separate control in the widget and is not baked into the hub entry.

**These two hubs are straight-pull.** KOM states that every Xeno version uses straight-pull spokes, and the document is explicitly written for straight-pull spoke calculators. Every other hub in this catalogue is J-bend. The model does not distinguish between the two: a spoke is a line from a point on the flange pitch circle to a point on the rim, so the stiffness, tension and buckling figures for the KOM rows are computed on the same basis as every other row and are directly comparable. What the model does not capture is where the two differ in practice — fatigue life at the spoke-hub interface, which is the J-bend elbow's characteristic failure point and does not exist on a straight-pull hub. Read the KOM rows as geometry, not as a verdict on durability.

The same document lists a "Spoke Offset Left & Right" of 0.5 mm, its spoke *seat* offset. This model has no input for it: the Mode Matrix treats each spoke as attaching at a point on the flange pitch circle, so a 0.5 mm lateral offset of the seat from the flange plane is not represented. At that magnitude the effect is far below the batch-to-batch variation in the rest of this dataset, but it is unmodelled rather than accounted for, and is recorded here as such.

**Addition (2026-09), Hope 150 converted to 157.** Hope's PRO5 Rear 150 6 Bolt accepts a normal wide-range cassette and converts to 157x12 with 3.5 mm endcaps per side, so it is listed on the 157 side. Its geometry is entered unchanged from Hope's 150 row (28.0 / 26.8, PCD 57 / 59): symmetric endcaps widen the axle without moving the shell relative to hub centre, and the rim still centres on that same point, so the flange offsets the model needs are the ones Hope publishes for the 150. Nothing about the conversion needs to be recomputed.

What the conversion *does* change is the cassette's position relative to the frame. Symmetric caps leave the cassette where it sat on the 150, so a converted hub does not inherit a native Super Boost chainline, and frame and drivetrain clearance should be checked against the specific bike rather than assumed from the axle width. That is a fitment question, not a structural one, and it sits outside what this widget computes — but it is the reason a converted 150 and a native 157 SB are two different rows here rather than interchangeable ones.

**Addition (2026-09), OneUp.** The two OneUp Components rear hubs were added from OneUp's own published product-page dimensions ([148x12](https://www.oneupcomponents.com/products/rear-hub), [157x12](https://www.oneupcomponents.com/products/rear-hub-157x12)), which are given in spoke-calculator form (PCD-L / Flange Dist-L / PCD-R / Flange Dist-R). Left maps to non-drive side, right to drive side, and "PCD" is the flange pitch circle diameter this dataset calls `pds`/`pnds`. One thing to note when reading these two rows: OneUp's published NDS offset is *smaller* on the 157 (35.0 mm) than on the 148 (38.0 mm), which is the reverse of the pattern in every other hub pair here. That is what the manufacturer publishes and it is recorded unaltered, but it means the OneUp 157's advantage over the OneUp 148 shows up as tension balance (74.3% vs 60.7%) rather than as lateral stiffness, where it is actually the lower of the two. Caliper measurements confirming or contradicting these figures are welcome.

**Known correction (v2).** The Hope Pro5 150/157 geometry in v1 of this widget was incorrect (nds = 28.0 mm, sourced in error). The corrected value (nds = 39.6 mm) is used in v2. This correction substantially changes the results for this hub: with the wrong geometry, the 148 version appeared stiffer than the 157, which created an interesting counter-narrative; with the correct geometry, the 157 is stiffer as expected from physics. The v1 repo and its validation artifacts should not be used as reference.

**Root cause of that correction, identified 2026-09.** Hope's own PCD chart (*Pro5 PCD — J-Bend, 2025*, [PDF](https://www.hopetech.com/webtop/modules/_repository/1/documents/Pro5_PCD_J_Bend_2025.pdf)) shows where the v1 number came from:

| Hope row | PCD NDS / DS | Flange offset NDS / DS |
|---|---|---|
| PRO5 Rear 150 6 Bolt | 57 / 59 | **28.0** / 26.8 |
| PRO5 Rear 157 SB 6 Bolt | 57 / 59 | **39.6** / 27.0 |

The v1 value sat on the *150* row, not the *157 SB* row. Hope ships those as two separate hubs with materially different geometry, and the v1 entry name — "Hope Pro5 150/157" — is what invited the slip. The entry is now named "Hope Pro5 157 SB 6 bolt" for that reason.

**The 150 row is not irrelevant to the 157 side, though — which is the subtler half of this.** Hope's 150 shell converts to 157x12 with 3.5 mm endcaps per side, so it is a real 157x12 option, and it is now in the catalogue in its own right as "Hope Pro5 150 6 bolt (157 conv)". The v1 error was therefore not "used a 150 hub, which has no business here"; it was collapsing two genuinely different 157-capable Hope hubs into one entry and attaching the wrong geometry to the wrong name. Both belong, as separate rows with separate numbers. A catalogue name that merges two axle standards is a latent sourcing bug precisely because the merge hides a real distinction rather than inventing a fake one.

While checking this, the Pro5 **148** entry was verified against the same chart and is correct as stored (35.0 / 22.6, PCD 57 / 59). Its NDS PCD is 57 because this is the 6-bolt version; Hope's *centerlock* Pro5 148 uses 51. Any future Hope addition needs the right disc-interface row, not just the right axle width.

### What is in the catalogue, and what is deliberately not

The catalogue holds rear hubs whose freehub takes a current wide-range MTB cassette — HG, XD or Microspline, 11- or 12-speed. That is the inclusion rule, and it exists so that every pairing the widget can produce is a choice a rider could actually make. A hub that reaches one of the two axle widths through the manufacturer's own endcaps counts as that width, which is why Hope's 150 shell appears on the 157 side; note that the *DH* version of that same shell is excluded below, on the cassette rule, so "Hope 150" is not simply in or out — it depends which driver it carries. Front hubs are out of scope entirely; the tool compares rear axle standards, and the manufacturer documents cited above list front hubs alongside rear ones, so this is worth stating rather than assuming.

**Downhill-driver hubs are excluded on purpose.** Several manufacturers publish a DH version of a rear hub that takes only a 7- or 8-speed downhill cassette. These are not omissions and should not be added:

| Hub | Flange offset NDS / DS | PCD NDS / DS | Tension ratio | K_lat |
|---|---|---|---|---|
| KOM Xeno Rear Downhill 157 | 35.0 / 34.0 | 46.0 / 46.0 | 97.2% | 84.5 |
| Hope PRO5 Rear 150 DH 6 Bolt | 33.0 / 33.0 | 60.0 / 64.0 | 100.2% | 78.3 |
| Hope PRO5 Rear 148 DH 6 Bolt | 28.5 / 28.5 | 60.0 / 64.0 | 100.2% | 55.4 |

Computed at the same standard build conditions as the catalogue table below, from the manufacturer documents already cited. The two Hope rows exceed 100% because their flange offsets are equal while the drive-side PCD is the larger of the two (64 vs 60), which leaves the non-drive spokes at fractionally the shallower angle — a hair past undished, in the direction opposite to every other rear hub here.

Their geometry is genuinely remarkable — a DH driver is short, which frees the drive-side flange to move outboard until the wheel is nearly undished, and the tension balance that follows is far beyond anything else here. That is exactly why they are a trap in this particular tool. Dropped into the same list, they would top the tension-balance column and win random pairings against hubs they are not an alternative to: no one choosing between a 148 and a 157 trail build can run a 7-speed cassette. The comparison would read as a recommendation while describing an unavailable option.

The numbers are recorded here so the research is not lost and nobody re-derives it. If DH builds are ever brought into scope, they belong in their own group with their own baseline, not mixed into this one.

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
| OneUp Rear Hub 148x12 | 148 | 60.7% | 77.9 | 4728 | 158.1 | not yet run |
| KOM Xeno Rear Boost 148x12 | 148 | 77.2% | 53.6 | 4737 | 135.2 | not yet run |
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
| OneUp Rear Hub 157x12 | 157 | 74.3% | 72.1 | 4731 | 155.0 | not yet run |
| KOM Xeno Rear Super Boost 157 | 157 | 80.2% | 74.4 | 4723 | 159.3 | not yet run |
| Hope Pro5 150 6 bolt (157 conv) | 157 | 95.8% | 50.8 | 4750 | 137.6 | not yet run |

"PASS" means the widget value matched the `bike-wheel-calc` Python library to < 10⁻¹² % (floating-point noise).

"not yet run" marks a hub added after the most recent congruence run (2026-08-20). Its figures above were computed with the shipped engine, but that engine has not been re-checked against the Python library *with this hub's geometry in the input set*. The two are not equivalent claims, so the column records the difference rather than glossing it. Since the engine is geometry-independent — the same code path runs for every hub — a passing run on 20 hubs is strong evidence the engine is correct, not proof for a specific untested row. These rows change to PASS at the next congruence re-run.

### Notable results worth examining

**project 321 G3 148 vs 157.** Both versions of this hub use an unusually narrow NDS offset (32 mm) for their respective standards. The 157 version reaches the highest tension ratio of any *conventionally dished* 157 here (81.6%) but among the lowest lateral stiffness in the 157 group (63.0 N/mm) — because while the ratio is excellent, the narrow NDS offset means the NDS spoke angle is steep and the absolute stiffness contribution is reduced. This is a good illustration of why no single metric tells the full story.

**I9 Hydra Centerlock 157 SB.** Among the highest lateral stiffness in the dataset (101.8 N/mm, second only to the Erase MTB IS 157x12 at 102.5) and one of the highest buckling margins (188.4 kgf), owing to a notably wide NDS offset (43 mm) that gives the NDS spokes excellent lateral bracing geometry.

**KOM Xeno Rear Boost 148 — the clearest tension-balance-versus-stiffness trade in the dataset.** This hub posts the best tension balance of any 148 in the catalogue by a wide margin (77.2%, against a 148 median near 65%) and simultaneously the lowest lateral stiffness of any hub here, either standard (53.6 N/mm). Both come from the same two geometry choices: a 46 mm flange PCD, the smallest in the dataset, and a flange spacing of 54 mm that sits the two flanges unusually close together. The small PCD shortens the lever the spokes act on and steepens their angle at the rim, which costs bracing stiffness; the narrow, comparatively even flange spacing is what keeps the two sides' tensions close. A builder reading only the tension-ratio column would rank this hub first among 148s, and a builder reading only the stiffness column would rank it last. Neither column is wrong, and this is the sharpest illustration in the catalogue of why the widget shows four metrics instead of a score.

**Axle standard is not the only driver.** The 148 range (53.6–82.6 N/mm) and 157 range (50.8–102.5 N/mm) overlap, and the 157 range now fully contains the 148 range. A well-specified 148 build with a high-quality hub and large-flanged hubs can outperform a poorly specified 157 build. What the 157 standard enables is a structural ceiling that is simply not available at 148 mm — the best 157 hubs reach about 25% higher lateral stiffness than the best 148 hubs in this dataset.

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

**Re-run, 2026-08-20.** The same congruence check was re-run two months later — `bikewheelcalc` source fetched fresh from GitHub, engine re-extracted from the then-current `index.html` — after several UI-only changes had been made to the widget (card header layout, advanced-settings copy). All 20 hubs still passed at the same floating-point-noise level (worst case **1.13 × 10⁻¹³ %**), confirming the engine had not drifted from the Ford library across those changes. Results are in [`validation_baseline_v4_2026-08-20.csv`](./validation_baseline_v4_2026-08-20.csv); the June file is kept alongside it rather than overwritten, so the history of passing baselines is auditable over time.

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
| `validation_baseline_v4_2026-08-20.csv` | Re-run of the same congruence check, ~2 months later, after UI-only changes. All rows PASS, matching the June baseline to floating-point precision — confirms no engine drift. |
| `README.md` | This document. |

---

## License and attribution

The physics engine is a port of Matt Ford's `bike-wheel-calc`, which is licensed under the MIT License. The original library and its documentation are available at [github.com/dashdotrobot/bike-wheel-calc](https://github.com/dashdotrobot/bike-wheel-calc).

Widget UI, hub data compilation, strength metric formulas, and this README: © PostMillennium MTB / RedFoxRun, 2026.

---

## Contact and corrections

Hub geometry corrections, methodology questions, or requests to add hubs: open an issue in this repository or reach out via Pinkbike.

If you have caliper measurements for a hub already in the catalogue and they differ from the values listed, please open an issue with the source of the values (manufacturer drawing, personal measurement, etc.) — corrections with documented sources are prioritized.
