# TODO / Known Issues

## CI: `nbdev-test` fails on `06_upset.ipynb` under numpy 2.4+

**Status:** fixed - CI installs the upstream fix
([UpSetPlot PR #302](https://github.com/jnothman/UpSetPlot/pull/302), unmerged)
instead of upsetplot's broken 0.9.0 release.

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
length-1 numpy array rather than a scalar. The text is `upsetplot`'s, not ours.

**Versions:** breaks on numpy **>= 2.4.0** only (2.0-2.3 just warned). CI runs
2.4.6; the local `viset` conda env now runs 2.4.6 too, upgraded from 2.2.6.

**Caveat:** `pyproject.toml` still lists plain `'upsetplot'`, since PyPI rejects
direct-URL deps - so `pip install viset` gets the broken 0.9.0. Vendor the patch
before publishing.

**Related note:** the interactive Plotly notebooks needed `nbformat`, which
has been added to the `dev` deps (fixes `05_venn_interactive`,
`07_upset_interactive`, `index`). Only `06_upset.ipynb` remains failing.

## Venn layout: random layouts, and false intersection regions

**Status:** seed fixed; rectangles fixed; circle/ellipse still open.

**Random layout (fixed).** `eunoia_venn_interactive` never passed a seed, so it
re-randomised every run. Now takes `seed=0` like the static one. Verified
identical geometry across separate processes, and `seed=7` gives a different
layout.

**False intersection regions (rectangles fixed).** eunoia could return shapes
that overlap for sets sharing nothing - see `repro/`. Cause was the default
`loss="sum_squared"`, which minimises *total* error and tolerates one badly wrong
region. Both venn functions now take `loss=None`, defaulting to `"max_absolute"`
for rectangles only. On the drug dataset that takes the false overlap from 41.3%
to 0.0%. Circle/ellipse deliberately keep eunoia's default, so their output is
unchanged.

**Still open:** circle/ellipse can't draw two sets nested in a third that share
nothing - geometrically impossible, so no loss fixes it (`max_absolute` helps,
29% -> 5%, but doesn't clear it). Mitigation: at `venn.py:191` (`if not s:
continue`), test the region mask already built at `venn.py:186`; if an empty
region has real drawn area, warn and draw an explicit `0` instead of leaving it
blank.

## Let Mass-spec-BioID consume VISET instead of copying it

**Status:** open.

`Mass-spec-BioID` re-defines `eunoia_venn`, `eunoia_venn_interactive` and the
upset plotters inside its notebooks, so VISET fixes never reach it. Its copies
are an older generation (helpers `_pole` / `_perim` / `_fit_box` vs VISET's
`_max_font_rect` / `_center_rect`), and none of its three `eu.euler` calls pass
a seed - so both static and interactive re-randomise every run.

**Plan:** delete the copied cells there and import from VISET instead. No PyPI
needed - either an editable install (`pip install -e ../VISET`, updates are
instant) or a `requirements.txt` line
`viset @ git+https://github.com/lnicole08/VISET.git@main`, pinned to a tag when
figures must stay fixed.

**Gotchas:** `pip install -U` won't re-fetch a git URL unless `__version__` is
bumped; the copies have diverged, so figures need eyeballing after the swap; and
until the upsetplot patch is vendored, BioID has to install the fork too.
