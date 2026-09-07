# Episode 01 · Build a name generator

Open **[episode_01.ipynb](episode_01.ipynb)** in VS Code. This is the main teaching
artifact, with explanations, code, executed outputs, and four charts.
For a read-only walkthrough, open [episode_01.html](episode_01.html) in a browser.
Start with the short [code companion guide](CODE_GUIDE.md) for setup, function
explanations, and common questions. The [presenter guide](PRESENTER_GUIDE.md)
contains the longer narration notes.

## Setup

Use Python 3.11 or newer; verified here with Python 3.14.2. From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r episodes/01_names/requirements.txt
```

In VS Code, use its Python and Jupyter extensions, open the notebook, and select
`.venv/bin/python` using the notebook's kernel picker. Run the cells in order.
The notebook supports a working directory of either the repository root or
`episodes/01_names`. It uses the bundled dataset and does not download anything.

For recording, copy the notebook to `episode_01.RECORDING.ipynb` **in the same
folder**, restart its kernel, and clear its outputs. Keep the completed notebook
available as a checkpoint. The recording copy is ignored by Git.

The model uses standard-library Python only. Matplotlib and its dependencies
(including NumPy internally) support charts; there is no NumPy model code or
PyTorch dependency. Jupyter executes and displays cells.

## What is included

| File | Purpose |
|---|---|
| `episode_01.ipynb` | Main presentation and viewer download |
| `episode_01.html` | Executed browser-readable copy |
| `lesson.py` | Editable source, using `# %%` notebook cell markers |
| `visuals.py` | Chart formatting and table printing; no model logic |
| `build_notebook.py` | Generate notebook; optionally execute and export HTML |
| `release_report.py` | Save experiment evidence during builds, outside the teaching cells |
| `test_lesson.py` | Tests of the exact functions taught in the lesson |
| `data/` | Bundled names, checksum, attribution, and upstream license |
| `outputs/` | Four chart PNGs and the actual experiment's `results.json` |
| `PRESENTER_GUIDE.md` | Explanations, verified numbers, and recording checkpoints |
| `CODE_GUIDE.md` | Short viewer companion and troubleshooting |

For maintained changes, edit `lesson.py`, then regenerate. Direct notebook edits
are fine for exploration, but regeneration overwrites them. Copy useful edits
back to `lesson.py` before rebuilding.

```bash
# Correctness tests (standard library only).
.venv/bin/python -m unittest discover -s episodes/01_names -p 'test_*.py' -v

# Regenerate, execute every cell in a fresh kernel, and export HTML.
.venv/bin/python episodes/01_names/build_notebook.py --execute
```

The build creates a private temporary kernel configuration using the invoking
Python interpreter. It does not install or modify a global Jupyter kernel.
The final notebook has 41 cells, including 25 code cells, and preserves the
recorded scope with 100 samples in each batch. It ends at the test comparison;
the build tool saves the results report separately from the visible lesson.
Without `--execute`, the builder produces a notebook with cleared outputs;
existing HTML and report files still refer to the previous executed run.

## Verified reference run

29,494 unique names; training/validation/test sizes 23,595 / 2,949 / 2,950.
Vocabulary: 26 ordinary characters; a 27 × 27 table with separate START and END.
Natural-log loss includes END and averages over predictions, not name averages.

The unsmoothed bigram has 8 zero-probability validation predictions and therefore
infinite validation NLL. The selected candidate is **k = 0.3**, with validation
NLL **2.456622**. This is the best of the tested grid, not a universal optimum.

| Model | Final test NLL, nats per prediction |
|---|---:|
| Uniform | 3.295837 |
| Unigram | 2.818510 |
| Smoothed bigram, k = 0.3 | 2.460499 |

All three are evaluated on the same 21,053 test predictions. The toy regression
check reproduces `P(ana) = 0.0625` and average NLL `0.693147`.
Seeds and the Python version are stored in the report. Exact sample strings can
depend on runtime behavior; the checked-in outputs document the verified run.
