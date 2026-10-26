# PR #66 review fixes

## #1: Hover text got cut off

**Fix:**
- Added a max width (`fig width − 30`) alongside the existing max height.
- Box width is estimated as `longest line × 0.6 × font size + 9px` (monospace hover font).
- If the box is too wide, the hover font shrinks from 13px in 0.5px steps until it fits, down to `13 × 0.35 = 4.55px` (the same ratio as packed members).

## #2: Label didn't fit in short figures

**Fix:** the title now follows matplotlib's `tight_layout`:
- No title: no title band (same as before the PR).
- With a title: the figure stays exactly `width × height`; the title band comes out of that height and the diagram shrinks to fit.
- Band height = `title lines × 1.3 × font + 8px gap + 1.08 × font`.
- Default title font = `20 × √(width / 500)`, shrinking (not below 3px) to fit the width and at most 0.25 of the height.
