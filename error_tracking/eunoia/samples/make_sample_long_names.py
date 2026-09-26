"""Generate a sample long-name dataset for testing eunoia's packed/list members.

Three sets (Drug A, Drug B, Drug C) with made-up gene-style names (2-13 chars) and
long protein-style names (up to ~58 chars). All names are invented; only the
set sizes, overlaps and name-length spread are chosen to give a realistic,
crowded layout (including a tiny three-way overlap).

Run from anywhere:  python make_sample_long_names.py
Writes sample_long_names_DrugA.csv, _DrugB.csv, _DrugC.csv next to this script,
each with columns "Gene names" and "Protein names".
"""
import random
import string
from pathlib import Path

import pandas as pd

SEED = 7
OUT = Path(__file__).parent

# members per region (exclusive counts)
REGIONS = {
    ("Drug A",): 61,
    ("Drug B",): 20,
    ("Drug C",): 25,
    ("Drug A", "Drug B"): 11,
    ("Drug A", "Drug C"): 2,
    ("Drug A", "Drug B", "Drug C"): 5,
}

# gene-name length -> how often (mostly short, a few long)
GENE_LENGTHS = {2: 5, 3: 34, 4: 32, 5: 29, 6: 19, 7: 12, 8: 5, 9: 4, 10: 3, 11: 1, 12: 2, 13: 1}
# protein-name length ranges -> how often
PROTEIN_LENGTHS = {(8, 9): 2, (10, 19): 15, (20, 29): 11, (30, 39): 14, (40, 49): 5, (50, 58): 4}

PROTEIN_WORDS = [
    "Putative", "Probable", "Uncharacterized", "protein", "kinase", "subunit", "regulator",
    "receptor", "transporter", "factor", "homolog", "domain-containing", "alpha", "beta",
    "gamma", "delta", "membrane", "nuclear", "binding", "activating", "associated",
    "ribosomal", "ligase", "hydrolase", "phosphatase", "complex", "light", "chain",
    "repeat", "cytoplasmic", "signal", "transcription", "polarity", "adapter", "scaffold",
]

rng = random.Random(SEED)


def gene_name(length):
    """Gene-style name of exactly `length` characters, e.g. Xg21, RhoLK88B, Qt-7alpha."""
    styles = [
        lambda: rng.choice(string.ascii_uppercase) + rng.choice(string.ascii_lowercase)
                + "".join(rng.choices(string.digits, k=8)),
        lambda: "".join(rng.choices(string.ascii_uppercase, k=2))
                + "".join(rng.choices(string.digits, k=8)),
        lambda: rng.choice(string.ascii_uppercase)
                + "".join(rng.choices(string.ascii_lowercase, k=3))
                + "".join(rng.choices(string.ascii_uppercase + string.digits, k=8)),
        lambda: rng.choice(string.ascii_uppercase) + rng.choice(string.ascii_lowercase)
                + "-" + "".join(rng.choices(string.digits, k=2)) + rng.choice(["alpha", "beta", "gamma", "sigma"]),
        lambda: "".join(rng.choices(string.ascii_lowercase, k=12)),
    ]
    name = rng.choice(styles)()
    return (name + "".join(rng.choices(string.ascii_lowercase, k=13)))[:length]


def protein_name(lo, hi):
    """Protein-style phrase between lo and hi characters, built from common words."""
    target = rng.randint(lo, hi)
    words = []
    while len(" ".join(words)) < target:
        word = rng.choice(PROTEIN_WORDS)
        if len(" ".join(words + [word])) > hi:
            word = rng.choice([w for w in PROTEIN_WORDS if len(" ".join(words + [w])) <= hi] or [None])
            if word is None:
                break
        words.append(word)
    name = " ".join(words)
    return name[0].upper() + name[1:]


def draw(weights, n):
    keys = list(weights)
    return rng.choices(keys, weights=[weights[k] for k in keys], k=n)


total = sum(REGIONS.values())
gene_lengths = draw(GENE_LENGTHS, total)
protein_ranges = draw(PROTEIN_LENGTHS, total)

rows = {s: [] for s in ["Drug A", "Drug B", "Drug C"]}
seen_g, seen_p = set(), set()
i = 0
for region, count in REGIONS.items():
    for _ in range(count):
        g = gene_name(gene_lengths[i])
        while g in seen_g:
            g = gene_name(gene_lengths[i])
        p = protein_name(*protein_ranges[i])
        while p in seen_p:
            p = protein_name(*protein_ranges[i])
        seen_g.add(g)
        seen_p.add(p)
        for s in region:
            rows[s].append({"Gene names": g, "Protein names": p})
        i += 1

for s, r in rows.items():
    pd.DataFrame(r).to_csv(OUT / f"sample_long_names_{s.replace(' ', '')}.csv", index=False)
    print(f"{s}: {len(r)} names -> sample_long_names_{s.replace(' ', '')}.csv")
