# PRD: Compact mode redesign

**Date:** 2026-10-09
**Feature:** 001-compact-mode-redesign

## Problem

Compact (Simplified) mode is what a phone visitor sees first, and it makes the tool's one job hard. The answer ("the 157 build is 28% more laterally strong than the 148 wheel") is below the first screen because the wheel drawing comes first. The sentence names both hubs in full, in 800-weight 30px type, so it runs to five lines and reads as a wall of bold. Choosing the two hubs takes two modes: tap the 148x12 tab, pick a hub, tap the 157x12 tab, pick a second hub, with the other hub hidden while you work. The figure carries a "to first slack spoke" caption that most readers cannot use. Four hub names repeat across the card.

## Users & Context

Readers of the Pinkbike and Post Millennium Renaissance articles, mostly on a phone, who want to know how much stronger one rear hub makes a wheel than another and who are not wheelbuilders. The widget is a single `index.html` served from GitHub Pages and embedded by iframe. Simplified mode opens by default below 700px wide and is a toggle at any width. It shares state with the full view, which stays unchanged. The physics engine is a synced copy of `wheel-physics-core` and is not edited here. Both colour themes (DMC-12, MGB) must keep working.

## Goals

- Both hubs are visible and changeable at the same time, in two fixed rows, with no tab to press first.
- The result is stated as one plain sentence: "157x12 is 28% stronger than 148x12", the stronger side first, with the percentage as the only large type and no mid-sentence bold.
- The result is on the first screen of a phone (393×852) without scrolling.
- "to first slack spoke" no longer appears in compact mode. "Lateral strength" stays as the label so "stronger" is not an unqualified claim.
- Each hub's strength is shown as a bar and a figure on one shared scale, next to its picker.
- The phone header is slimmer (one row of buttons at 393px) and picker text is 16px so mobile browsers do not zoom on focus.
- The axle standard appears as "148x12" and "157x12" only. The "Boost axle" and "Super Boost axle" nicknames are not shown in compact mode.
- The README's description of compact mode is updated to match.

## Non-Goals

- No change to the physics engine or to any computed figure.
- No change to the full (non-compact) view, or to the shared URL format.
- No new compact-mode controls (wheel size, tension, spokes, rim stay in the full view).
- No short or renamed hub names, and no change to the hub data.
- No "weaker" wording anywhere in compact mode.

## Success Criteria

- At 393×852 the whole result sentence is on screen with no scrolling.
- Changing either hub updates its bar, its figure and the sentence with no other tap, and the wheel turns to the hub just changed.
- With a 148 hub and a 157 hub selected the sentence reads exactly "157x12 / is N% stronger / than 148x12" (or the reverse order when the 148 hub is stronger). With two hubs of the same standard it names the two hubs instead. Equal hubs, a gap under 1%, and a past-buckling build each give the existing meaning in the new layout.
- The strings "first slack", "Boost axle" and "Super Boost axle" do not appear on the compact screen.
- No horizontal scroll at 360, 393 and 1100px wide. Picker text is at least 16px and each picker is at least 44px tall.
- A screen reader announces the percentage as "N percent".
- The full view, the shared-link round trip (`sm=` included), and the MGB theme render and behave as before.
- Compact mode in MGB is checked by eye, since the rows and bars use the shared theme tokens.

## Architecture Decisions

- [Two fixed hub rows and a stronger-first sentence](../../adr/001-compact-comparison-model.md) — both hubs always visible in fixed slot order, the sentence read-only, stronger side first, "stronger" never "weaker", named by axle standard (hub names when both sides share a standard).

Smaller choices stay inline here rather than getting their own record: the wheel is kept (one wheel that morphs, driven by a small "Wheel shows" switch and by the hub just changed); the order on a phone is pickers, answer, wheel; the credit and "full breakdown" link move below the wheel; the percent sign stays the existing icon with an off-screen "percent" for screen readers.

## Out of Scope

- Giving MGB the same panel-contrast treatment as DMC-12.
- A third "Night Drive" theme.
- Auto-flipping the wheel between hubs on a timer.
- Per-hub short names, or showing bracing angle as anything other than the one small line under the answer.
