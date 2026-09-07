"""Presentation helpers. No model training, sampling, or scoring lives here."""

import math
from pathlib import Path

import matplotlib.pyplot as plt

BLUE = "#2563eb"
ORANGE = "#ea580c"


def style():
    plt.rcParams.update({
        "figure.figsize": (10, 4.5), "figure.dpi": 130,
        "font.size": 12, "axes.titlesize": 16, "axes.titleweight": "bold",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.labelcolor": "#334155", "text.color": "#0f172a",
        "axes.edgecolor": "#cbd5e1", "savefig.facecolor": "white",
    })


def finish(fig, output_dir, filename):
    fig.tight_layout()
    fig.savefig(Path(output_dir) / filename, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def plot_lengths(names, output_dir):
    fig, ax = plt.subplots()
    lengths = [len(name) for name in names]
    ax.hist(lengths, bins=[n - 0.5 for n in range(1, max(lengths) + 2)],
            color=BLUE, edgecolor="white")
    ax.set(title="Our data: one spelling per example", xlabel="Characters per name",
           ylabel="Number of names")
    finish(fig, output_dir, "name_lengths.png")


def print_table(matrix, rows, columns, decimals=None):
    width = 9
    print("current \\ next".ljust(16) + "".join(str(c).rjust(width) for c in columns))
    for token, values in zip(rows, matrix):
        cells = [str(x) if decimals is None else f"{x:.{decimals}f}" for x in values]
        print(token.ljust(16) + "".join(x.rjust(width) for x in cells))


def plot_counts(counts, rows, columns, output_dir):
    fig, ax = plt.subplots(figsize=(10, 8))
    values = [[math.log1p(value) for value in row] for row in counts]
    im = ax.imshow(values, cmap="Blues", aspect="equal")
    ax.set_xticks(range(len(columns)), columns, rotation=90, fontsize=9)
    ax.set_yticks(range(len(rows)), rows, fontsize=9)
    ax.set(title="The entire model starts here: transition counts",
           xlabel="Next token", ylabel="Current token")
    fig.colorbar(im, ax=ax, shrink=0.7, label="log(1 + count), for display only")
    finish(fig, output_dir, "transition_counts.png")


def plot_row(probabilities, row_id, next_tokens, current, output_dir):
    values = probabilities[row_id[current]]
    fig, ax = plt.subplots()
    ax.bar(next_tokens, values, color=[ORANGE if t == "<END>" else BLUE for t in next_tokens])
    ax.tick_params(axis="x", labelrotation=60)
    ax.set(title=f"After {current!r}, what comes next?", xlabel="Next token", ylabel="Probability")
    finish(fig, output_dir, "next_character.png")


def plot_sweep(results, output_dir):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, subset, title in [(axes[0], results, "The full experiment"),
                              (axes[1], [r for r in results if r["k"] <= 3], "A closer look · k ≤ 3")]:
        for key, label, color in [("train_nll", "Training", BLUE), ("validation_nll", "Validation", ORANGE)]:
            finite = [r for r in subset if math.isfinite(r[key])]
            ax.plot([r["k"] for r in finite], [r[key] for r in finite], "o-", label=label, color=color)
        ax.set_xscale("symlog", linthresh=0.01)
        ax.set(title=title, xlabel="Pseudo-count k", ylabel="Average NLL · nats per prediction")
        ax.ticklabel_format(axis="y", useOffset=False)
        ax.legend(loc="lower right")
        ax.grid(alpha=0.15)
    if not math.isfinite(results[0]["validation_nll"]):
        axes[0].text(0.03, 0.95, "k = 0: validation NLL = ∞\n(not plotted)",
                     transform=axes[0].transAxes, va="top", color=ORANGE, fontsize=11)
    best = min(results, key=lambda r: r["validation_nll"])
    axes[1].annotate(f"Best tested k = {best['k']:g}", xy=(best["k"], best["validation_nll"]),
                     xytext=(0.4, 0.82), textcoords="axes fraction", color=ORANGE,
                     arrowprops={"arrowstyle": "->", "color": ORANGE}, fontsize=11)
    fig.text(0.5, -0.01, "Same measurements, different y-axis ranges. x-axis: linear near zero; logarithmic beyond 0.01.",
             ha="center", fontsize=10, color="#475569")
    finish(fig, output_dir, "smoothing.png")
