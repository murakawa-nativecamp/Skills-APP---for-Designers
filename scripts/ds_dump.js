// ds_dump.js — read-only Figma Plugin API script for use_figma
// Purpose: dump the NativeCamp "Design System - APP" registered variables, text styles
//          and Button-family component keys as a single JSON object.
// How to run: the ds-sync workflow reads this file and passes its CONTENTS as the
//   `code` parameter of the Figma MCP `use_figma` tool, with
//   fileKey = "DKl4vZ6OAtXYhuvMHbWkRZ" (the Design System - APP file).
//   The Design System file MUST be open in the Figma desktop app for this to work.
// Output: return value is JSON — save it verbatim to scripts/ds_tokens.json
//   (replacing "generatedAt":"AUTO" with the current ISO timestamp), then run
//   scripts/ds_generate.py to rebuild the skill token blocks.

const WANT_COLLECTIONS = ['Semantic', 'Spacing', 'Radius', 'BorderWidth', 'Layout'];
// Button-family component sets to capture keys for. Icons live in a separate library
// file and are intentionally not enumerated here.
const WANT_COMPONENT_SETS = ['Button', 'Compact Button', 'Icon Button', 'Toggle Button', 'Text Link'];

const cols = await figma.variables.getLocalVariableCollectionsAsync();
const allVars = await figma.variables.getLocalVariablesAsync();
const byId = new Map(allVars.map(v => [v.id, v]));

const toHex = c => {
  if (c == null) return null;
  const f = x => Math.round(x * 255).toString(16).padStart(2, '0');
  let s = '#' + f(c.r) + f(c.g) + f(c.b);
  if (c.a != null && c.a < 0.999) s += f(c.a);
  return s.toUpperCase();
};

async function resolve(val, d) {
  d = d || 0;
  if (d > 10) return null;
  if (val && val.type === 'VARIABLE_ALIAS') {
    let t = byId.get(val.id) || await figma.variables.getVariableByIdAsync(val.id);
    if (!t) return null;
    const mk = Object.keys(t.valuesByMode)[0];
    return await resolve(t.valuesByMode[mk], d + 1);
  }
  if (val && typeof val === 'object' && 'r' in val) return toHex(val);
  if (typeof val === 'number') return val;
  if (typeof val === 'string') return val;
  return null;
}

// --- variables by collection ---
const collections = {};
for (const col of cols) {
  if (!WANT_COLLECTIONS.includes(col.name)) continue;
  const modes = col.modes.map(m => ({ id: m.modeId, name: m.name }));
  const vars = [];
  for (const vid of col.variableIds) {
    const v = byId.get(vid);
    if (!v) continue;
    const value = {};
    for (const m of modes) value[m.name] = await resolve(v.valuesByMode[m.id]);
    vars.push({ name: v.name, key: v.key, type: v.resolvedType, val: value });
  }
  collections[col.name] = { modes: modes.map(m => m.name), vars };
}

// --- text styles ---
const ts = await figma.getLocalTextStylesAsync();
const textStyles = ts.map(s => ({
  name: s.name,
  key: s.key,
  size: s.fontSize,
  family: s.fontName && s.fontName.family,
  weight: s.fontName && s.fontName.style,
  lh: (s.lineHeight && s.lineHeight.unit === 'PERCENT')
    ? Math.round(s.lineHeight.value) + '%'
    : (s.lineHeight && s.lineHeight.value != null ? s.lineHeight.value : 'auto')
}));

// --- component sets ---
// Only scan the DS component pages (named with a leading "・", e.g. "・Button").
// Thumbnail / example / pattern pages contain duplicate sets with the SAME name
// but different (non-canonical) keys, so restrict to the real component pages.
const components = [];
const seen = new Set();
for (const page of figma.root.children) {
  if (!page.name.startsWith('・')) continue;
  await page.loadAsync();
  const sets = page.findAllWithCriteria({ types: ['COMPONENT_SET'] });
  for (const s of sets) {
    if (!WANT_COMPONENT_SETS.includes(s.name) || seen.has(s.name)) continue;
    seen.add(s.name);
    components.push({
      name: s.name,
      type: s.type,
      key: s.key,
      props: s.componentPropertyDefinitions ? Object.keys(s.componentPropertyDefinitions) : []
    });
  }
}

return {
  meta: {
    sourceFileKey: figma.fileKey || 'DKl4vZ6OAtXYhuvMHbWkRZ',
    sourceFileName: 'Design System - APP',
    sourceUrl: 'https://www.figma.com/design/DKl4vZ6OAtXYhuvMHbWkRZ/Design-System---APP',
    generatedAt: 'AUTO'
  },
  collections,
  textStyles,
  components
};
