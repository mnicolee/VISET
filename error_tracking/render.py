"""Child-process side of the version comparison: draws and measures under whichever
eunoia `eunoia_versions.run` has put on the path. Not meant to be imported directly
from the notebook -- the notebook's own eunoia is a different version.
"""
import json
import sys

import eunoia as eu
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from drug_data import DATA, LABELS
from measure import false_regions

SHAPES = ("rectangle", "square", "circle", "ellipse")
LOSSES = ("sum_squared", "max_absolute")


def grid(out_path, seed=0):
    "One panel per shape x loss, titled with the worst false region it draws."
    fig, axes = plt.subplots(len(SHAPES), len(LOSSES), figsize=(11, 19))
    for row, shape in zip(axes, SHAPES):
        for ax, loss in zip(row, LOSSES):
            fit = eu.euler(DATA, shape=shape, seed=seed, loss=loss)
            fit.plot(ax=ax, quantities=True, legend=False)
            bad = false_regions(fit, DATA, LABELS)
            worst = max(bad.values()) if bad else 0.0
            verdict = f"FALSE REGION {worst * 100:.1f}%" if bad else "clean"
            ax.set_title(f"{shape}, loss={loss}\n{verdict}", fontsize=10,
                         color="crimson" if bad else "seagreen")
    fig.suptitle(f"eunoia {eu.__version__}  (seed={seed})", fontsize=13, y=0.999)
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    print(json.dumps({"version": eu.__version__, "path": out_path}))


def sweep(n_seeds=20):
    "How many of the first `n_seeds` seeds draw a region the data says is empty."
    out = {}
    for shape in SHAPES:
        for loss in LOSSES:
            hits = 0
            for seed in range(n_seeds):
                fit = eu.euler(DATA, shape=shape, seed=seed, loss=loss)
                if false_regions(fit, DATA, LABELS):
                    hits += 1
            out[f"{shape}|{loss}"] = hits
    print(json.dumps({"version": eu.__version__, "n_seeds": n_seeds, "counts": out}))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "grid":
        grid(sys.argv[2])
    elif cmd == "sweep":
        sweep(int(sys.argv[3]) if len(sys.argv) > 3 else 20)
