# Bridge · We built a language model. What comes next?

A standalone orientation video between Episode 02B and Episode 03A.
It completes the Count section without adding another technical episode or
renumbering the 14-part curriculum. No coding companion is needed.

## Record from these

- [Presenter script and visual cues](PRESENTER_GUIDE.md)
- [Offline presentation](../../canvas/bridge_02_to_03.html)
- [Editable Excalidraw canvas](../../canvas/bridge_02_to_03.excalidraw)
- [Learning notes and answers](THEORY.md): read first, especially the backoff distinction
- [Title, description, thumbnail and publishing notes](../../youtube/BRIDGE_02_TO_03_METADATA.md)

Eleven frames. Clarity takes priority over runtime; the earlier 3–5 minute cap
has been removed. The 1,158-word script allocates about 12 minutes with pointing
and pauses. Rehearse naturally and use the actual runtime rather than rushing.

Frames 4–7 establish the count-row, backoff and interpolation examples.
Frames 8–10 explain which evidence the mixture uses, what the pooled row loses,
and why cup-related experience might help a mug query. Frame 11 combines the motivation for weights with the three pieces needed:
adjustable weights (Episode 03), training (04–06), and a structure that reuses
weights (07). Future technical names are roadmap labels, not prerequisites.
The advanced vocabulary remains in the learning reference for the presenter.

Equations and full optimization derivations remain in later lessons. The bridge
should make the need for those lessons clear without teaching them all at once.

Open the HTML locally. Arrow keys navigate; Speaker notes is for rehearsal;
Present hides the controls and notes; Escape restores them. The editable canvas
uses the existing series visual language. For annotations, save a recording copy.
The HTML is an SVG approximation, not Excalidraw's hand-drawn renderer.

## Editorial promise

Viewers should leave able to explain why we started with counts, what failed
in the measured experiment, why count-based remedies remain valid, and why
Episode 03 deliberately revisits bigrams to teach adjustable parameters.

The following Episode 03 opening can stand alone:

> We already know how a bigram predicts the next character using counts.
> Today we'll represent that same task using adjustable weights and turn their
> scores into probabilities. This is our first step toward learning neural models.

## Maintain

Edit `scenes.json` for spoken text, timing, cues, and source attribution.
Edit `../../canvas/build_bridge_02_to_03.py` for diagrams. Rebuild from repo root:

```bash
.venv/bin/python canvas/build_bridge_02_to_03.py
```

Rebuilding overwrites only this bridge's generated canvas, reader, and presenter
script. Preserve manual canvas edits in a copy before rebuilding. Thumbnail
source and rebuild instructions are in the metadata file.

The exact three-sentence toy on frames 5–7 separates training from prediction:
first populate rows at every context length, then select one (simple backoff)
or mix their probabilities (interpolation). The earlier common/rare story is a
separate hypothetical setting; the tiny toy assigns no common/rare labels.
