# TODO / Known Issues

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
`viset @ git+https://github.com/mnicolee/VISET.git@main`, pinned to a tag when
figures must stay fixed.

**Gotchas:** `pip install -U` won't re-fetch a git URL unless `__version__` is
bumped; the copies have diverged, so figures need eyeballing after the swap; and
`upsetplot` 0.9.0 on PyPI is still broken under numpy>=2.4, so BioID has to
install the fixed fork ([UpSetPlot PR #302](https://github.com/jnothman/UpSetPlot/pull/302))
the same way VISET's CI does.
