# ADR-001-compact-comparison-model: Two fixed hub rows and a stronger-first sentence

**Status:** Proposed
**Date:** 2026-10-09
**Feature:** 001-compact-mode-redesign

## Context

Compact (Simplified) mode shows one wheel, one hub picker and a result sentence. To compare two hubs the reader taps the "148x12" tab, picks a hub, taps the "157x12" tab and picks a second hub, so the second hub is hidden until its tab is open and the picker means two different things depending on the tab. The result sentence names both hubs in full, in 800-weight type at 30px, and runs to five lines on a phone.

Constraints from the PRD: both hubs visible and changeable at once; the answer must read as "X is N% stronger than Y"; it must be visible on a phone's first screen; either row must still be able to hold either axle standard (148 vs 148 and 157 vs 157 are supported); the physics engine is not touched; shared links, including `sm=`, must keep working.

One property of the metric bears directly on wording: the gap is asymmetric. 25.9 kgf against 20.3 kgf is 28% stronger measured from the weaker hub, and 22% weaker measured from the stronger one. Both are true, and a reader shown both words will carry the wrong figure away.

## Options Considered

### Option A: Keep the tab-bound single picker, restyle only

**Pros:** smallest change; no new state.
**Cons:** does not address the two-step flow, which is the main usability complaint; the second hub stays hidden.

### Option B: Two always-visible pickers in fixed slot order; the sentence leads with the stronger side and is named by axle standard

Each row is amber (first slot) or blue (second slot) and holds a hub picker, its standard label, and a bar and kgf figure on one shared scale. The sentence is read-only and sits directly under the rows.

**Pros:** both hubs are on screen and editable at once with no mode; rows keep their position, so nothing moves under the thumb while choosing; the sentence can always lead with the stronger side and use "stronger", never "weaker"; naming sides by standard keeps the sentence to a few words (the rows above tie each standard to a hub).
**Cons:** names the standards, not the hubs, so the sentence alone does not say which hubs were compared (the rows do); when both sides hold the same standard the standard names nothing and the sentence must fall back to hub names, which is longer.

### Option C: The sentence is the control (each name in "X is N% stronger than Y" is a dropdown)

**Pros:** answer and input are one object; very few elements.
**Cons:** the sentence must lead with the stronger hub, so the two dropdowns would swap places whenever a new pick crosses the other hub's strength, moving the control the reader just used. Holding the order fixed instead forces "weaker" wording about half the time (the asymmetry above). Long hub names also make a tappable chip awkward on a phone.

## Decision

**We chose Option B** because the PRD's first goal is that both hubs are visible and changeable at once with no tab to press first, and only B does that without letting the sentence's direction move the controls. The sentence keeps the rule the current one already follows (it leads with the stronger build) and adds that it never says "weaker", for the asymmetry reason in Context. That meets the PRD's requirement of a literal "X is N% stronger than Y" statement directly.

## Consequences

- The wheel is no longer the way in. A small "Wheel shows" switch under it flips between the two rows, and changing a hub points the wheel at that row.
- `sm=` keeps the meaning it has in the code today: `sm=148` is the first (amber) row and `sm=157` the second (blue) row. The numbers are the historical names of the two slots, not the axle standards they currently hold, so with 148 vs 148 selected `sm=157` still means the second row. With the default pair the two readings coincide, which is why the README describes it as a standard; that sentence is corrected when this ships. `sm=1` and `#simple` are unchanged.
- Prose names a side by its axle standard ("157x12"), and by hub name when both sides hold the same standard.
- The word "weaker" is not used in compact mode.
- Revisit if a third hub is ever compared (the fixed two-row structure and the single stronger-versus-weaker sentence assume exactly two), or if the metric changes to one without the asymmetry.
