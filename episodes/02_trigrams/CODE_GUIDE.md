# Episode 02B - Build a trigram model and test sparsity

Start with [the executed notebook](episode_02.ipynb). It contains the complete
model code, small examples, experiment, saved outputs, and charts. The
[HTML reading copy](episode_02.html) contains the same executed lesson; download
it and open it locally. GitHub shows HTML source rather than hosting the page.

The [theory companion](../../docs/episode-02-theory.pdf) is the mathematical
reference. The [presenter guide](PRESENTER_GUIDE.md) explains how to record the
notebook. Use the preparation route below to learn it first.

## Setup

Use the existing project `.venv` from Episode 01. No dataset download is needed.
If starting on a new machine, download or clone the **whole repository**:

```bash
git clone https://github.com/HussainAbuwala/llm-from-scratch.git
cd llm-from-scratch
python3 -m venv .venv
.venv/bin/python -m pip install -r episodes/02_trigrams/requirements.txt
```

Python 3.11 or newer is required. The verified reference environment is Python
3.14.2. On Windows, use `py -m venv .venv`, then `.venv\Scripts\python.exe`
instead of `.venv/bin/python`.

Open the whole project in VS Code, enable the Python and Jupyter extensions,
and open `episodes/02_trigrams/episode_02.ipynb`. Select the project's `.venv`
kernel. Read the saved outputs first; then restart the kernel and Run All.
Use Shift+Enter for a slower cell-by-cell walkthrough.

The notebook only imports presentation functions from `visuals.py`; every
model function is printed in full in the notebook. The editable source is `lesson.py`; integration checks verify that its model
functions still match the tested `lab.py`. The builder saves the audit report
after execution without adding that reporting code to the presentation.

## Learn it in three passes

### Pass 1: make the toy model feel obvious (sections 1-5)

You only need ordinary Python lists, tuples, loops, dictionaries, functions,
and a small class. When you reach an unfamiliar construct, connect it to its
purpose:

| Construct | Purpose in this model |
|---|---|
| `yield` | Produce one context/target window at a time |
| Tuple `(a, n)` | Use the whole history as an immutable dictionary key |
| `defaultdict(Counter)` | Create a row when training first observes a context |
| `.get(context, {})` | Read an absent row without inserting it |
| `self` | Access the counts and settings belonging to this model |
| `None` | Mark an entirely unspecified raw probability row |
| `context[1:]` | Drop the oldest token before appending the sampled token |
| `random.Random(seed)` | Keep sampling independent from the split shuffle |

Stop after section 5 and explain these without looking:

- Why do anna and ava provide nine predictions at every context length?
- Why is `P(a | an)` zero but `P(a | vn)` undefined before smoothing?
- Why does add-one give 1/5 for the first query and 1/4 for the second?
- Why can evaluating or generating names leave the training dictionary unchanged?

### Pass 2: understand the experiment (sections 6-10)

Load the same Episode 01 split. Train five separate models on training only.
Use validation to select k for each one. Compare training and validation loss,
then inspect the supporting evidence and first generated samples.

The main chart has both raw training loss and selected-k training loss, clearly
labeled. The second panel holds k fixed. That panel answers whether a change
in smoothing settings alone explains the shape of the comparison.

A singleton means the row's **total count is one**. The unseen-context metric
counts **prediction occurrences**, not unique missing context keys. The two
percentages on the evidence chart have different denominators.

Generation uses the same probability function as evaluation, but generation
samples its history while evaluation uses the supplied real history. The first
12 outputs for each context are shown without filtering. END and CAP distinguish
model termination from the 24-prediction-step limit.

### Pass 3: selection and final reporting (section 11 and the closing recap)

The notebook writes `outputs/frozen_selection.json` before scoring test. It
reports all five fixed configurations but retains the winner chosen by validation.
Do not pick a new winner because of its test score, and do not alter the search
grid after inspecting the final comparison.

This reuses Episode 01's test split, whose bigram result was already reported.
It is excluded from this episode's fitting and selection, but it is not a newly
collected independent test set. Repeat execution verifies fixed-code results;
it does not create a fresh evaluation.

## What to expect

The validation experiment reproduces the existing reference exactly up to
floating-point tolerance. Among the declared choices, three context characters
(a 4-gram) with k = 0.1 has the lowest validation NLL, about 2.126903.

The model called a **trigram uses two context characters**, not three.
The episode starts with trigrams and extends beyond them to measure sparsity.

See [the reference results](README.md#coding-notebook-results) and
[`outputs/coding_results.json`](outputs/coding_results.json) for the complete
final report. These numbers describe this split and plain add-k model family;
they do not rank backoff, interpolation, neural networks, or language models
in general.

## Troubleshooting

- Missing kernel or packages: select the project `.venv` and install the requirements there.
- Dataset/helper missing: open the whole repository, not a detached notebook file.
- NameError: restart and execute cells in order; later cells use earlier definitions.
- Infinity for raw validation: expected when a needed target has zero probability or a row is absent; inspect the separate counters.
- Unknown target: the model rejects it rather than silently dropping that example. Smoothing does not expand the vocabulary.
- Many odd names: do not filter them out to make the model look better; compare held-out loss too.
- Rebuilding: `python3 episodes/02_trigrams/build_notebook.py --execute` regenerates saved outputs and the HTML copy. Without `--execute`, it deliberately clears notebook outputs.
