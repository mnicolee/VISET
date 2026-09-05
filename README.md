# VISET

> **Vis**ual **I**temized **SET** diagrams: area-proportional Venn/Euler and UpSet plots that print the **member names** inside each region, in Python.

**📖 Docs & interactive figures: https://mnicolee.github.io/VISET**

Venn/Euler diagrams read best for **2 to 3 sets**; **UpSet** takes over when there are more. Below, both are drawn on drug-target sets as static (Matplotlib) figures — every region or bar lists the actual genes. When an intersection is too small to print its members legibly, reach for the **interactive** (Plotly) versions on the [documentation site](https://mnicolee.github.io/VISET) and hover the region to read them.

## Venn / Euler (three drugs)

**Static** (Matplotlib): proportional ellipses, every gene printed and auto-sized to fit its region.

<details class="code-fold">
<summary>Code</summary>

``` python
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager
from viset import load, eunoia_venn
fp = "Font" if os.path.isdir("Font") else "../Font"
for f in font_manager.findSystemFonts(fontpaths=[fp]):
    font_manager.fontManager.addfont(f)
db = "Drug target sample files/" if os.path.isdir("Drug target sample files") else "../Drug target sample files/"
def L(name, fname): return load(db + fname, "Gene names", name)
flx = L("Fluoxetine", "1. FLUOXETINE_sample.csv")
ibu = L("Ibuprofen", "2. IBUPROFEN_sample.csv")
ace = L("Acetaminophen", "3. ACETAMINOPHEN_sample.csv")
eunoia_venn([flx, ibu, ace], colors=["#3a7ca5", "#e08a3c", "#3c8c57"], style="round", title="", figsize=(8.5, 7.5), margin=0.06, seed=0)
```

</details>

![](index_files/figure-commonmark/cell-2-output-1.png)

## UpSet (four drugs)

**Static** (Matplotlib): one bar per intersection with its members listed inside, so it keeps working past the three-set limit of a Venn.

<details class="code-fold">
<summary>Code</summary>

``` python
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager
from viset import load, upset
fp = "Font" if os.path.isdir("Font") else "../Font"
for f in font_manager.findSystemFonts(fontpaths=[fp]):
    font_manager.fontManager.addfont(f)
db = "Drug target sample files/" if os.path.isdir("Drug target sample files") else "../Drug target sample files/"
def L(name, fname): return load(db + fname, "Gene names", name)
ibu = L("Ibuprofen", "2. IBUPROFEN_sample.csv")
ace = L("Acetaminophen", "3. ACETAMINOPHEN_sample.csv")
dic = L("Diclofenac", "12. DICLOFENAC_sample.csv")
ind = L("Indomethacin", "13. INDOMETHACIN_sample.csv")
upset({"Ibuprofen": ibu, "Acetaminophen": ace, "Diclofenac": dic, "Indomethacin": ind},
      figsize=(13, 7), color_list="Set2", wspace=0.5)
```

</details>

![](index_files/figure-commonmark/cell-4-output-1.png)

## Learn more

Want the reasoning behind all this? See [State of current set diagrams](https://mnicolee.github.io/VISET/state_of_set_diagrams.html) for the existing tools and their gaps, and the [Introduction](https://mnicolee.github.io/VISET/introduction.html) to install VISET and run it on your own data. Full-page interactive versions: [Venn](https://mnicolee.github.io/VISET/venn_interactive.html) and [UpSet](https://mnicolee.github.io/VISET/upset_interactive.html).
