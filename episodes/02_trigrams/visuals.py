"""Charts for Episode 02B; model training and selection stay visible in the notebook."""
from pathlib import Path
import matplotlib.pyplot as plt

BLUE, ORANGE, PURPLE = '#2563eb', '#ea580c', '#7c3aed'


def setup():
    plt.rcParams.update({'figure.dpi': 130, 'font.size': 11,
                         'axes.titlesize': 14, 'axes.titleweight': 'bold',
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'savefig.facecolor': 'white'})


def finish(fig, directory, name):
    fig.tight_layout()
    fig.savefig(Path(directory) / name, bbox_inches='tight')
    plt.show()
    plt.close(fig)


def plot_losses(records, directory):
    x = [r['context_size'] for r in records]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    for key, label, color, linestyle in [
        ('unsmoothed_train', 'Training: k = 0', '#64748b', '--'),
        ('train', 'Training: selected k', BLUE, '-'),
        ('validation', 'Validation: selected k', ORANGE, '-')]:
        axes[0].plot(x, [r[key]['nll'] for r in records], 'o', linestyle=linestyle,
                     label=label, color=color)
    axes[0].set(title='Fit to training vs. held-out prediction',
                xlabel='Context characters (m)', ylabel='NLL (nats per prediction; lower is better)', xticks=x)
    axes[0].legend(fontsize=9)
    candidates = [r['k'] for r in records[0]['validation_sweep']]
    for k in (0.01, 0.1, 0.3, 1.0):
        index = candidates.index(k)
        axes[1].plot(x, [r['validation_sweep'][index]['nll'] for r in records], 'o-', label=f'k = {k:g}')
    axes[1].set(title='Hold k fixed: does the pattern persist?',
                xlabel='Context characters (m)', ylabel='Validation NLL (nats per prediction)', xticks=x)
    axes[1].legend(fontsize=9)
    for ax in axes:
        ax.grid(alpha=.18)
    finish(fig, directory, 'context_loss.png')


def plot_evidence(records, directory):
    x = [r['context_size'] for r in records]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    singleton_pct = [100*r['singleton_rows']/r['observed_rows'] for r in records]
    unseen_pct = [100*r['validation']['unseen_context_predictions']/r['validation']['predictions'] for r in records]
    for ax, values, title, ylabel, color in [
        (axes[0], singleton_pct, 'How thin is the training evidence?', 'Observed context rows seen once (%)', PURPLE),
        (axes[1], unseen_pct, 'How often is the required row absent?', 'Validation predictions with unseen context (%)', ORANGE)]:
        ax.bar(x, values, color=color, width=.6)
        ax.set(title=title, xlabel='Context characters (m)', ylabel=ylabel, xticks=x,
               ylim=(0, max(values)*1.22+1))
        for a, b in zip(x, values):
            label = f'{b:.2f}%' if 0 < b < .1 else f'{b:.1f}%'
            ax.text(a, b+.5, label, ha='center', va='bottom', fontsize=10)
    finish(fig, directory, 'sparse_evidence.png')


def plot_sweep(records, directory):
    fig, (ax, raw_ax) = plt.subplots(1, 2, figsize=(12, 4.8),
                                   gridspec_kw={'width_ratios': [3, 1]})
    for r in records:
        sweep = [p for p in r['validation_sweep'] if p['k'] > 0]
        ax.plot([p['k'] for p in sweep], [p['nll'] for p in sweep], 'o-',
                label=f"m = {r['context_size']} ({r['ngram_order']}-gram)")
    ax.set(xscale='log', xlabel='Smoothing pseudocount k (log scale)',
           ylabel='Validation NLL (nats per prediction)', title='Positive smoothing candidates')
    ax.legend(fontsize=9); ax.grid(alpha=.18)
    raw_ax.axis('off')
    raw_ax.set_title('k = 0: no smoothing')
    rows = [[f"m = {r['context_size']}",
             f"{r['unsmoothed_validation']['nll']:.6f}"] for r in records]
    raw_ax.table(cellText=rows, colLabels=['Context', 'Val NLL'],
                 cellLoc='center', loc='center')
    raw_ax.text(.5, .12, 'Included in selection.\nZero is shown separately\nfrom the logarithmic axis.\ninf = scoring failure',
                ha='center', va='center', transform=raw_ax.transAxes, fontsize=9)
    finish(fig, directory, 'smoothing_grid.png')
