# Hover box sizing: modifications

All changes are in `python/eunoia/_plotly.py` (`_add_hover`, `_hover_text`, plus the new
`_hover_box_width` and `_fit_hover_text`).

To revert: `git restore python/eunoia/_plotly.py`

## Section 1: box limits
- max height = fig height − top margin − 30 (unchanged)
- max width = fig width − 30 (new)
- box width ≈ longest line (chars) × 0.6 × font size + 9 (6px arrow + 3px padding)
- hover font = IBM Plex Mono, hover box only (replaces the `TEMP` block)

## Section 2: height → columns
- line height = 17px at font size 13
- max rows = max height // line height − 2
- columns = ceil(names / max rows), names padded so columns line up (unchanged)

## Section 3: width → shrink font
- font size starts at 13 (the ceiling), then steps down by 0.5
- line height = 17 × size / 13
- char width = 0.6 × size
- rows and columns redone at each size
- stops at the first size where box width ≤ max width
- each region gets its own size

## Section 4: min font → leave out + warn
- min font = 13 × 0.35 = 4.55 (same ratio as the core's packed-member `min_scale`)
- still too wide at 4.55 → drop columns until it fits
- names shown = max rows × columns − 1, last line `+N more`
- one `UserWarning` per figure, with the count + first 5 names per region:
  ```
  some member names did not fit in the hover box and were left out:
    Kinase inhibitors: 157 left out (GENE143, GENE144, GENE145, GENE146, GENE147, ...)
  Try a larger figure size
  ```

## Regression #2: title band (like matplotlib's tight_layout)
- no title → no band, same as before the PR
- fixed `height` → figure stays `width × height`; band comes out of it, diagram = height − band
- no `height` → diagram sized from width, band added on top
- label/member/glyph placement uses the diagram height, so it matches what plotly draws
- lines = only the user's line breaks, counted like plotly (`<br>`, `<BR>`, `<br >`), no auto-wrap
- band = lines × 1.3 × font + 8px gap + 1.08 × font edge pad
- default font = 20 × √(width / 500) (20px at 500px); shrinks 0.5 at a time until each line fits the width (width − 20) and band ≤ 0.25 × height; never below 3px
- `fontsize` or `font.size` → used as-is, no limit (band capped at the figure height so code doesn't break)
- `title` docstring updated (`_models.py`)
- to revert: `git restore python/eunoia/_plotly.py python/eunoia/_models.py`
