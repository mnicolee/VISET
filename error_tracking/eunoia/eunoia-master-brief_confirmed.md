# VISET × eunoia — Status & Checklist

_As of 25 Sep 2026. Cross-checked against Johan's emails, project docs, and GitHub
(eunoia-py v0.6.0, eunoia Rust core). Single working reference + shareable checklist._

---

## 0. Definitions — read first (don't confuse these)

- **Glyphs = DOTS. Counts. "How many."** `plot(glyphs=True)` draws one dot per item in a
  region; you read the number of dots. No text.
- **Itemisation / packed members = WORDS. Names. "Who."** `plot(members=...)` prints the
  actual member names inside the region, auto-shrunk to fit. This is VISET's feature.
- Test: readable names → itemisation. Countable dots → glyphs.
- Under the hood both use the **same box-packing engine** (fit N boxes into a region; a dot
  is a box with a dot, a name a box with text), so improving packing helps both. But they
  are two separate, mutually exclusive plot options — never call glyphs "names" or
  itemisation "dots."

---

## 1. Summary — what's been going on

- Johan offered **co-authorship on the eunoia JOSS paper**, conditional on a real code
  contribution from Nicole. He is submitting to JOSS in ~2 weeks (email ~11 Sep).
- The original deal had three items: (1) **itemisation** — Johan builds the Rust core, hands
  Nicole the Python binding to implement; (2) **glyphs** — optional/later; (3) a
  **fit-quality repr PR** — Nicole's one concrete task.
- **What's happened since: Johan built and shipped nearly all of it himself (v0.6.0).**
  - Itemisation (the Python `members=` feature that was Nicole's to implement) — **done by him.**
  - Glyphs (dots) — **done by him.**
  - Fit-quality repr — **done by him.**
  - Interactive Plotly backend — **shipped**, but undocumented / not in the gallery.
  - Comparisons doc — now looks complete (was "rough, Claude-generated").
  - Colour bug in "Two sets intersecting inside a third" — **his to fix**, status unconfirmed.
  - Label placement — open, mostly **his Rust work.**
- **Net:** all three agreed contributions are now done by Johan. Nicole needs to (a) test the
  package thoroughly, (b) give design feedback he asked for, and (c) find and ship **one new
  Python contribution that is genuinely hers** before travel.

**VISET overlap:** VISET's headline features (name itemisation + interactive hover) are now
both upstream in eunoia-py, so VISET largely duplicates the package under it. The natural
bridge back to a real contribution is the shared **glyph/name packing engine** and the
**faithfulness gap** (surfacing when a diagram misrepresents the data).

---

## 2. Checklist — what to do

### A. Test itemisation / packed members
- [ ] Run the current packed-members examples; confirm they work.
- [ ] Confirm each name lands in the correct region.
- [ ] Test 2-set and 3-set cases.
- [ ] Test nested-set cases.
- [ ] Test small / narrow intersection regions.
- [ ] Test uneven region sizes and very different member counts.
- [ ] Test short vs long names.
- [ ] Increase member counts to see how auto-sizing behaves.
- [ ] Check for overlap, clipping, boundary collisions, unreadably small text.
- [ ] Check whether names are silently dropped when space runs out.
- [ ] Note where VISET handles anything better / worse / differently.

### B. Evaluate glyph (dots) rendering — Johan asked for your opinion
- [ ] Run the glyph examples (`glyphs=True`).
- [ ] Use the same diagrams as packed-members so the two can be compared.
- [ ] Check dots stay countable at low / medium / high counts.
- [ ] Check small / narrow regions and crowded intersections.
- [ ] Look for poor spacing, random-looking placement, collisions, excessive shrinking.
- [ ] Write concrete suggestions for better layout (e.g. rows/grid vs scattered dots, overflow handling).
- [ ] Flag any improvement that helps BOTH glyphs and names (shared engine).

### C. Find poor label-placement cases (for Johan to fix in Rust)
- [ ] Hunt for badly placed set labels: nested sets, tight overlaps, small regions.
- [ ] Look for labels straddling boundaries or in confusing spots.
- [ ] Look for leader lines crossing labels / boundaries / each other.
- [ ] Save reproducible code + screenshot + short note for each case.
- [ ] Separate "for Johan (Rust)" from "I could fix in Python."

### D. Test interactive / Plotly backend
- [ ] Confirm interactive diagrams render.
- [ ] Test hover / region + member info.
- [ ] Test itemisation with the interactive backend specifically.
- [ ] Note missing docs, missing examples, or incomplete behaviour.

### E. General package testing
- [ ] Work through the whole gallery; confirm examples run without errors.
- [ ] Try deliberately awkward / adversarial set configs.
- [ ] Record crashes, warnings, inconsistent or surprising output.
- [ ] Note any differences between static and interactive output.

### F. Comparisons doc
- [ ] Read it start to finish; check claims match actual behaviour.
- [ ] Flag anything inaccurate, unclear, or machine-generated in tone.
- [ ] Only rewrite if there's a substantive improvement left (may already be handled).

### G. Ship one replacement contribution (the key outcome)
- [ ] Keep a shortlist of Python issues found during testing.
- [ ] Prefer one discovered via itemisation / glyph / Plotly testing (stays close to the collaboration).
- [ ] Strong candidate: **extend the fit-quality repr to surface missing / false regions**
      (requested ≠ fitted / dropped zero-count regions). Confirm first whether zero-count
      regions are recoverable from the fit object or need Python-side reconstruction.
- [ ] Other candidates: packed-member overflow / fallback behaviour; small API / validation /
      docs / test improvements.
- [ ] Pick ONE bounded enough to finish before travel. Implement with tests. Open a clean PR
      (problem, before/after, tests).

---

## 3. Recommended order

1. Itemisation testing → 2. Glyph testing + feedback → 3. Label failure cases →
4. Plotly testing → 5. General gallery testing → 6. Comparisons review →
7. Pick & implement one replacement contribution → 8. Package findings + PR for Johan.

---

## 4. Deliverables to Johan
- [ ] Short summary of what was tested.
- [ ] Itemisation / packed-member findings.
- [ ] Concrete glyph-rendering suggestions.
- [ ] A few reproducible bad label-placement examples.
- [ ] Any Plotly / documentation issues.
- [ ] At least one concrete PR that is yours.

---

## 5. Out of scope / already done
- Do NOT re-implement Python itemisation — Johan shipped it.
- Do NOT re-implement basic glyphs — they exist.
- Do NOT redo the fit-quality repr from scratch (extending it is fine).
- Do NOT take the colour bug unless Johan reassigns it.
- Do NOT take Rust-core label work unless he asks — your role is finding failure cases.

---

## 6. Constraints & logistics
- **Python only.** No Rust, no R. JavaScript unconfirmed (lean no) — flag before handoff.
- eunoia-py PRs are plain `.py` + their test setup (NOT nbdev; nbdev is VISET-only).
- **No unpublished lab data** in any public repo or anything an agent/Codex touches.
- **Travel: mid next week to 12 Oct; likely uncontactable until 6 Oct.** Aim to contribute
  this week before leaving.
