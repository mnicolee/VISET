"""False intersection region in `style="box"` (eunoia shape="rectangle") layouts.

Real data, no synthetic sets: the DGIdb 2024 drug-target library shipped in
`Drug target sample files/DGIdb_Drug_Targets_2024.txt`.

    Etomidate   17 targets, 16 of them inside Topiramate  (GABA-A receptor subunits)
    Tezampanel   9 targets,  9 of them inside Topiramate  (AMPA/kainate receptor subunits)
    Topiramate  42 targets

Etomidate and Tezampanel share **zero** targets - GABA-A vs glutamate receptors,
no gene in common. Both sit almost entirely inside Topiramate. The rectangle
fit cannot satisfy that, so it returns geometry in which the two drug shapes
overlap by ~41% of the smaller one. VISET computes its counts from real set
membership, finds nothing to put in that region, and `viset/venn.py:191`
(`if not s: continue`) skips it - so the false intersection renders as a large
blank grey block with no count and no members.

`fitted_values` agrees there is no intersection; only the returned outlines
disagree. Same failure class as `eunoia_false_lens.ipynb`, but that notebook
covers circle/ellipse - on this dataset ellipse is clean (0.0%) and only the
box/rectangle layout fails.

Run from anywhere:  python repro/make_box_false_region.py
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager
from matplotlib.path import Path
import eunoia as eu

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
for f in font_manager.findSystemFonts(fontpaths=[os.path.join(ROOT, "Font")]):
    font_manager.fontManager.addfont(f)
from viset import eunoia_venn  # noqa: E402

SRC = os.path.join(ROOT, "Drug target sample files", "DGIdb_Drug_Targets_2024.txt")
A, B, C = "Etomidate", "Tezampanel", "Topiramate"   # A & B share nothing; both nested in C

sets = {}
for line in open(SRC, encoding="utf-8"):
    parts = [p for p in line.rstrip("\n").split("\t") if p.strip()]
    if len(parts) >= 2:
        sets[parts[0].strip().capitalize()] = set(parts[1:])
data = {k: sorted(sets[k]) for k in (A, B, C)}


def drawn_overlap(fit, a, b, n=500):
    "Fraction of the smaller drawn shape covered by the drawn a&b overlap."
    o = fit.plot_data["shape_outlines"]
    allp = np.vstack([np.asarray(o[k]) for k in o])
    gx = np.linspace(allp[:, 0].min(), allp[:, 0].max(), n)
    gy = np.linspace(allp[:, 1].min(), allp[:, 1].max(), n)
    GX, GY = np.meshgrid(gx, gy)
    P = np.column_stack([GX.ravel(), GY.ravel()])
    ma = Path(np.asarray(o[a])).contains_points(P)
    mb = Path(np.asarray(o[b])).contains_points(P)
    return (ma & mb).sum() / max(min(ma.sum(), mb.sum()), 1)


for k in (A, B, C):
    print(f"{k:12s} n={len(sets[k]):3d}   inside {C}: {len(sets[k] & sets[C])}")
print(f"\n{A} & {B} shared targets: {sorted(sets[A] & sets[B]) or 'NONE'}")

print("\nshape      drawn A&B overlap   diag_error   fitted A&B region")
for shape in ("rectangle", "ellipse"):
    fit = eu.euler(data, shape=shape, seed=0)
    key = next((k for k in fit.fitted_values if set(k.split("&")) == {A, B}), None)
    print(f"{shape:10s} {drawn_overlap(fit, A, B) * 100:15.1f}%   {fit.diag_error:10.4f}   "
          f"{'absent (=0)' if key is None else round(fit.fitted_values[key], 2)}")

dfs = [pd.DataFrame({k: data[k]}) for k in (A, B, C)]

# the failure: rectangles draw a ~41% overlap between two sets sharing nothing
out = os.path.join(HERE, "drug_box_false_region.png")
eunoia_venn(dfs, colors=["#3a7ca5", "#e08a3c", "#3c8c57"], style="box", seed=0,
            title=f"style='box'  -  {A} & {B} share ZERO targets",
            figsize=(11, 8.5), save_path=out)
print(f"\nwrote {out}")

# the control: same data, ellipses - the fit is exact and the two shapes stay apart
out_r = os.path.join(HERE, "drug_ellipse_control.png")
eunoia_venn(dfs, colors=["#3a7ca5", "#e08a3c", "#3c8c57"], style="round", seed=0,
            title=f"style='round'  -  same data, {A} & {B} correctly drawn apart",
            figsize=(11, 8.5), save_path=out_r)
print(f"wrote {out_r}")
