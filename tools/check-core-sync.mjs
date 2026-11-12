// Checks that this widget's pasted copies of wheel-physics-core still match it.
//
//   node tools/check-core-sync.mjs <path to a wheel-physics-core checkout>
//
// 1. Engine (<script id="engine">): the widget's copy and the core's current
//    js/engine.js are both run on every hub in the core's validation catalogue
//    at a spread of builds. Every number the widget's copy returns must match
//    the core's to 1e-9 (relative). The core may add outputs the widget does
//    not use; those are ignored. A change to an output the widget does use
//    fails this check until the copy is re-synced.
// 2. Build links (<script id="build-link">): must be the core's
//    js/build-link.js, character for character.
// 3. "Copy result" wording (<script id="share-text">): must be the core's
//    js/share-text.js, character for character. Skipped, with a note, while
//    the core's main branch does not have that file yet (the widget's copy
//    arrived alongside the core change that adds it).
//
// The physics is Matthew Ford's Mode Matrix method (bike-wheel-calc, MIT);
// wheel-physics-core checks its engine against his library, this script only
// checks that the widget's copy is the same engine.
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const core = process.argv[2];
if (!core) {
  console.error("usage: node tools/check-core-sync.mjs <wheel-physics-core checkout>");
  process.exit(2);
}
const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(here, "..", "index.html"), "utf8");

function block(id) {
  const m = html.match(new RegExp(`<script id="${id}"[^>]*>([\\s\\S]*?)</script>`));
  if (!m) throw new Error(`index.html has no <script id="${id}">`);
  return m[1];
}
function load(src, name) {
  const module = { exports: {} };
  vm.runInNewContext(src, { module, exports: module.exports, Math, Number, Infinity, NaN, Array, Object, Float64Array, Map, Set, console }, { filename: name });
  return module.exports;
}

let failures = 0;

// ── 1. engine ────────────────────────────────────────────────────────────
const widget = load(block("engine"), "index.html#engine");
const coreEng = load(readFileSync(join(core, "js", "engine.js"), "utf8"), "core/js/engine.js");
const cat = JSON.parse(readFileSync(join(core, "validation", "hub_catalogue.json"), "utf8"));
const R = cat.rim_constants;

const builds = [];
for (const erd of [538, 567, 605, 649])
  for (const ns of [28, 32])
    for (const t of [95, 110, 125])
      builds.push({ erd, ns, t, dDS: 2.0, dNDS: 2.0 });
builds.push({ erd: 605, ns: 32, t: 100, dDS: 2.0, dNDS: 1.5 });
builds.push({ erd: 605, ns: 32, t: 100, dDS: 1.8, dNDS: 1.5 });

function close(a, b) {
  if (a === b) return true;
  if (!Number.isFinite(a) || !Number.isFinite(b)) return Object.is(a, b);
  return Math.abs(a - b) <= 1e-9 * Math.max(Math.abs(a), Math.abs(b), 1e-12);
}
function compare(w, c, path, out) {
  if (typeof w === "number") {
    if (typeof c !== "number" || !close(w, c)) out.push(`${path}: widget ${w}, core ${c}`);
  } else if (w && typeof w === "object") {
    if (!c || typeof c !== "object") { out.push(`${path}: missing in core`); return; }
    for (const k of Object.keys(w)) compare(w[k], c[k], path ? `${path}.${k}` : k, out);
  } else if (w !== c) {
    out.push(`${path}: widget ${JSON.stringify(w)}, core ${JSON.stringify(c)}`);
  }
}

let rows = 0;
for (const h of cat.hubs) {
  const hub = { ds: h.ds, nds: h.nds, pds: h.pds, pnds: h.pnds };
  for (const b of builds) {
    const args = [b.erd, hub, b.dDS, b.dNDS, b.t, R.EIL, R.EIR, R.GJ, R.EA_rim, b.ns, R.modes];
    const diffs = [];
    compare(widget.calc(...args), coreEng.calc(...args), "", diffs);
    rows++;
    if (diffs.length) {
      failures++;
      if (failures <= 10) console.error(`DRIFT ${h.name} ERD ${b.erd} ${b.ns}H ${b.t} kgf ${b.dDS}/${b.dNDS} mm:\n  ${diffs.slice(0, 5).join("\n  ")}`);
    }
  }
}
console.log(`engine: ${rows} builds (${cat.hubs.length} hubs x ${builds.length}), ${failures} with differences`);

// ── 2. build links ───────────────────────────────────────────────────────
const linkOk = block("build-link").trim() === readFileSync(join(core, "js", "build-link.js"), "utf8").trim();
console.log(`build-link: ${linkOk ? "identical to" : "DIFFERS from"} core js/build-link.js`);

// ── 3. share text ────────────────────────────────────────────────────────
const shareCore = join(core, "js", "share-text.js");
let shareOk = true;
if (existsSync(shareCore)) {
  shareOk = block("share-text").trim() === readFileSync(shareCore, "utf8").trim();
  console.log(`share-text: ${shareOk ? "identical to" : "DIFFERS from"} core js/share-text.js`);
} else {
  console.log("share-text: core has no js/share-text.js yet; check skipped");
}

if (failures || !linkOk || !shareOk) {
  console.error("\nThe widget's copy no longer matches wheel-physics-core. Re-sync the <script> block(s) from the core (see README, \"Where this widget's copy of the engine comes from\").");
  process.exit(1);
}
console.log("PASS: the widget's engine, build-link and share-text copies match wheel-physics-core.");
