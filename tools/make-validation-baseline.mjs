// Dumps the widget's own engine (index.html <script id="engine">) run on every
// catalogue hub, as JSON on stdout. Input for tools/make_validation_baseline.py,
// which computes the matching Ford (bike-wheel-calc) values and writes the CSV.
//
//   node tools/make-validation-baseline.mjs > engine_out.json
//
// Matthew Ford's Mode Matrix method (bike-wheel-calc, MIT) is the physics.
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(here, "..", "index.html"), "utf8");
const block = id => html.match(new RegExp(`<script id="${id}"[^>]*>([\\s\\S]*?)</script>`))[1];
const module = { exports: {} };
vm.runInNewContext(block("engine"), { module, exports: module.exports, Math, Number, Infinity, NaN, Array, Object, Float64Array, Map, Set, console });
const { calc } = module.exports;

// Hub catalogue and rim defaults exactly as shipped in index.html
const ctx = {};
const catSrc = html.match(/const HUBS_148 = \[[\s\S]*?\];\s*const HUBS_157 = \[[\s\S]*?\];/)[0];
vm.runInNewContext(catSrc + "; out = {HUBS_148, HUBS_157};", ctx);
const rim = vm.runInNewContext("(" + html.match(/const RIM_DEFAULTS = (\{[^}]*\})/)[1] + ")");
const out = { rim, hubs: [] };
for (const [std, list] of [["148", ctx.out.HUBS_148], ["157", ctx.out.HUBS_157]])
  for (const h of list) {
    const r = calc(600, h, 2.0, 2.0, 100, rim.eil, rim.eir, rim.gj, rim.ea * 1e6, 32, 24);
    out.hubs.push({ id: h.id, std, name: h.name, ds: h.ds, nds: h.nds, pds: h.pds, pnds: h.pnds, r });
  }
console.log(JSON.stringify(out));
