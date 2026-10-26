<!--

1. Updating author and affiliations list:

authors:
  - name: Johan Larsson
    orcid: 0000-0002-4029-5945
    affiliation: "1"
  - name: Nicole M. Lee
    orcid: 0000-0001-6953-2177
    affiliation: "2"
affiliations:
  - name: Department of Mathematical Sciences, University of Copenhagen, Denmark
    index: 1
    ror: 035b05819
  - name: Program in Neuroscience and Behavioral Disorders, Duke-NUS Medical School, Singapore
    index: 2
    ror: 02j1m6098

2. Insert the "# Features" section after the complete "# Software Design"
   section, before "# Research Impact Statement".

3. Add this entry to paper/paper.bib:

@article{micallef2012,
  author       = {Micallef, Luana and Dragicevic, Pierre and Fekete,
                  Jean-Daniel},
  title        = {Assessing the Effect of Visualizations on {Bayesian}
                  Reasoning through Crowdsourcing},
  journaltitle = {IEEE Transactions on Visualization and Computer Graphics},
  date         = {2012-12},
  volume       = {18},
  number       = {12},
  pages        = {2536--2545},
  issn         = {1077-2626},
  doi          = {10.1109/TVCG.2012.199}
}
-->

# Features

Area-proportional Euler diagrams encode the size of each set intersection as
the area of a region. Eunoia extends this with three complementary additions.
Unit glyphs show how many elements a region contains, member labels show which
elements they are, and interactive output exposes regions that are too small
to annotate.

## Glyphs

Glyphs are equally sized circular marks, one per data unit, packed inside the
region they belong to, following the eulerGlyphs approach of
@micallef2012. Glyphs can also be added to Venn diagrams.

All glyphs in a diagram are the same size, so that counts can be compared
across regions. By default, Eunoia searches for the largest common size that
fits every region's count. In Python, a fixed size can be set instead, and a
warning is given if any glyphs do not fit. In Python and the web app, glyphs
are kept clear of the diagram's labels where space allows.

The web app and the JavaScript package offer four arrangements, namely a
hexagonal grid (the default), a rectangular grid, an even scatter, and a
random scatter. The Python package offers the hexagonal grid and the random
scatter.

## Member Labels

Member labels add the elements themselves to the diagram, so that each region
shows which elements it contains rather than only a set name or a count. In
Python, member names are available when the input is given as member lists, or
as array or DataFrame input with identifiers. They are drawn with
`plot(members=...)` in one of two modes.

- **List mode** (the default) draws each region's names as a single block of
  text. A block that does not fit inside its region is placed outside it with
  a leader line. If a maximum number of names per region is set, only that
  many are shown, followed by a "+N more" line.
- **Packed mode** places each name individually inside its region. When space
  is limited, all names are reduced by the same factor, down to a minimum
  size, and names that still do not fit are left out with a warning.

In the web app, names are typed in for each region and drawn in packed mode.
If a region's names do not all fit, they are shown as a single block instead,
as in list mode, so no names are left out. Names are not drawn when a diagram
has more than 500 in total.

## Interactivity

The Python package provides an interactive plotly backend through
`fit.plot_plotly()`. It adds a hover tooltip to each region showing the
intersection label, its sample size, and its members. This is primarily useful for dense multi-set diagrams, in which
small regions cannot hold any text. The JavaScript SVG serializer similarly
supports native tooltips and data attributes on each region, so that host pages
can add their own interaction. The web app provides controls for glyph mode,
spacing, and styling.
