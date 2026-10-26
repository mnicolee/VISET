# Eunoia writeup: shared notes (Claude + Codex)

Goal: a short writeup on **itemisation (member labels), glyphs, and
interactivity** in the new Eunoia (Rust core `jolars/eunoia` v1.10.0 and
Python `jolars/eunoia-py`).

Sources were cloned at the commits below. Re-clone if they are missing:

- `jolars/eunoia` @ `102ff26`
- `jolars/eunoia-py` @ `83fe459`

## Handoff log

| # | Who | What | Next |
|---|-----|------|------|
| 1 | Claude | Researched both repos, wrote fact sheet below and `draft.md` v1 | Codex: fact-check `draft.md` against the sources; list issues in the section "Codex review" below, don't rewrite the draft |
| 2 | Codex | Checked draft against both source trees; found sizing, obstacle, callout and Plotly qualifications, plus omitted packing and SVG interactivity features; draft unchanged | Claude |
| 3 | Claude | Rewrote draft short and plain per user (1 page, no em dashes). Verified Codex #1 and #10 in source, applied #1-7 and #10 in plain words. Skipped #8, #9 and fine print in #6 to keep it 1 page | User review |
| 4 | Claude | Rewrote draft in Johan's paper.md style (formal, pandoc citations, his section style), still no em dashes, ~1 page. Uses keys from eunoia `paper/paper.bib` plus new `micallef2012` (entry below, needs checking) | Codex: check `micallef2012` entry is the real eulerGlyphs paper |
| 5 | Codex | Completed round 2 source, citation, online bibliography and tone checks; micallef2012 verified; remaining qualifications recorded below; draft unchanged | Claude: consider round 2 qualifications |
| 6 | Claude | Applied round 2 #1, #3, #5, #6, #10 as small wording changes. Left #2 as is (draft makes no effectiveness claim), #7, #8 and #12 as too fine for 1 page. TODO add micallef2012 to the bib used for building | User review |
| 7 | Claude (+ reviewer subagent) | User caught a misleading Rust-only claim. Ran a strict user-perspective review (per-binding scope, no obvious/internal details). 9 findings; spot-checked #1-5 in source, all confirmed. Rewrote draft from the user's view | User review |
| 8 | Codex | Completed round 3 sentence-by-sentence code review, YAML/bibliography style checks and attempted all requested metadata APIs; remaining qualifications and online verification failures recorded below; draft unchanged | Claude: consider round 3 findings and complete online identifier/Crossref checks |
| 9 | Claude + Nicole | Verified online: ORCID 0000-0001-6953-2177 = Nicole MynYi Lee; ROR 02j1m6098 = Duke-NUS Medical School, 035b05819 = University of Copenhagen; micallef2012 fields match Crossref. Applied round 3 #1, #4 (500-name limit, names skipped not truncated), #5, #7, #9; Nicole skipped #6 and the tooltip-coverage nuance. Interactivity simplified to hover = intersection label, sample size, members (glyphs/members in plotly are opt-in, hover members on by default). Draft final | Nicole: paste author block, Features section, and micallef2012 into eunoia paper |

## Status (2026-10-26)

**`draft.md` is final.** Its top comment has the three merge steps for
`eunoia/paper/paper.md` and `paper.bib`. The fact sheet below is from round 1
and is outdated in places (e.g. Python offers only two glyph arrangements, the
web app never shows "+N more"). Trust `draft.md` and the review sections over
it.

## Extra bib entry (not in Johan's paper.bib)

```bibtex
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
```
_Restyled to match Johan's paper.bib (biblatex fields, as wilkinson2012); fields from Crossref record for the DOI._

## Fact sheet (with sources)

### Glyphs ("how many")
- One equal-sized dot per data unit, packed inside its region, after
  eulerGlyphs (Micallef, Dragicevic & Fekete, IEEE TVCG 2012).
  `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx`
- Placement runs in the Rust core, so every binding gives identical output.
  Rust `place_glyphs`, npm `placeGlyphsForRegions`, C `eunoia_place_glyphs`.
- Returns one diagram-wide `radius`, `positions` per region, and `unplaced`.
  Same radius everywhere is deliberate so counts stay comparable.
- Arrangements: `uniform` (default, hex lattice at pole of inaccessibility),
  `rectangular`, `lowDiscrepancy` (Halton), `random` (seeded dart throwing,
  then a force-directed relaxation pass).
- Auto radius: bisects for the largest radius where every region fits its full
  count. Fixed radius: fills what it can, reports the rest in `unplaced`.
- `gap` (default 0.25) sets spacing; `boundaryGap` sets edge clearance
  separately.
- Label keep-out: label boxes can be passed as `obstacles`;
  `obstaclePolicy` = `bestEffort` (default) or `strict`. With obstacles,
  auto radius can't shrink below half its obstacle-free value.
- Disconnected region pieces split their count by area (largest remainder).
- Counts are supplied by the user; spec quantities are areas, not assumed to be
  cardinalities.

### Itemisation / member labels ("which ones")
- `place_glyph_boxes` (Rust) / `placeGlyphBoxesForRegions` (npm) pack measured
  `w x h` boxes for member names; return one rect per item plus a diagram-wide
  `scale`. Core is font-blind: caller measures, core packs.
- `uniform` packs rows centred on the pole of inaccessibility;
  `targetAspectRatio` can favour square blocks (`c0737eb`).
- Scale is **shrink-only** in `[minScale, 1]`, `minScale` default 0.35.
- Items are taken in order; the result is a **prefix** of the input, so
  dropped names are decided by input order. Dropping is expected, not a bug.
- Web app: per-combination roster fields; if a roster doesn't fit, the whole
  roster becomes a callout block with a leader (`fae7882`).
  `eunoia/web/src/lib/members.ts`
- Python: membership-list input (e.g. `{"A": ["Ada", ...]}`) keeps names on
  `fit.members`. `plot(members=True)` = list mode; `members={"mode": "packed"}`
  packs names; `max` caps names with a `"+N more"` line.
  `eunoia-py/python/eunoia/_render_common.py:237`

### Interactivity
- Web app at eunoia.bz/app fits diagrams in-browser via WASM; has Glyphs ->
  Draw -> Dots / Member names, dot styling (fill, border colour, border
  width), spacing controls.
- Python `fit.plot_plotly(...)` (extra: `pip install 'eunoia[plotly]'`,
  added `edfd6e8`, 2026-07-09) returns a `plotly.graph_objects.Figure`.
  `eunoia-py/python/eunoia/_plotly.py`
- Hover tooltips per region (invisible fill traces, `hoveron="fills"`): region
  key, `n = count`, member names. `hover=True|"members"|"quantities"|"all"`.
- Stated reason for the backend: dense diagrams where names don't fit in small
  regions; hover covers them.
- Text measured with fontTools metrics since plotly can't measure
  synchronously; approximate, as the browser font differs.
- Glyph dots in plotly use `hoverinfo="skip"`, so hovering shows the region
  tooltip, not per-dot info.

## Codex review (round 2)

Reviewed the entire current draft against the supplied snapshots on 2026-10-26. Paths below beginning `eunoia/` and `eunoia-py/` are relative to the read-only `scratchpad/repos` directory named above. Draft line numbers refer to this round's unchanged draft. No cloned-repository code was run or installed.

1. **Summary, draft:8-14: area encoding, recent additions and complementary roles are supported, with two wording qualifications.** The paper defines area-proportional regions by intersection size (`eunoia/paper/paper.md:49-51`); glyph/member additions appear in 1.9.0 and 1.10.0 (`eunoia/CHANGELOG.md:3-35`). Calling interactivity an “encoding” is a loose classification; it is an interaction mechanism exposing information. Shared-core deterministic glyph placement is documented (`eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:11-14`), but identical complete rendered label layouts across bindings require identical measured boxes, polygons, options and seeds. Python backends measure text differently (`eunoia-py/python/eunoia/_plotly.py:9-14`). “Same input” should mean the same core placement input, not just the same dataset.

2. **Glyph definition and attribution, draft:18-23: supported.** Equal circular marks, one per requested data unit, eulerGlyphs inspiration, countable frequencies and the hybrid area/count rationale are stated in `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:3-14`. Separate user-supplied counts, non-cardinality spec areas and Venn support are explicit at `:375-382`. “Reinforce each other” describes complementary encodings, not an established improvement in comprehension: the cited study reports no measurable visualization benefit in its first experiment ([author's university record](https://kar.kent.ac.uk/30782/)). Avoid extending this sentence into an empirical effectiveness claim.

3. **Radius and shortfalls, draft:25-29: supported as a search objective, not a global optimality guarantee.** One shared radius and `unplaced` in both sizing modes are documented at `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:18-27`; auto bisection and fixed sizing at `:74-83`. With obstacles, the radius cannot shrink below half its obstacle-free value and strict mode can leave a region empty (`:143-155`). The next sentence about reported shortfalls helps, but qualify “largest value at which every region holds its full count” as what the search seeks. Packing feasibility is not provably monotone, so bisection is not a proof of the mathematical maximum (`eunoia/crates/eunoia/src/plotting/glyphs/boxes.rs:25-30`, explicitly also discussing discs).

4. **Four arrangements and obstacle policy, draft:29-34: supported.** Default pole-anchored hexagonal lattice, rectangular grid, filtered Halton sequence and seeded darts followed by relaxation are documented in `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:40-70`. Best-effort permits overlap; strict guarantees clearance for returned glyphs and reports the remainder (`:148-155`). The draft now distinguishes these correctly.

5. **Font-blind member boxes, rows and scale, draft:38-42: two small qualifications remain.** Caller measurement and one diagram-wide scale are supported (`eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:166-195`). Rows describe the default uniform arrangement; random packing throws rectangular darts (`:199-206`), so add “by default” to “packs ... into rows.” Automatic scale is bounded above by 1, but 0.35 is the default configurable `min_scale`, not an invariant floor; obstacles can impose a higher floor. Sources: `eunoia/crates/eunoia/src/plotting/glyphs/boxes.rs:64-74`, `:97-106`. The new “automatic mode” qualification correctly resolves the earlier explicit-scale issue.

6. **Prefix/order and expected omissions, draft:43-46: supported.** Packing stops at the first item that fits nowhere; each region's returned boxes are a prefix of its supplied items, including under either obstacle policy. Wide names make omissions expected. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:240-260`. Interpret “prefix of the input” per region rather than as a single flattened diagram-wide sequence.

7. **Python member retention and list/packed/cap modes, draft:48-50: supported.** Membership-list identities are retained on `fit.members` (`eunoia-py/python/eunoia/_models.py:129-145`). List is the default display mode, packed is accepted, and a positive `max` adds `+N more` only when the list exceeds the cap (`eunoia-py/python/eunoia/_render_common.py:237-274`). A list label can be moved outside if it does not fit, so “lists them in their regions” is not an unconditional inside-placement guarantee (`eunoia-py/python/eunoia/_plotly.py:151-155`).

8. **Web roster fallback, draft:50-52: supported for drawable regions, with an exception.** Incomplete individual packing is replaced by one complete measured roster block, placed inside if possible and outside with a leader otherwise. Requested regions without drawable geometry instead appear in a separate “no geometry” list without a leader. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:262-278`. The rewritten inside/outside distinction fixes the earlier issue; qualify the generalization if covering absent geometry.

9. **Plotly API, geometry, approximate metrics and purpose, draft:56-61: supported.** `plot_plotly` is exposed at `eunoia-py/python/eunoia/_models.py:298-342`. Both renderers consume the fit's region pieces and shape outlines (`eunoia-py/python/eunoia/_plotly.py:105-113`, `:147-149`; `eunoia-py/python/eunoia/_plot.py:105-109`, `:241`). Approximate fontTools metrics and hover coverage for regions too small for text are explicitly explained at `eunoia-py/python/eunoia/_plotly.py:1-14`. The current “same geometry” wording avoids the earlier unsupported claim of identical label appearance.

10. **Hover contents and “each region,” draft:58-60: mostly correct; narrow the coverage claim.** Default hover shows the combination and available quantity/member identities; quantity is `original_values` or otherwise `fitted_values`, so “quantity” is more accurate than “count.” Hover traces cover drawable pieces, skip the empty-combination complement and rings with fewer than three points, and may be disabled or content-filtered. Source: `eunoia-py/python/eunoia/_plotly.py:850-896`; `eunoia-py/python/eunoia/_models.py:312`, `:338-342`. Prefer “drawable non-complement regions by default” over an unconditional “each region.”

11. **SVG hooks and browser app, draft:61-64: supported.** Optional `tooltip` emits a native SVG title, `interactive` emits `data-combination`/`data-area`, and `regionAttrs` supports host event hooks (`eunoia/web/src/routes/docs/reference/javascript/+page.svx:330-357`). Entirely browser-side fitting is described in `eunoia/paper/paper.md`, Software Design; glyph mode, spacing and styling are documented in `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:47-55`, `:99-112`, `:262-263`. This verifies snapshot capabilities, not the currently deployed site.

12. **Citation-key audit: passes the requested exception rule.** The draft contains exactly two distinct citation keys, including narrative citations: `eunoia2026` at draft:9 and `micallef2012` at draft:20. `eunoia2026` exists in `eunoia/paper/paper.bib:40-47`; `micallef2012` is absent as expected and supplied above. One version qualification: that software entry cites 1.9.0 (`:43`), whereas the draft also describes features added in 1.10.0 (`eunoia/CHANGELOG.md:3-15`). Key existence passes, but the citation alone does not identify the full reviewed feature version. For compilation, the extra entry must ultimately be included in the bibliography used by the draft; this review does not modify it.

13. **Extra `micallef2012` entry: verified online; all eight requested fields are correct.** The eulerGlyphs author's site explicitly recommends this paper and matches the authors, title, journal, volume, issue, pages and year ([eulerGlyphs, Licensing Terms](https://www.eulerdiagrams.com/eulerGlyphs/)). The author's university repository independently confirms Luana Micallef, Pierre Dragicevic and Jean-Daniel Fekete; *Assessing the Effect of Visualizations on Bayesian Reasoning through Crowdsourcing*; IEEE Transactions on Visualization and Computer Graphics; 18(12); 2536–2545; 2012; DOI `10.1109/TVCG.2012.199`, and links the record to eulerGlyphs ([Kent Academic Repository](https://kar.kent.ac.uk/30782/)). No BibTeX correction is needed. The initial bare-domain and DOI resolver requests failed, but online verification succeeded through the www project site and Kent record.

14. **Tone and punctuation, entire draft: broadly matches the paper.** Like `eunoia/paper/paper.md:29-45` and its Software Design section, the draft uses a Summary, title-case topical headings, compact explanatory paragraphs, concrete API names, restrained technical language and Pandoc citations. It is more narrowly a feature overview, and “font-blind”/“readability floor” echo the docs' vocabulary more than the paper's, but neither is a significant tonal mismatch. No em-dash character or `---` prose dash occurs, and no prose colon occurs. The only colons are YAML `title:` and `bibliography:` at draft:2-3; the `---` at draft:1 and :4 are YAML delimiters. The reference paper itself does use prose colons and triple-hyphen em dashes, so avoiding them is the user's style constraint rather than a feature copied from that paper.

## Codex review

1. **Claim: the scale "only ever shrinks" and text is "never enlarged".** This is true only for automatic scale selection. An explicit `scale` above 1 is honoured, and `min_scale` is ignored for explicit scales. Qualify both statements as defaults/auto mode. Source: `eunoia/crates/eunoia/src/plotting/glyphs/boxes.rs:64-74`.

2. **Claim: auto radius is the largest size where every region fits its full count; only fixed-radius overflow is mentioned.** That describes the search goal, not an unconditional guarantee: obstacles impose a floor at half the obstacle-free radius, and strict mode can leave items unplaced or even a region empty at that floor. Tell readers to check `unplaced` in either sizing mode. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:26-27`, `:142-155`.

3. **Claim: passing label boxes as obstacles keeps dots clear of labels.** Passing obstacles alone does not guarantee this: default `bestEffort` permits overlap; `strict` requires clearance and reports shortfalls. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:148-159`; implementation policy: `eunoia/crates/eunoia/src/plotting/glyphs.rs:62-70`.

4. **Claim: a web roster that does not fit becomes a callout "outside the diagram with a leader line".** The app replaces incomplete individual packing with one measured block containing the heading, optional count and entire roster. The block stays inside if it fits; only otherwise is it placed outside with a leader. A missing-geometry roster is a separate "no geometry" list without a leader. Other regions are repacked without the overflow roster. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:262-278`; implementation: `eunoia/web/src/lib/member-layout.ts:80`, `:155-200`.

5. **Claim: Plotly has "the same geometry and labels as the static plot".** Shared fit geometry and label-content helpers are supported, but identical label placement/appearance is too strong. Plotly uses approximate fontTools text metrics instead of live Matplotlib measurements; the browser may render a different font. Source: `eunoia-py/python/eunoia/_plotly.py:1-14`, `:46-49`.

6. **Claim: a tooltip on "each region" shows "its name, count and members".** Defaults show the combination key and whatever data is available; names require retained member identities. The displayed `n` comes from `original_values` or, failing that, `fitted_values`, so it need not be an integer cardinality. Hover traces only cover drawable region pieces, explicitly skip the empty combination/complement, and ignore outer rings with fewer than three points. Source: `eunoia-py/python/eunoia/_plotly.py:850-868`, `:884-896`. `hover=False` disables tooltips; `"members"`, `"quantities"` (alias `"counts"`) and `"all"` select content (`:858-862`; `eunoia-py/python/eunoia/_models.py:338-342`).

7. **Important omission: counts are supplied separately, and both dots and member boxes also work on Venn geometry.** Spec quantities are floating-point areas, not assumed cardinalities. The "20 members shows 20 dots" example is supported when the requested count is 20 and packing succeeds; it is not automatic conversion of arbitrary areas to membership counts. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:376-382`.

8. **Claim: the core "packs the boxes into rows"; omitted packing options.** Rows describe `uniform`, not every arrangement: random box packing throws rectangular darts and has no dot-style relaxation. `targetAspectRatio` can favour square/wider/taller row blocks while preserving input order; callers can measure wrapped multiline boxes too. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:198-219`, `:247-254`.

9. **Important glyph omissions:** `gap` controls dot spacing, while `boundaryGap` independently controls clearance to boundaries, holes and label boxes; the app defaults are 0.25 and 1 respectively. Disconnected pieces receive counts proportional to area with deterministic largest-remainder rounding. These explain spacing controls and split overlaps more concretely. Source: `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:29-36`, `:84-100`.

10. **Important interactivity omission:** JavaScript SVG output also supports native hover tooltips through `tooltip(info)`, `interactive` data attributes (`data-combination`, `data-area`) and `regionAttrs(info)` for host-page event handling. The summary's interactivity row could include JS/SVG, rather than only Python and the web app. These are serializer capabilities, not evidence that the app itself currently enables region hover. Source: `eunoia/web/src/routes/docs/reference/javascript/+page.svx:330-343`.

11. **Remaining claims check out against the supplied snapshots.** The Euler-area framing, Rust/binding ecosystem, equal-radius dots and eulerGlyphs attribution, four dot arrangements and deterministic shared-core placement, font-blind box measurements, default 0.35 automatic scale floor, prefix/order contract and expected drops, Python membership retention/list/packed/max modes, Plotly extra/Figure/dense-region motivation, and browser app/mode/styling claims are supported. Key sources: `eunoia/README.md:18-19`, `:79-95`; `eunoia/web/src/routes/docs/concepts/glyphs/+page.svx:3-24`, `:40-81`, `:102-113`, `:165-193`, `:229-260`; `eunoia-py/python/eunoia/_models.py:129-145`, `:298-346`; `eunoia-py/python/eunoia/_render_common.py:237-274`; `eunoia-py/pyproject.toml:34-36`; `eunoia-py/python/eunoia/_plotly.py:1-14`. This is a source-snapshot review, not verification of present deployment or package-release timing. No cloned-repository code was run or installed.
## Codex review (round 3)

Reviewed the current draft sentence by sentence on 2026-10-26, separately against Python main (0.6.0, excluding PR #66), the JavaScript package, and web app code. Paths beginning `eunoia/` and `eunoia-py/` refer to the supplied read-only snapshots. Line numbers below are for the unchanged draft. No cloned-repository code was run or installed. Only this notes file was edited.

1. **"By default, they are made as large as possible while every region still fits its count" (draft:56-57).** This remains an unconditional success/optimality claim. The implementation searches for a feasible radius, has a fallback when no radius is feasible, and limits obstacle-driven shrinking; final placement can report shortfalls in automatic mode too. Evidence: `eunoia/crates/eunoia/src/plotting/glyphs/discs.rs:265-329`, particularly `:288-301`; Python warns whenever `unplaced` is nonempty in both modes (`eunoia-py/python/eunoia/_plot.py:679-684`, `_plotly.py:734-739`). Suggested fix: "By default, Eunoia searches for a common glyph size that fits the requested counts. Python also allows a fixed size and warns when glyphs do not fit in either mode."

2. **"It renders the same geometry, labels, glyphs, and member names as the static backend" (draft:89-90).** The shared geometry and supported content are correct, but "same" can imply identical placement and identical visible names. Plotly measures text approximately with fontTools, whereas Matplotlib measures with its renderer. This changes label placement, packed-name capacity, and label obstacles used for glyph placement. Evidence: `eunoia-py/python/eunoia/_plotly.py:9-14`, `:650-681`, `:723-733`; `_plot.py:593-624`. Suggested fix: "It uses the same fitted geometry and supports labels, glyphs, and member names." This also avoids suggesting that the bare `fit.plot_plotly()` call enables glyphs or names; those remain opt-in (`_plotly.py:78`, `_render_common.py:243-244`).

3. **"by default adds a hover tooltip to each region" (draft:90-92).** "Each" includes regions without drawable geometry and the complement, neither of which receives these traces. The content claim itself is correct, including "quantity" rather than "count" and "when these are available." Evidence: `eunoia-py/python/eunoia/_plotly.py:850-900`, especially `:887-896`. Suggested fix: "by default adds hover tooltips to drawable non-complement regions, showing their combinations, quantities, and available member names."

4. **"so no names are left out" (draft:84).** Correct for the web app's normal packing fallback, but not an unconditional rendering guarantee. More than 500 names across the diagram skips member rendering and reports the budget limit. Evidence: `eunoia/web/src/lib/components/DiagramSvg.svelte:406-410`, `:426-428`, `:469`, `:526-537`. The fallback itself preserves the whole roster (`eunoia/web/src/lib/member-layout.ts:97-104`, `:148-200`), including a separate column for missing geometry. Suggested fix: "This preserves the complete roster when individual names do not fit." If retaining a universal guarantee, state the 500-name rendering limit. The current omission of a guaranteed outside leader is appropriate because complete blocks may fit inside and missing-geometry blocks have no leader.

5. **"Glyphs are kept clear of the diagram's labels where space allows" (draft:58-59).** Accurate as best-effort behavior for Python and the app, which supply measured label obstacles. For the JavaScript placement API this requires the caller to supply obstacles; passing region geometry and counts alone does not make it aware of labels. Evidence: Python `_plot.py:249-283`, `_plotly.py:723-733`; app `eunoia/web/src/lib/components/DiagramSvg.svelte:374-383`; JS `eunoia/ts/index.ts:2082-2097` only forwards explicitly supplied obstacles. Suggested fix: "Python and the web app avoid diagram labels where space allows; JavaScript callers can supply label obstacles." Alternatively omit this sentence if the extra interface qualification is too detailed.

6. **"all names are reduced by the same factor, down to a minimum size" (draft:79-80).** Correct for default automatic packed sizing, but Python exposes explicit `scale`, which bypasses automatic shrinking and can exceed 1. Evidence: `_plot.py:610-617`, `_plotly.py:663-673`; core `eunoia/crates/eunoia/src/plotting/glyphs/boxes.rs:64-74`. Suggested fix: begin "By default, when space is limited ..." The omission-with-warning statement passes for packer shortfalls in both renderers (`_plot.py:619-624`, `_plotly.py:675-680`); there is no automatic overflow summary replacing packed names.

7. **"glyph and label placement is implemented in the Rust core, so that all interfaces share a single implementation" and "the web app fits and renders diagrams entirely in the browser" (draft:46-47, 95-96).** These are substantially true, but repeat Software Design's core plotting/label placement and browser-side fitting discussion (`eunoia/paper/paper.md:216-221`). The shared-core sentence is also an implementation detail in a user-facing Features introduction; measurement and overflow composition still live in each frontend. Evidence for shared packing calls: Python `src/lib.rs:850`, `:902`; JS `ts/index.ts:2008-2116`; app `member-layout.ts:139-147`. Suggested fix: remove the shared-implementation sentence here and retain only the new control information at the end, for example "The web app provides controls for glyph mode, spacing, and styling." The opening area-encoding sentence also repeats paper:49-51, but serves as reasonable short context rather than a significant problem.

8. **"ror: 02j1m6098", "ror: 035b05819", "orcid: 0000-0001-6953-2177", and the `micallef2012` metadata (draft:11, 16, 19, 25-37). Online verification could not be completed in this round.** All four requested endpoints failed through the web tool and direct PowerShell requests, including TLS 1.2 retries; ORCID was explicitly requested with `Accept: application/json`. Therefore I cannot certify that the ROR records name Duke-NUS Medical School and University of Copenhagen, that the ORCID belongs to Nicole M. Lee, or that every BibTeX field matches the current Crossref response. Evidence/required checks: https://api.ror.org/v2/organizations/02j1m6098 ; https://api.ror.org/v2/organizations/035b05819 ; https://pub.orcid.org/v3.0/0000-0001-6953-2177/person ; https://api.crossref.org/works/10.1109/TVCG.2012.199 . Suggested fix: complete these API checks before merging, without guessing replacements. Check article type, all three authors in order, full title, journal, December 2012 date, volume 18, issue 12, pages 2536--2545, ISSN 1077-2626 and DOI 10.1109/TVCG.2012.199. Round 2's independent bibliographic checks are historical supporting evidence, not a substitute for the requested Crossref comparison.

9. **"2. # Features\" section to be directly after \"# Software Design\"" (draft:21).** Minor merge-note typo, with a closing quote but no opening quote before `# Features`. Suggested fix: `2. Insert the "# Features" section after the complete "# Software Design" section.` This makes clear that insertion precedes Research Impact Statement, rather than the Software Design body. This is an HTML-comment edit for Claude, not a prose-style violation.

What passed:

- **Interface scope and arrangements (draft:51-64).** Shared equal-size circles and Venn support are supported by the region-based placement code, Python Venn fit's inherited plotting and supplied quantities, and the app's Venn annotations. Python main only accepts `uniform` (default) and `random` (`eunoia-py/src/lib.rs:664-670`); JS maps all four arrangements (`eunoia/ts/index.ts:2046-2063`); the app exposes all four (`web/src/lib/components/GlyphControls.svelte:91-102`) and defaults to uniform (`web/src/lib/state.svelte.ts:63`). The app passes no fixed radius (`DiagramSvg.svelte:374-383`), so the fixed-size claim is correctly scoped to Python, although JS also supports it (`ts/index.ts:2065`). "Even scatter" is a reasonable plain description of Halton placement; "low-discrepancy scatter" would match the control name more precisely. One-per-unit is a count interpretation, not a promise that arbitrary fractional areas become counts: Python requires nonnegative integer exclusive quantities (`_render_common.py:324-340`), JS takes separate counts, and the app rounds quantities (`DiagramSvg.svelte:350-355`).
- **Member inputs and two modes (draft:68-84).** Python actually retains identities for membership lists and array/DataFrame inputs with `ids` (`_fit.py:302-346`, `_venn.py:301-351`). Default list mode, capped lists with `+N more`, packed placement and warning behavior are implemented (`_render_common.py:237-274`, `_plot.py:593-624`). The draft correctly discusses the summary line under capped list mode rather than claiming automatic summaries for packing drops. Code nuance: this snapshot applies `max` before dispatching either mode, so an explicit `max` in packed mode also supplies a `+N more` item to the packer (`_render_common.py:255-274`); do not strengthen the wording to say the option is technically exclusive to list mode. Web roster entry and full-block fallback pass, subject to finding 4.
- **Interactivity and purpose (draft:88-96).** `fit.plot_plotly()` exists (`eunoia-py/python/eunoia/_models.py:298-342`), default tooltip content and dense-region motivation are supported (`_plotly.py:9-14`, `:850-868`). JavaScript's SVG serializer emits optional native `<title>` tooltips and identifying attributes, with hooks for host interaction (`eunoia/ts/svg.ts:1023-1040`). This does not attribute region hover to the web app. Mode, spacing and styling controls are present in `web/src/lib/components/GlyphControls.svelte`.
- **YAML and bibliography form.** The authors/affiliations mapping preserves the paper's exact existing Johan entry, quoted affiliation references, numeric indexes and `ror` fields (`paper/paper.md:17-24`), adding Nicole and affiliation 2 consistently. The BibTeX uses the same `@article`, `journaltitle`, `date`, aligned equals signs, continuation indentation, `--` page range and proper-name brace protection as `paper/paper.bib:155-165`. `{Bayesian}` is appropriately protected; author wrapping preserves Jean-Daniel as Fekete's given name. No style correction is required. Record identity and field values remain unverified online as stated in finding 8.
- **Prose and overall scope.** Every Features sentence was considered against the relevant interfaces. The tone is formal and concrete, with no em dashes or prose colons in the Features section, no conspicuously pompous phrasing, and no claim that merely using the user's data is a novel capability. The glyph/member explanation adds useful information beyond Software Design; the main duplication is identified in finding 7. The eulerGlyphs attribution is consistent with the prior verified citation history, with no added empirical effectiveness claim.

