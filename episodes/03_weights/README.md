# Episode 03A · From counts to weights

Theory preparation for the next numbered episode after the counting-to-learning
bridge. The core route is **current character → score-row lookup → softmax → target NLL**.
The worked examples retain Episode 01's `anna` / `ava` corpus and boundaries.

## Start here

1. [Theory reference](../../EPISODE_03_THEORY.md): intuition, worked arithmetic,
   prerequisites, limitations, source links, and optional presenter details.
2. [Offline presentation](../../canvas/episode_03_theory.html): 20 frames,
   speaker notes, overview, keyboard navigation and presentation mode.
3. [Presenter script](PRESENTER_GUIDE.md): four recording blocks, narration,
   pointing cues, and flexible rehearsal allocations totaling about 32 minutes.
4. [Understanding checks](EXERCISES.md), then [the separate answer key](ANSWERS.md).

[Editable Excalidraw canvas](../../canvas/episode_03_weights.excalidraw) ·
[Preparation review](../../EPISODE_03_REVIEW.md)

The hand-set change `W[a,END]=ln 2` lowers toy training NLL from 1.386294 to
1.331437; `ln 100` raises it to 1.806672. All three scores average the same
9 training targets, including END. These are demonstrations, not optimizer
results or a new real-data comparison.

## Reproduce and maintain

From repository root, using the existing environment:

```bash
.venv/bin/python episodes/03_weights/verify_theory.py
.venv/bin/python -m unittest discover -s episodes/03_weights -p 'test_*.py' -v
.venv/bin/python canvas/build_episode_03.py
```

For a clean environment, install NumPy with
`python3 -m pip install -r episodes/03_weights/requirements.txt`.
Then use that Python executable for the commands above. The canvas builder itself
uses the standard library and the bundled series font.

Edit `scenes.json` for audience text, narration and cues;
`../../canvas/build_episode_03.py` for diagram layouts; `reader_template.html`
for presentation controls. Rebuilding overwrites only Episode 03's generated
canvas, HTML and script. Preserve hand annotations in a `.RECORDING.excalidraw`
copy. The offline reader approximates Excalidraw with SVG; it does not use the
full Excalidraw renderer.

The NumPy verifier checks the theory arithmetic. The complete Episode 03B coding
companion is now available below. Later gradient lessons remain separate work.

[Optional math](OPTIONAL_MATH.md) retains one-hot encoding, matrix multiplication
and target-vector cross-entropy. These are not prerequisites for this episode.

## Current recording sequence

Frames 1–6 introduce the task, compare count and weight training, and motivate
softmax. Frames 7–11 evaluate all-zero weights completely, including every target
in anna/ava and the average over nine predictions. Frames 12–13 show the ln 2
improvement and ln 100 overshoot. Frames 14–20 connect to updates, stability,
limits, generation and gradients. The count-probability equivalence is optional.

## Recorded Episode 03A

Use the [final edited 19-frame canvas](../../canvas/episode_03_final.excalidraw)
for the recorded episode. The 20-frame HTML and presenter guide are rehearsal
materials retained for reference. [Upload package](../../youtube/EPISODE_03A_METADATA.md).

## Episode 03B · Coding companion

Prepared September 30, 2026, following publication of 03A (presenter confirmed).

- [Start here: setup and code guide](CODE_GUIDE.md)
- [Executed notebook](episode_03.ipynb) and [HTML reading copy](episode_03.html)
- [Editable cell source](lesson.py)
- [Coding presenter walkthrough](CODING_PRESENTER_GUIDE.md)
- [Coding exercises](CODING_EXERCISES.md) and [answers](CODING_ANSWERS.md)
- [Verification and scope](CODING_REVIEW.md)

Core route: reproduce the theory in NumPy, measure chosen changes, and generate.
The presenter removed the optional real-data extension for recording.
Generation remains a notebook exploration; the video closes after weight comparison.
No gradient training is claimed.

[Recorded 03B upload package](../../youtube/EPISODE_03B_METADATA.md) · [Release checks](../../youtube/EPISODE_03B_RELEASE.md).
