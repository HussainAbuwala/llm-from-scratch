# %% [markdown]
# # From counts to weights — in NumPy
# **Episode 03B · Building an LLM From Scratch**
#
# Published 03A gave us a prediction function and a loss. Now implement each step.
# Route: pairs → scores → probabilities → target loss → chosen changes → samples.
# We are evaluating adjustable weights, not yet learning an update rule.
# Run every cell in order. Python loops, indexing, probabilities and logs are prerequisites;
# NumPy arrays and broadcasting are introduced as we need them.
# NumPy is our bridge from Python loops to numerical arrays in Episodes 3–4.
# The tiny model could use ordinary Python; arrays let us process examples together.
# NumPy does not supply our model or an automatic training rule.
# Printed arrays below expose its indexing and broadcasting before we use them.

# %%
from pathlib import Path
import hashlib
import json
import random
import numpy as np

np.set_printoptions(precision=4, suppress=True)
START, END = '<START>', '<END>'
TRAIN = ['anna', 'ava']

# %% [markdown]
# ## 1 · Give each token a table address
# Inputs are START plus characters. Outputs are characters plus END.
# The two index maps have different meanings: a sampled output ID is not an input ID.

# %%
def vocabulary(names):
    characters = sorted(set(''.join(names)))
    if not characters:
        raise ValueError('Need at least one character in the training vocabulary')
    rows, columns = [START] + characters, characters + [END]
    return rows, columns, {s: i for i, s in enumerate(rows)}, {s: i for i, s in enumerate(columns)}

rows, columns, row_id, target_id = vocabulary(TRAIN)
print('Input rows:', rows)
print('Output columns:', columns)
print('Input address map:', row_id)
print('Target address map:', target_id)
print('a input ID:', row_id['a'], '| a output ID:', target_id['a'])

# %% [markdown]
# ## 2 · Make all nine prediction targets
# Reset to START for each name; include END once per name. The data supplies the
# previous character during evaluation. There is no transition between names.

# %%
def encode(names, row_id, target_id):
    inputs, targets = [], []
    for name in names:
        previous = START
        for token in [*name, END]:
            inputs.append(row_id[previous])
            targets.append(target_id[token])
            previous = token
    if not inputs:
        raise ValueError('Need at least one name to score')
    return np.array(inputs, dtype=np.int64), np.array(targets, dtype=np.int64)

x, y = encode(TRAIN, row_id, target_id)
print('x — input row IDs:', x, '| shape:', x.shape)
print('y — target column IDs:', y, '| shape:', y.shape)
for current, target in zip(x, y):
    print(f'{rows[current]:>7} → {columns[target]}')
print('Predictions:', len(y))
assert len(y) == 9

# %% [markdown]
# ## 3 · Look up scores directly
# W has one row per input and one column per possible output. `W[x]` gathers a
# score row for every prediction: (4, 4) becomes (9, 4).
# Zero initialization is an inspectable choice for independent bigram rows,
# not a general initialization recommendation for neural networks.
# **NumPy indexing:** `W[x]` selects multiple rows, including repeats, in x's order.
# Its loop equivalent is `np.array([W[i] for i in x])`.
# W still has only 16 parameters; the nine gathered rows are not new parameters.

# %%
W = np.zeros((len(rows), len(columns)), dtype=np.float64)
scores = W[x]
print('Stored W, shape', W.shape, ':\n', W)
print('Requested row IDs x:', x)
print('Gathered scores W[x], shape', scores.shape, ':\n', scores)

# %% [markdown]
# ## 4 · Turn each row into probabilities
# Subtract the row maximum, exponentiate, and divide by the row sum.
# `axis=-1` means output columns; `keepdims=True` preserves a column dimension
# so NumPy broadcasts each row's denominator across that row.
# A shared score shift does not change the normalized probabilities.

# %%
def softmax(scores):
    scores = np.asarray(scores, dtype=np.float64)
    shifted = scores - scores.max(axis=-1, keepdims=True)
    masses = np.exp(shifted)
    return masses / masses.sum(axis=-1, keepdims=True)

# Expose the same calculation outside the helper for the presentation.
row_maxima = scores.max(axis=-1, keepdims=True)
shifted_scores = scores - row_maxima
masses = np.exp(shifted_scores)
row_totals = masses.sum(axis=-1, keepdims=True)
print('Row maxima, shape', row_maxima.shape, ':\n', row_maxima)
print('Shifted scores = scores - row maxima:\n', shifted_scores)
print('Exponentiated scores:\n', masses)
print('Row totals, shape', row_totals.shape, ':\n', row_totals)
probabilities = softmax(scores)
print('Probabilities = masses / row totals:\n', probabilities)
print('Probability row sums:', probabilities.sum(axis=-1))
assert np.allclose(probabilities.sum(axis=-1), 1)

# %% [markdown]
# ### Optional NumPy close-up: make broadcasting visible
# Our zero rows all look alike. These two illustrative rows show that NumPy
# subtracts a DIFFERENT maximum for each row. This demo does not change W.

# %%
demo_scores = np.array([[2., 3., 1., 5.], [0., 0., 0., np.log(2)]])
demo_maxima = demo_scores.max(axis=-1, keepdims=True)
print('Demo scores (2, 4):\n', demo_scores)
print('Max without keepdims (2,):', demo_scores.max(axis=-1))
print('Max with keepdims (2, 1):\n', demo_maxima)
print('Subtract each row maximum from its four entries:\n', demo_scores - demo_maxima)
print('Demo probabilities:\n', softmax(demo_scores))

# %% [markdown]
# ## 5 · Select the actual target, then average surprise
# The two index arrays select one target probability per prediction, not an
# entire column. The denominator is nine character-or-END predictions.
# We use natural logs: the unit is nats per prediction.
# **NumPy paired indexing:** the first array gives example rows; y gives target
# columns. NumPy selects (row[0], y[0]), (row[1], y[1]), and so on.
# Loop equivalent: `[probabilities[i, target] for i, target in enumerate(y)]`.

# %%
example_rows = np.arange(len(y))
print('np.arange(len(y)) — example row IDs:', example_rows)
print('y — target column IDs:              ', y)
print('Paired (example row, target column):', list(zip(example_rows.tolist(), y.tolist())))
selected = probabilities[example_rows, y]
print('Selected target probabilities, shape', selected.shape, ':', selected)
losses = -np.log(selected)
print('Per-target losses = -np.log(selected):', losses)
for current, target, probability, loss in zip(x, y, selected, losses):
    print(f'{rows[current]:>7} → {columns[target]:<5} p={probability:.4f} loss={loss:.6f}')
print(f'Total: {losses.sum():.6f} / {len(y)} = {losses.mean():.6f} nats/prediction')
assert np.isclose(losses.mean(), np.log(4))

# %% [markdown]
# ## 6 · Compute log probabilities without an underflow trap
# Stable softmax avoids ordinary exponential overflow, but tiny probabilities
# can still round to zero. Computing log-softmax directly preserves their loss.
# This is the same NLL objective as before; it is also categorical cross-entropy
# for the observed target. No target one-hot vector is necessary.

# %%
def log_softmax(scores):
    scores = np.asarray(scores, dtype=np.float64)
    if scores.ndim == 0 or scores.shape[-1] == 0 or not np.isfinite(scores).all():
        raise ValueError('Expected finite scores and at least one output')
    shifted = scores - scores.max(axis=-1, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=-1, keepdims=True))


def nll(weights, inputs, targets):
    if len(targets) == 0:
        raise ValueError('Need at least one prediction')
    log_p = log_softmax(weights[inputs])
    return float(-log_p[np.arange(len(targets)), targets].mean())

# %% [markdown]
# ### A · Softmax, then log: the target probability rounds to zero
# A separate numerical demonstration: W is unchanged. Suppose output index 1
# (the second output) is correct. Our existing softmax subtracts the maximum,
# preventing overflow, but this target's probability still underflows.

# %%
extreme = np.array([1000., -1000., 0., 0.])
demo_target = 1
extreme_shifted = extreme - extreme.max()
extreme_masses = np.exp(extreme_shifted)
extreme_probabilities = softmax(extreme)
print('A — SOFTMAX, THEN LOG')
print('Scores:', extreme)
print('Correct target index:', demo_target, '(second output)')
print('Shifted scores:', extreme_shifted)
print('Exponentials (tiny values round to zero):', extreme_masses)
print('Sum of exponentials:', extreme_masses.sum())
print('Probabilities:', extreme_probabilities)
print('Selected target probability:', extreme_probabilities[demo_target])
# Suppress only the expected log(0) warning; keep and display the infinite result.
with np.errstate(divide='ignore'):
    ordinary_log_probability = np.log(extreme_probabilities[demo_target])
print('log(target probability):', ordinary_log_probability)
print('Final loss = -log(target probability):', -ordinary_log_probability)

# %% [markdown]
# ### B · Log-softmax: keep the target score and get a finite loss
# Same scores and target. Compute shifted score minus log(sum of exponentials).
# The denominator still rounds to 1, but the target score -2000 is preserved.
# At least one shifted score is zero, so the denominator contains exp(0) = 1.
# This returns LOG probabilities directly; loss still needs the negative sign.

# %%
extreme_log_probabilities = log_softmax(extreme)
log_denominator = np.log(extreme_masses.sum())
print('B — LOG-SOFTMAX DIRECTLY')
print('Scores:', extreme)
print('Shifted scores:', extreme_shifted)
print('Sum of exponentials:', extreme_masses.sum())
print('Log of that sum:', log_denominator)
print('Log probabilities = shifted scores - log(sum):', extreme_log_probabilities)
print('Selected target log probability:', extreme_log_probabilities[demo_target])
print('Final loss = -target log probability:', -extreme_log_probabilities[demo_target])
print('Our unchanged model loss:', nll(W, x, y))
assert np.isclose(nll(W, x, y), losses.mean())

# %% [markdown]
# ## 7 · A helpful change, then an overshoot
# Predict before running: does making END more likely always improve the model?
# These are hand-chosen settings from 03A, not optimizer steps. Each model is
# scored on the same two training names and all nine targets.

# %%
models = {}
for label, mass in [('initial', 1), ('chosen_log2', 2), ('overshoot_log100', 100)]:
    weights = W.copy()
    weights[row_id['a'], target_id[END]] = np.log(mass)
    models[label] = weights
    print(f'{label:>16}: a row = {softmax(weights[row_id["a"]])}; NLL = {nll(weights, x, y):.6f}')

# %% [markdown]
# END follows a twice, but n and v also follow a. Increasing END's score reduces
# their probabilities. The full loss falls from 1.386294 to 1.331437, then rises
# to 1.806672. The other input rows remain unchanged: no shared representation
# or longer context has appeared. Choosing updates systematically is Episode 04.

# %% [markdown]
# ## 8 · Generate: samples now supply the next input
# Start at START, sample an output, translate its token back to an input row,
# and repeat. END stops generation. Empty outputs are possible. A length cap
# is a safety stop and is labeled separately from a sampled END.

# %%
def generate(weights, rows, columns, seed=7, number=12, max_length=20):
    if max_length < 1:
        raise ValueError('max_length must be positive')
    rng = np.random.default_rng(seed)
    input_id = {token: i for i, token in enumerate(rows)}
    distributions = softmax(weights)
    samples = []
    for _ in range(number):
        current, characters, ended = START, [], False
        for _ in range(max_length):
            output = int(rng.choice(len(columns), p=distributions[input_id[current]]))
            token = columns[output]
            if token == END:
                ended = True
                break
            characters.append(token)
            current = token
        samples.append({'text': ''.join(characters), 'ended': ended})
    return samples

for label, weights in models.items():
    print('\n', label)
    for sample in generate(weights, rows, columns):
        print(repr(sample['text']), 'END' if sample['ended'] else 'CAP')

# %% [markdown]
# ## 10 · What we built, and the next question
# We can look up scores, normalize them, evaluate target loss, and generate.
# A chosen change can help or hurt; a different representation alone does not
# improve the count model. Next: how does a small weight change affect the loss?
# Episode 04 introduces derivatives, the chain rule, and gradient descent.
