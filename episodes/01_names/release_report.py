"""Save build results outside the viewer's teaching cells."""

import json
import math
import sys


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return "infinity"
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def save_report(namespace):
    n = namespace
    report = {
        "dataset_sha256": n["provenance"]["sha256"],
        "source_commit": n["provenance"]["commit"],
        "python_version": sys.version.split()[0],
        "split_seed": 42, "sampling_seed": 2026,
        "split_sizes": {key: len(n[variable]) for key, variable in
                        [("train", "train_names"), ("validation", "validation_names"), ("test", "test_names")]},
        "ordinary_characters": len(n["next_tokens"]) - 1,
        "outcomes": n["outcomes"],
        "metric": "total negative natural log probability / all predictions, including END",
        "toy": {"ana_probability": n["path_probability"], "ana_nll": n["toy_score"]["nll"]},
        "validation_baselines": n["validation_baselines"],
        "sweep": n["sweep"], "selected_k": n["best_k"],
        "test": n["test_results"], "samples": n["samples"],
        "greedy": {"name": n["greedy_name"], "ended": n["greedy_ended"]},
    }
    (n["OUTPUT"] / "results.json").write_text(
        json.dumps(json_safe(report), indent=2, allow_nan=False) + "\n"
    )
