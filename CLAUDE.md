# CLAUDE.md

Guidance for Claude Code sessions working in this repository (the 148 vs 157
wheel comparison widget, a single-file `index.html` served live from `main`).

The wheel-strength math comes from Matthew Ford's Mode Matrix method via
`wheel-physics-core`; credit him whenever this tool's numbers are used.

## Working rules

- **Merging to `main` publishes.** The live page at
  postmillenniumrenaissance.com/wheel-comparison-widget2/ serves this repo's
  `main`, so work on a branch and merge only with Jon's go.
- **The engine is a copy.** `<script id="engine">` in `index.html` is a copy
  of wheel-physics-core's `js/engine.js` (currently from commit `1e81384`).
  Change the math there, validate it there, then re-sync the copy; never edit
  the physics here first. `js/build-link.js` is pasted in the same way.
  `tools/check-core-sync.mjs` (CI: `core-sync.yml`, also weekly) fails when
  either copy no longer matches the core's main branch; after a re-sync,
  update the commit named here and in the README.
- **Stiffness and strength are different words.** Stiffness (`K_lat`,
  `K_rad`) is load per unit deflection; strength (`F_lat`, `F_rad`) is the
  load at which the first spoke goes slack. Never use one for the other in
  card text, chart labels or docs.
- **Cite Ford's thesis by its title page:** Ford, M.T. (2018), *Reinventing
  the Wheel: Stress Analysis, Stability, and Optimization of the Bicycle
  Wheel*, PhD thesis, Northwestern University.
- **README numbers come from the engine.** When quoting a hub's K_lat,
  F_lat or balance in `README.md`, take it from the catalogue table's
  conditions (or say which conditions) and re-run it, rather than copying
  an older figure.

## Color accessibility (colorblind-safe)

Every color scheme and theme must stay readable for colorblind viewers
(about 1 in 12 men, mostly red-green). This covers charts, graphs, diagrams,
text and fonts, icons, badges, buttons and sliders, in every theme, not just
the default one.

- **Check with numbers, not by eye.** Any two colors that must be told apart
  in the same view (two series, the two hubs, a hub vs a failure line, status
  colors) need an OKLab ΔE×100 of at least **15 for normal vision** and at
  least **8 under simulated deuteranopia, protanopia and tritanopia**. Check
  every theme against that theme's own background, e.g. with the `dataviz`
  skill's `scripts/validate_palette.js` (`--pairs all` when everything is on
  screen at once) or any OKLab + color-vision-simulation tool.
- **One color, one meaning per view.** A color that marks a hub or series is
  never reused for something else (a failure line, a status) in the same chart.
- **Never color alone.** Pair color with a second cue: a text label, line
  style (solid / dashed / dotted), marker shape, icon, or position. Charts with
  two or more series keep a legend or direct labels.
- **Watch the risky pairs:** red/green, red/orange, pink/teal, blue/purple and
  cyan/light blue are easy to confuse when their lightness is similar. A clear
  lightness difference between the two is the most reliable fix.
- **Text contrast (WCAG 2.x):** normal text at least 4.5:1 against its
  background; large text (24px+, or 18.7px+ bold) and chart lines, marks and
  icons at least 3:1. Colored text, such as a value printed in its series
  color, counts too.
- **Text over lines or fills** gets a halo or backing box in the background
  color (SVG: `stroke` = background, `paint-order: stroke`) so it is never
  struck through.
- **Fix with the smallest change that keeps the existing look:** adjust one
  color's shade, or add a line style or label. Don't restyle a chart to fix a
  color problem unless Jon asks for a redesign.
- **When adding or changing a theme or palette,** re-run the check for every
  pair in that theme and put the results (pairs and ΔE values) in the PR
  description.
