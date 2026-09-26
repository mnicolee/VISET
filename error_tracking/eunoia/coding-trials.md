# Coding Trials — eunoia itemisation (with VISET comparison)

Data: `C:\Users\user\Documents\GitHub\VISET\Drug target sample files`, column `Gene names`.
Code verified against eunoia-py 0.6.0 and VISET source. Run locally to confirm output.

## Setup

```python
import pandas as pd, warnings
import eunoia as eu

DATA = r"C:\Users\user\Documents\GitHub\VISET\Drug target sample files"
def genes(f): return pd.read_csv(f"{DATA}\\{f}")["Gene names"].dropna().tolist()

A = genes("5. ATORVASTATIN_sample.csv")
S = genes("8. SIMVASTATIN_sample.csv")
U = genes("16. SUNITINIB_sample.csv")
```

## 1. Basic 2-set

```python
eu.euler({"Atorvastatin": A, "Simvastatin": S}).plot(members={"mode": "packed"})
```

## 2. Basic 3-set

```python
eu.euler({"Atorvastatin": A, "Simvastatin": S, "Sunitinib": U}).plot(members={"mode": "packed"})
```

## 3. Nested set

```python
eu.euler({"Atorvastatin": A, "Subset": A[:10]}).plot(members={"mode": "packed"})
```

## 4. Small / narrow intersection

```python
eu.euler({"Atorvastatin": A, "Sunitinib": U}).plot(members={"mode": "packed"})
```

## 5. Uneven sizes

```python
eu.euler({"Big": A, "Tiny": S[:3]}).plot(members={"mode": "packed"})
```

## 6. Word length: short vs long

```python
short = ["ACE", "TP53", "EGFR", "MYC", "KIT"]
long = ["ADORA2A", "SLC6A4x", "CYP3A4long", "TNFRSF1B", "HTR2Areceptor"]
eu.euler({"Short": short, "Overlap": short[:2] + long[:2], "Long": long}).plot(members={"mode": "packed"})
```

## 7. Many members

```python
eu.euler({"Atorvastatin": A, "Simvastatin": S, "Sunitinib": U}).plot(members={"mode": "packed"})
```

## 8. Overflow: does it drop names?  (confirms Johan ITEM 3)

```python
big = [f"VERYLONGGENE{i}" for i in range(40)]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    eu.euler({"Tiny": big[:3], "Packed": big}).plot(members={"mode": "packed"})
    print([str(x.message) for x in w])
```

## 9. Monospace vs proportional

```python
fit = eu.euler({"Atorvastatin": A, "Simvastatin": S})
fit.plot(members={"mode": "packed"})
fit.plot(members={"mode": "packed", "fontfamily": "monospace"})
```

## 10. Arrangement + scale knobs

```python
fit = eu.euler({"Atorvastatin": A, "Simvastatin": S, "Sunitinib": U})
fit.plot(members={"mode": "packed", "arrangement": "uniform"})
fit.plot(members={"mode": "packed", "min_scale": 0.3})
```

## 11. Interactive (plotly)

```python
eu.euler({"Atorvastatin": A, "Simvastatin": S, "Sunitinib": U}).plot_plotly(members={"mode": "packed"})
```

## 12. Label placement: hunt bad cases  (confirms Johan ITEM 4)

```python
eu.euler({"Atorvastatin": A, "Subset": A[:8]}).plot(members={"mode": "packed"})
eu.euler({"A": A, "S": S, "U": U}).plot(members={"mode": "packed"})
```

## 13. VISET comparison (same data)

```python
from viset.core import load
from viset.venn import eunoia_venn

dfs = [load(f"{DATA}\\5. ATORVASTATIN_sample.csv", "Gene names", "Atorvastatin"),
       load(f"{DATA}\\8. SIMVASTATIN_sample.csv", "Gene names", "Simvastatin"),
       load(f"{DATA}\\16. SUNITINIB_sample.csv", "Gene names", "Sunitinib")]
eunoia_venn(dfs, colors="Dark2", seed=0)
```

## Record per trial

Region correct, names in right region, overlap/clip/drop, font size, eunoia vs VISET.
