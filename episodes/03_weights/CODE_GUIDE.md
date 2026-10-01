# Episode 03B · Start here

03A is published (confirmed by the presenter September 30, 2026). This is its
NumPy coding companion. Open `episode_03.ipynb`, select the project `.venv`
Python kernel, and run from the top. `episode_03.html` is the executed reading copy.

From the repository root:

```sh
.venv/bin/python episodes/03_weights/lesson.py
.venv/bin/python episodes/03_weights/build_notebook.py --execute
.venv/bin/python -m unittest discover -s episodes/03_weights -p 'test_*.py' -v
```

For a new environment, create a virtual environment and install
`episodes/03_weights/requirements-coding.txt`. The lesson itself only needs NumPy;
the remaining packages build and execute the notebook. No dataset download is needed.
The notebook supports a working directory at the repository root or episode folder.

## Learning route

1. Trace the separate input and output maps and all nine targets.
2. Inspect `W[x]`: one selected score row per target.
3. Follow row-wise softmax and target selection before reading the NLL helper.
4. Compare ordinary log-of-probability against direct log-softmax under underflow.
5. Predict the effect of each chosen weight change before executing it.
6. Trace the sampler's conversion from an output token to its input row.
7. Review the closing connection to derivatives and gradients.

The three toy losses are **1.386294**, **1.331437**, and **1.806672** nats per
prediction, averaged over the same nine character-or-END targets in anna/ava.
These are training-example demonstrations, not generalization measurements.

The recorded episode stays with anna/ava. The optional larger-data extension
was removed by the presenter. The preserved notebook retains generation code
for further exploration, although the recording closes after the weight comparison.

The presenter-edited `episode_03.ipynb` is the authoritative recording notebook.
Its source has been synchronized back into `lesson.py` (percent-cell format).
Before rebuilding, preserve any new notebook edits and synchronize them back
into the source; the builder overwrites the notebook and its outputs.
The existing 03A presenter guide remains the theory script. Use
`CODING_PRESENTER_GUIDE.md` for this video. References and scope decisions are in
`../../EPISODE_03_THEORY.md`; coding exercises are in `CODING_EXERCISES.md`.
