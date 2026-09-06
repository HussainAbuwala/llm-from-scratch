# Episode 01 release documents

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
