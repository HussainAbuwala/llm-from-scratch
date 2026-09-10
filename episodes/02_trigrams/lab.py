"""Episode 02 self-study lab. Pure Python; run --toy before --experiment."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import platform
import random

START, END = "<START>", "<END>"
HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "01_names" / "data"
K_VALUES = (0.001, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 100.0)


def windows(name, context_size):
    """Yield (context tuple, target); START is context only, END is scored once."""
    if not isinstance(context_size, int) or context_size < 1:
        raise ValueError("context_size must be a positive integer")
    tokens = [START] * context_size + list(name) + [END]
    for index in range(context_size, len(tokens)):
        yield tuple(tokens[index - context_size:index]), tokens[index]


class CountModel:
    def __init__(self, names, context_size):
        names = list(names)
        if not names or not any(names):
            raise ValueError("Training needs at least one ordinary character")
        # Also validates the context length before constructing a model.
        list(windows("", context_size))
        self.context_size = context_size
        self.outcomes = tuple(sorted(set("".join(names)))) + (END,)
        self.counts = defaultdict(Counter)
        for name in names:
            for context, target in windows(name, context_size):
                self.counts[context][target] += 1
        self.totals = {context: sum(row.values())
                       for context, row in self.counts.items()}

    def probability(self, context, target, k=0.0):
        if not math.isfinite(k) or k < 0:
            raise ValueError("k must be finite and non-negative")
        context = tuple(context)
        if len(context) != self.context_size:
            raise ValueError("Wrong context length")
        if target not in self.outcomes:
            raise ValueError(f"Unknown target: {target}")
        # get() deliberately avoids adding evaluation contexts to the counts.
        count = self.counts.get(context, {}).get(target, 0)
        total = self.totals.get(context, 0)
        if total == 0 and k == 0:
            return None  # 0/0: MLE leaves this entire row unspecified.
        return (count + k) / (total + k * len(self.outcomes))


def evaluate(model, names, k):
    loss = 0.0
    predictions = zero = unseen = 0
    for name in names:
        for context, target in windows(name, model.context_size):
            p = model.probability(context, target, k)
            predictions += 1
            unseen += int(context not in model.totals)
            zero += int(p == 0)
            # Infinity is a failure marker if any row is undefined, not a
            # claim that 0/0 defines a zero-probability distribution.
            loss += -math.log(p) if p is not None and p > 0 else math.inf
    if not predictions:
        raise ValueError("Evaluation needs at least one example")
    return {"nll": loss / predictions, "predictions": predictions,
            "zero_probability_predictions": zero,
            "unseen_context_predictions": unseen}


def generate(model, k, rng, max_steps=24):
    context = (START,) * model.context_size
    letters = []
    for _ in range(max_steps):
        weights = [model.probability(context, token, k) for token in model.outcomes]
        if any(p is None for p in weights):
            raise ValueError("Generation reached an unspecified row; use k > 0")
        target = rng.choices(model.outcomes, weights=weights, k=1)[0]
        if target == END:
            return {"name": "".join(letters), "ended": True}
        letters.append(target)
        context = (*context[1:], target)
    return {"name": "".join(letters), "ended": False}


def toy():
    bigram = CountModel(["anna", "ava"], 1)
    trigram = CountModel(["anna", "ava"], 2)
    print("TRIGRAM TRAINING WINDOWS")
    for name in ("anna", "ava"):
        print(name, list(windows(name, 2)))
    print("\nTRIGRAM COUNTS: context -> {target: count}")
    for context, row in trigram.counts.items():
        print(context, dict(row))
    print("\nUNSMOOTHED COMPLETE NAME PROBABILITIES")
    for name in ("anna", "ava", "ana"):
        for model in (bigram, trigram):
            probabilities = [model.probability(c, t) for c, t in windows(name, model.context_size)]
            print(f"{name:4} context={model.context_size}: {probabilities}; "
                  f"product={math.prod(probabilities)}")
    print("\nSEEN ROW vs UNSEEN ROW")
    print("P(a | a,n), k=0:", trigram.probability(("a", "n"), "a"))
    print("P(a | v,n), k=0:", trigram.probability(("v", "n"), "a"))
    print("P(a | a,n), k=1:", trigram.probability(("a", "n"), "a", 1))
    print("P(a | v,n), k=1:", trigram.probability(("v", "n"), "a", 1))
    print("Smoothed trigram ana:", evaluate(trigram, ["ana"], 1))


def load_splits():
    raw = (DATA / "names.txt").read_bytes()
    provenance = json.loads((DATA / "provenance.json").read_text())
    if hashlib.sha256(raw).hexdigest() != provenance["sha256"]:
        raise ValueError("Dataset checksum mismatch")
    names = sorted(set(raw.decode("utf-8").splitlines()))
    if not all(name and name.isascii() and name.isalpha() and name.islower() for name in names):
        raise ValueError("Expected nonempty lowercase ASCII names")
    random.Random(42).shuffle(names)
    train_end, val_end = int(0.8 * len(names)), int(0.9 * len(names))
    return names[:train_end], names[train_end:val_end], names[val_end:], provenance


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return "infinity"
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def experiment(output=None):
    train, validation, test, provenance = load_splits()
    model_training_names = set(train)
    records = []
    print("Validation experiment: context sizes 1–5; test names are NOT scored.")
    print(" ctx  observed rows  singleton rows   unseen val    best k  train NLL    val NLL")
    for size in range(1, 6):
        model = CountModel(train, size)
        sweep = [{"k": k, **evaluate(model, validation, k)} for k in K_VALUES]
        best = min(sweep, key=lambda result: result["nll"])
        unhandled = evaluate(model, validation, 0)
        train_result = evaluate(model, train, best["k"])
        singleton_rows = sum(total == 1 for total in model.totals.values())
        characters = len(model.outcomes) - 1
        # Valid histories: all-character windows plus START-prefix windows.
        possible_rows = sum(characters ** power for power in range(size + 1))
        rng = random.Random(2026)
        samples = [generate(model, best["k"], rng) for _ in range(12)]
        for sample in samples:
            sample["in_training"] = sample["name"] in model_training_names
        records.append({"context_size": size, "ngram_order": size + 1,
                        "possible_rows": possible_rows,
                        "possible_cells": possible_rows * len(model.outcomes),
                        "observed_rows": len(model.counts),
                        "observed_cells": sum(len(row) for row in model.counts.values()),
                        "singleton_rows": singleton_rows,
                        "unsmoothed_validation": unhandled,
                        "unsmoothed_train": evaluate(model, train, 0),
                        "validation_sweep": sweep, "selected_k": best["k"],
                        "train": train_result, "validation": best,
                        "first_12_samples": samples})
        print(f"{size:4} {len(model.counts):14,} {singleton_rows:15,} "
              f"{unhandled['unseen_context_predictions']:12,} {best['k']:9g} "
              f"{train_result['nll']:10.6f} {best['nll']:10.6f}")
    report = {"purpose": "Self-study validation experiment; test set not scored",
              "dataset_sha256": provenance["sha256"],
              "source_commit": provenance["commit"],
              "python_version": platform.python_version(),
              "split_seed": 42, "sampling_seed": 2026,
              "split_sizes": {"train": len(train), "validation": len(validation), "test": len(test)},
              "metric": "total negative natural log probability / predictions, including one END per name; START padding not scored",
              "k_candidates": list(K_VALUES), "models": records}
    if output:
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(json_safe(report), indent=2, allow_nan=False) + "\n")
        print("Saved", output)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toy", action="store_true")
    parser.add_argument("--experiment", action="store_true")
    parser.add_argument("--output", type=Path, help="Optional JSON evidence file")
    args = parser.parse_args()
    if args.toy or not args.experiment:
        toy()
    if args.experiment:
        experiment(args.output)
