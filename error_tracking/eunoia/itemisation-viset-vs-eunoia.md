# Itemisation: VISET vs eunoia — Comparison Analysis

_As of 25 Sep 2026. Read from source: VISET `viset/venn.py` (+ interactive), eunoia-py
`_plot.py` / `_render_common.py` / `_metrics.py`, eunoia Rust core
`crates/eunoia/src/plotting/glyphs*`. Standalone analysis for feeding into other agents._

## TL;DR

Both print member names inside regions, but they solve it differently. eunoia is more
general, faster, better at filling irregular regions, and consistent across a diagram.
VISET is more readable as an aligned list and never drops a name. VISET's two best ideas
(aligned columns + guaranteed no-drop) are exactly what eunoia lacks, which is where a real
contribution lives.

## The core mental model

- **VISET:** find the biggest rectangle that fits inside the region, then pour one aligned
  block of names into it, sized as large as that rectangle allows.
- **eunoia:** measure every name as its own box, then pack those boxes as rows directly on
  the region's true shape, shrinking them all by one shared factor until they fit.

Everything below is detail on those two sentences.

## How VISET works (your approach)

- Pure Python, sits on top of eunoia's fitted shapes (matplotlib only).
- Rasterises each region to a pixel grid, builds region masks by boolean AND / NOT of sets.
- Finds a text box inside the region:
  - curved regions: largest inscribed axis-aligned rectangle, found with a summed-area table,
    searched over 1 to 8 column layouts;
  - rectangles: grows a box outward from the centroid (or deepest point) until each side hits
    the boundary.
- Lays names into monospace, space-padded columns that line up into a table. Count stacked above.
- Binary-searches the largest font per region that still fits the box.
- Because the box is wholly inside the region, the outline never crosses the text.
- If nothing fits at min font, it uses the column count that overflows least. It never drops names.

### How VISET handles word length
- Columns are fixed width (monospace), so each cell is as wide as the longest name in that
  column plus a gutter. Short names get padded with spaces.
- A very long name widens its whole column, which can shrink the font for that region.
- Trade-off: guaranteed alignment and readability, but wasted width on short names and a
  long name penalises the whole column.

## How eunoia works (Johan's approach)

- Rust core packer with a thin Python layer. Same engine also places the unit-glyph dots.
- Python measures each name's box size, then hands the region polygon rings plus per-name
  box sizes to the Rust packer (`place_glyph_boxes`).
- Default arrangement `Uniform` = row / shelf packing: rows share one height, boxes fill each
  row left to right at their own proportional widths, block centred on the region's pole of
  inaccessibility. (`Random` = dart-thrown scatter, used for the dots look.)
- Sizing is one diagram-wide scale factor `k`, bisected in `[min_scale, 1.0]`, shrink-only,
  so the font stays consistent across all regions.
- Obstacle-aware: member boxes avoid set labels and each other.
- If a region cannot hold its items, they go to `unplaced` and it warns. Names can be dropped.

### How eunoia measures names (important detail)
- Two backends measure differently:
  - static (matplotlib): measures text through the real renderer. Accurate.
  - interactive (plotly): measures from the font's glyph-advance table (fontTools). His own
    code comment calls this approximate, because the browser draws a different font than the
    one measured, so widths "will not match to the pixel."
- The glyph-advance sum also ignores kerning (small letter-pair spacing). Minor, but another
  small error source.
- So proportional measurement is exact only for the exact font drawn; under font substitution
  it drifts, which can cause a wrong fit / drop decision.

### How eunoia handles word length
- Each name is measured up front and gets a box of its own width, so a long name simply takes
  a wider slot on its row. Different lengths are handled by per-name width, not by resizing text.
- The font and font size do not change per name. There is one size for all names; the only
  size change is the single global shrink `k` applied equally.
- A very long name becomes one wide box. If it will not fit even at min scale, it is dropped
  and a warning is raised. It never wraps a word across lines and never truncates.
- Rows were chosen deliberately over a uniform grid: the code notes a max-cell grid would let
  one long name inflate every cell (exactly VISET's column penalty).

## Head to head

| Aspect | VISET (you) | eunoia (Johan) |
|---|---|---|
| Layer | Pure Python, matplotlib-only | Rust core, shared across R/Julia/JS |
| Region geometry | Rasterised grid; inscribed rectangle only | True polygon (holes-aware), packs concavities |
| Name layout | Monospace aligned columns (table) | Proportional rows (ragged), centred on pole |
| Width handling | Fixed-width cells; long name widens its column | Per-name measured width; long name = wider box |
| Measuring | Real renderer (matplotlib) | Real renderer (static); glyph-advance table (interactive, approximate) |
| Font sizing | Largest font per region (varies) | One shared scale for whole diagram (consistent) |
| Font | Locked monospace | Any font (proportional by default) |
| Count | Stacked above the list | Separate (`quantities`) |
| Overflow | Never drops (overflow-least fallback) | Warns and drops unplaced |
| Obstacle avoidance | None (stays inside region) | Yes (labels + other boxes) |
| Speed / scaling | Slower; grid-resolution limited | Fast; resolution-independent |
| Interactive | Separate Plotly reimplementation | Plotly backend shares the engine |

## What works better, honestly

**eunoia wins on:**
- Filling irregular / curved regions: it packs the real polygon, so crescents and concave
  regions get used; VISET confines text to an inscribed rectangle and wastes the rest.
- Consistency: one scale means fonts match across regions; VISET's per-region maximisation
  looks uneven.
- Generality, speed, obstacle-awareness, one engine for names + dots across all bindings.

**VISET wins on:**
- Readability: monospace columns actually line up into a scannable table; eunoia's
  proportional rows are ragged.
- Faithfulness: it never silently drops a name; eunoia can drop and warn.
- Robust widths: monospace width is exact and survives font substitution; eunoia's
  proportional measuring can drift, especially in the browser / plotly path.
- Integrated count above the list.

## Where this points (contribution ideas)

Three VISET ideas are genuinely missing upstream and are in-scope Python work:

1. Aligned / columnar arrangement (a new `arrangement` alongside `uniform` / `random`) that
   brings VISET's table-like readability into eunoia.
2. A monospace option so width is exact and robust to font substitution, offered as opt-in
   with proportional kept as the default. Mainly improves fit detection.
3. A no-drop / overflow-least fallback so packing shrinks-to-fit rather than dropping and
   warning, bringing VISET's faithfulness guarantee upstream.

All three build on what VISET already does, and none exist in eunoia today. Good candidates
for the one contribution that is genuinely hers.
