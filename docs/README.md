# Release documents

## Episode 02A

- `episode-02-theory.md` is the editable audience companion guide.
- `episode-02-theory.pdf` is its 11-page reading copy with rendered equations.
- `episode-02-canvas.pdf` contains all 29 theory frames, one per page.
- `build_episode_02_pdfs.py` rebuilds both, reusing the shared renderer.

```bash
python3 docs/build_episode_02_pdfs.py
```

These PDFs are designed for the YouTube description. The original editable
canvas is `canvas/episode_02_trigrams.excalidraw`; the offline HTML reader is
`canvas/episode_02_theory.html`. Download HTML and open it locally; a GitHub
blob link displays the source, not a hosted slide viewer.

## Episode 01

- `episode-01-theory.md` is the editable source for the technical handout.
- `episode-01-theory.pdf` is the audience reading copy.
- `episode-01-canvas.pdf` contains the 40 presenter frames, one per page.
- `build_pdfs.py` rebuilds both PDFs from the Markdown and Excalidraw sources.

The builder requires Python, ReportLab, Matplotlib, and Pillow. It uses
`fonts/Virgil.ttf` for handwritten canvas text. The font is distributed under
the SIL Open Font License in `fonts/OFL.txt`.

Run from the repository root:

```bash
python3 -m pip install -r docs/requirements.txt
python3 docs/build_pdfs.py
```

The editable Excalidraw file remains authoritative for rough strokes and live
presentation. The canvas PDF is a portable reading and printing copy.
