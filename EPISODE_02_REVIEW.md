# Episode 02 · Theory recording review

Reviewed September 10, 2026. Scope: the theory reference, 29-frame canvas,
offline theory reader, presenter narration, and theory/coding separation.

## Ready materials

- [Theory reference](EPISODE_02_THEORY.md)
- [Editable theory canvas](canvas/episode_02_trigrams.excalidraw)
- [Offline theory presentation](canvas/episode_02_theory.html)
- [Presenter narration and cues](canvas/EPISODE_02_CANVAS_GUIDE.md)
- [Separate coding-video plan](episodes/02_trigrams/CODING_VIDEO_PLAN.md)

## Correctness findings resolved

1. Longer context is presented as a tradeoff with data support, not as an
   inherently inferior model. A small sample's 100% estimate is not a claim
   of certainty about the population.
2. The new four-string example shows evidence splitting beyond trigrams while
   leaving the observed next-token probabilities unchanged. A separate local
   nnn query demonstrates missing longer-context evidence. It is not labeled
   as an unsmoothed generated prefix.
3. Corpus changes are explicit: anna/ava have four outcomes; the separate
   anna/enna/inna/onna corpus has five ordinary characters plus END, six outcomes.
   The 26-character capacity calculation is a third setting, not empirical data.
4. Zero-probability targets are distinguished from entire unobserved rows.
   A raw 0/0 count estimate is unspecified. Positive add-k produces a uniform
   distribution for an empty row and does not add training observations.
5. The simple backoff illustration selects a whole normalized row. It repairs
   missing contexts but leaves zeros in observed rows; it is not claimed to be
   Katz backoff or a complete smoothing solution. Interpolation mixes defined
   normalized distributions. Equal weights are a teaching choice.
6. Capacity counts include valid START prefixes, exclude END from histories,
   and retain one END prediction per name. Independent-parameter details are
   moved to the presenter appendix to keep the spoken explanation focused.
7. Rounded NLL is marked approximately. The original toy probabilities remain
   P_bigram(ana)=1/16, P_trigram(ana)=0, and P_trigram,k=1(ana)=1/75.
8. The measured experiment and its numerical outcomes are absent from the
   theory canvas. The coding plan describes empirical testing, not proof of a
   universal outcome. The existing lab and saved experiment report are retained.
9. Episode 03 teaches learned bigram weights. Embeddings/MLP and representation
   sharing arrive in Episode 07; the endpoint remains the planned small
   decoder-only Transformer trained at laptop scale.

## Executed checks

- **12 tests passed** across `test_lab.py` and `test_lesson_material.py`:
  boundary reset, target counts, exact paths, NLL, normalization, generation,
  missing evidence, Episode 01 validation continuity, evidence splitting,
  fallback and interpolation distributions, and valid capacity counts.
- Rebuilt the canvas, both reader paths, and presenter guide from the source.
- Verified 29 editable frames and 29 well-formed SVG scenes; checked frame
  bounds and approximate rendered text widths, with no fitting warnings.
- Rendered all 29 frames at 1200×675 using the repository's PNG renderer and
  visually inspected all frames for clipping, overlaps, legibility, and labels.
  The final changed frame was rendered again after its wording adjustment.
- Checked Markdown math delimiters/braces/alignment blocks, JavaScript syntax,
  theory scope markers, and local companion links.
- Exercised reader navigation, scene selection, overview, speaker-note toggle,
  Present, and Escape in an isolated DOM harness. This is a logic check, not
  a live browser rendering test. Exact Excalidraw/browser typography may differ
  from the local preview renderer.
- Confirmed no “visual study” labels, empirical winning context, or saved
  validation-result numbers remain in audience canvas text.

Reproduce the mathematical checks from the repository root:

```bash
python3 -m unittest discover -s episodes/02_trigrams -p 'test_*.py' -v
python3 canvas/build_episode_02.py
```

## Source verification

Rechecked [Jurafsky and Martin, Chapter 3](https://web.stanford.edu/~jurafsky/slp3/3.pdf),
especially n-gram estimation and §3.6 on smoothing/interpolation/backoff;
[Chen and Goodman (1996)](https://aclanthology.org/P96-1041/) for the empirical
smoothing reference; and [Bengio et al. (2003)](https://jmlr.org/papers/v3/bengio03a.html)
for shared learned representations. The toy calculations and their checks are
our own teaching examples. This is an internal correctness review, not an
endorsement by those authors.

## Recording handoff

The presenter guide estimates 26 minutes including pauses. Use a recording
copy for annotations and frame 29 as the sources end card. Sections 6–7 mention
practical responses with limits; a full implementation belongs to the build.
The coding notebook and final test evaluation are outside this theory revision
and are not represented as complete.

## Episode 02A release follow-through

Recording completed. The [11-page audience guide](docs/episode-02-theory.pdf)
and [29-page canvas PDF](docs/episode-02-canvas.pdf) are finalized for the
YouTube description. The guide incorporates the clarifications developed
while learning: START padding, equal/fewer context matches, backoff's missing-row
rule, and the smoothed counts behind interpolation. All PDF pages were rendered
and visually reviewed; the 12 mathematical checks passed again.

The five-part video edit, chapter boundaries, media checks, thumbnail alternatives,
and publishing status are documented in the
[release record](youtube/EPISODE_02A_RELEASE.md).
