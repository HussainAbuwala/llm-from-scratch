"""NumPy arithmetic companion for Episode 03A; no optimizer or test-set fitting."""
import json
import numpy as np

INPUTS = ("START", "a", "n", "v")
OUTPUTS = ("a", "n", "v", "END")
TRAIN = ("anna", "ava")


def pairs(names):
    result = []
    for name in names:
        previous = "START"
        for target in (*name, "END"):
            result.append((INPUTS.index(previous), OUTPUTS.index(target)))
            previous = target
    return np.asarray(result, dtype=np.int64).reshape(-1, 2)


def log_softmax(logits):
    """Normalize along the last (outcome) axis, retaining batch dimensions."""
    logits = np.asarray(logits, dtype=np.float64)
    if logits.ndim == 0 or logits.shape[-1] == 0 or not np.isfinite(logits).all():
        raise ValueError("Expected finite logits with a nonempty outcome axis")
    shifted = logits - logits.max(axis=-1, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=-1, keepdims=True))


def evaluate(weights, names):
    transitions = pairs(names)
    if not len(transitions):
        raise ValueError("At least one name is required")
    weights = np.asarray(weights, dtype=np.float64)
    if weights.shape != (4, 4):
        raise ValueError("This toy uses four input rows and four output columns")
    logits = weights[transitions[:, 0]]  # direct row lookup for each input
    log_p = log_softmax(logits)
    losses = -log_p[np.arange(len(transitions)), transitions[:, 1]]
    return {"nll": float(losses.mean()), "predictions": len(losses)}


def counts():
    table = np.zeros((4, 4), dtype=np.int64)
    transitions = pairs(TRAIN)
    np.add.at(table, (transitions[:, 0], transitions[:, 1]), 1)
    return table


def report():
    result = {"training_names": TRAIN, "input_order": INPUTS,
              "output_order": OUTPUTS, "counts": counts().tolist(),
              "unit": "nats per character or END prediction", "models": {}}
    for label, mass in (("zero_logits", 1), ("a_end_log2", 2), ("a_end_log100", 100)):
        weights = np.zeros((4, 4))
        weights[1, 3] = np.log(mass)
        result["models"][label] = {
            "a_probabilities": np.exp(log_softmax(weights[1])).tolist(),
            "a_end_loss": float(-log_softmax(weights[1])[3]),
            "training": evaluate(weights, TRAIN),
        }
    weights = np.log(counts() + 1)
    result["constructed_add_one"] = {
        "probabilities": np.exp(log_softmax(weights)).tolist(),
        "ana": evaluate(weights, ["ana"]),
        "ana_probability": float(np.exp(-evaluate(weights, ["ana"])["nll"] * 4)),
        "method": "Constructed from training counts, not optimized",
    }
    return result


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
