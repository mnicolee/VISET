# TODO / Known Issues

## CI: `nbdev-test` fails on `06_upset.ipynb` under numpy 2.x

**Status:** open (pre-existing; not caused by the nbdev pin / sync-check work)

**Symptom:** `nbdev-test` (the `Run tests` CI step) fails while executing
`nbs/06_upset.ipynb` at the `upset({...})` call:

```
While Executing Cell #9:
  ...
  File ".../upset function", line 91, in upset
    fig.canvas.draw()
  ...
  File ".../matplotlib/text.py", line 863, in draw
    posx = float(self.convert_xunits(x))
TypeError: only 0-dimensional arrays can be converted to Python scalars
```

**Root cause:** version drift. CI installs the newest numpy (currently
`2.4.6`, since numpy is unpinned). During `fig.canvas.draw()`, matplotlib
does `float(x)` on a text label's x-position, and that position is a
length-1 numpy array rather than a scalar. numpy 1.x quietly allowed
`float(np.array([v]))`; numpy 2.x raises `TypeError`.

The offending text is almost certainly one of `upsetplot`'s own count
labels (`show_counts=True`) - every text call in our `upset()` function
passes a scalar x (`ax_int.text(i, y_data, g, ...)`). So this is an
`upsetplot` x numpy-2.x incompatibility surfaced by the notebook, not a
bug in our own text code.

**Fix options:**
1. Quick: pin numpy below 2 in `pyproject.toml` deps, e.g. add `'numpy<2'`.
   Restores the behavior the notebook was working under. Bigger hammer
   (constrains a core dep), so decide deliberately.
2. Proper: reproduce locally with numpy 2.x, find the array-valued text
   position, and coerce it to a scalar. Likely requires upgrading
   `upsetplot` to a numpy-2-compatible release (if one exists) or a small
   monkey-patch, since the position originates inside `upsetplot`.

**Related note:** the interactive Plotly notebooks needed `nbformat`, which
has been added to the `dev` deps (fixes `05_venn_interactive`,
`07_upset_interactive`, `index`). Only `06_upset.ipynb` remains failing.
