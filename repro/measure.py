"""Measure what an eunoia fit actually *draws*, region by region.

`fitted_values` reports the areas the optimiser settled on; these helpers
rasterise `plot_data["shape_outlines"]` instead, so a region that the data says
is empty but the geometry still paints shows up as a non-zero number.

Region names are '&'-joined and *exclusive*: 'Simvastatin&Sunitinib' means the
part in both and in nothing else. That distinction matters on this dataset --
Simvastatin and Sunitinib do share 2 genes, but both are also in Atorvastatin,
so the two-way region is empty while the three-way one is not.
"""
from itertools import combinations

import numpy as np
from matplotlib.path import Path as MplPath


def drawn_region_areas(fit, labels, n=600):
    "Fraction of the diagram's total drawn area taken by each exclusive region."
    outlines = fit.plot_data["shape_outlines"]
    pts = np.vstack([np.asarray(outlines[k]) for k in labels])
    gx = np.linspace(pts[:, 0].min(), pts[:, 0].max(), n)
    gy = np.linspace(pts[:, 1].min(), pts[:, 1].max(), n)
    GX, GY = np.meshgrid(gx, gy)
    P = np.column_stack([GX.ravel(), GY.ravel()])
    inside = {k: MplPath(np.asarray(outlines[k])).contains_points(P) for k in labels}
    total = np.zeros(len(P), bool)
    for k in labels:
        total |= inside[k]
    areas = {}
    for r in range(1, len(labels) + 1):
        for combo in combinations(labels, r):
            mask = np.ones(len(P), bool)
            for k in combo:
                mask &= inside[k]
            for k in labels:
                if k not in combo:
                    mask &= ~inside[k]
            areas["&".join(combo)] = mask.sum() / max(total.sum(), 1)
    return areas


def true_region_counts(data, labels):
    "Members in each exclusive region, straight from the sets."
    sets = {k: set(v) for k, v in data.items()}
    counts = {}
    for r in range(1, len(labels) + 1):
        for combo in combinations(labels, r):
            s = set.intersection(*(sets[k] for k in combo))
            for k in labels:
                if k not in combo:
                    s -= sets[k]
            counts["&".join(combo)] = len(s)
    return counts


def false_regions(fit, data, labels, tol=0.002, n=600):
    "Regions with no members that are nonetheless drawn, as {name: fraction of diagram}."
    areas = drawn_region_areas(fit, labels, n=n)
    counts = true_region_counts(data, labels)
    return {k: areas[k] for k, c in counts.items() if c == 0 and areas.get(k, 0) > tol}
