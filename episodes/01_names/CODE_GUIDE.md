# EP 01B · Build a language model in Python

This is the short companion to the coding video. The [notebook](episode_01.ipynb)
contains the full lesson, runnable code, charts, and reference outputs.
For the mathematics, use the existing [theory handout](../../docs/episode-01-theory.pdf).

## Run the code

Clone or download the **whole repository**, so the notebook can find `data/` and
`visuals.py`. Use Python 3.11 or newer; the reference run used 3.14.2.

```bash
git clone https://github.com/HussainAbuwala/llm-from-scratch.git
cd llm-from-scratch
python3 -m venv .venv
.venv/bin/python -m pip install -r episodes/01_names/requirements.txt
```

On Windows, use `py -m venv .venv` and `.venv\Scripts\python.exe` in place of
`.venv/bin/python` for subsequent commands.

Open the repository folder in VS Code. Install the Microsoft **Python** and
**Jupyter** extensions. Open `episodes/01_names/episode_01.ipynb`, select the
project `.venv` under **Select Kernel → Python Environments**, then restart the
kernel and choose **Run All**. To learn step by step, execute cells from the top
using Shift+Enter. The saved outputs can also be read directly on GitHub.

## What each function does

| Function | What to follow in the code |
|---|---|
| `make_vocabulary` | Learn the training letters and create separate row/column index maps. |
| `transitions` | Add START and END, then form adjacent token pairs. |
| `count_bigrams` | Add one tally for every training transition. |
| `normalize` | Divide each cell by its own row total. |
| `generate` | Select from the current row, append the token, and repeat until END or the cap. |
| `evaluate` | Score the supplied next tokens with −ln(p), then average over predictions. |
| `smooth` | Add k to each allowed cell and normalize a new table. |

The model uses standard-library Python. Jupyter displays the lesson and
Matplotlib draws charts. Chart colors use log(1 + count) for readability;
the model's count table still contains the original integers.

## Reference experiment

The bundled file has 32,033 lines. Deduplication leaves 29,494 spellings,
split with seed 42 into 23,595 training, 2,949 validation, and 2,950 test names.
There are 26 letters and 27 allowed next outcomes including END. Every spelling
has equal weight; these are not population-frequency-weighted name counts.

Training uses 169,134 transitions. A name with L characters contributes L + 1
predictions, including the final END. Each row is a conditional distribution:

```text
P(target | current) = (count + k) / (row total + 27 × k)
```

The best tested smoothing value is **k = 0.3**, chosen using validation only.
All final test scores use the same 21,053 predictions:

| Model | Test NLL, nats per prediction |
|---|---:|
| Uniform | 3.295837 |
| Unigram | 2.818510 |
| Smoothed bigram | 2.460499 |

## Questions that come up while following along

**Why isn't training NLL zero?** The same character can have several observed
successors. One shared row cannot assign probability 1 to each of them.

**Why is unsmoothed validation NLL infinite?** Eight validation prediction
occurrences have probability zero. Smoothing gives unseen pairs of known
characters some probability. It cannot represent an unknown character.

**How does weighted sampling work?** Imagine dividing an interval into regions
whose lengths are the probabilities. A uniform random position selects a
region. Python's `random.choices` performs this using cumulative weights.
Larger regions are selected more often, without guaranteeing exact counts
in a small sample. Seed 2026 makes the sequence reproducible in the reference run.

**Why can outputs have one letter or be too long?** The model only knows its
current character. It does not track name length or remember a complete spelling.
`END` means the model stopped; `CAP` means the code stopped generation at 24 letters.

**Why 1.040 on the theory canvas but 1.154 in section 9?** Both use add-one
smoothing, but 1.040 scores `ana` and 1.154 scores `avna`. The former shows the
cost of reallocating probability; the latter shows repair of unseen `v → n`.

## Troubleshooting and exploration

- **No kernels listed:** install/enable VS Code's Python and Jupyter extensions.
- **Missing package:** select the project `.venv`, and install the requirements there.
- **A name is not defined:** restart and run cells in order; later cells use earlier definitions.
- **Dataset/helper not found:** open the whole repository, not a detached notebook download.
- **GitHub doesn't render the notebook:** download the repository and open it locally.

Try a different sampling seed, inspect another character's probability row, or
compare samples with k = 0.01 and k = 100. Use training and validation for
exploration; reserve test scores for a settled comparison.

The published notebook matches the recorded scope: 100 samples in each sample
batch, with the extra loop demo and per-name score analysis omitted. It ends at
the final test comparison. The build tool saves `outputs/results.json` separately.

[Dataset provenance and license](data/README.md) · [Developer setup and tests](README.md)
