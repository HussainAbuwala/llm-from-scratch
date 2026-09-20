"""Save evidence after notebook execution; kept off the recording screen."""
import json
from lab import json_safe


def save_report(ns):
    report = {
        'purpose': 'Episode 02B fixed-grid count-model comparison; test reported after validation selection',
        'python_version': ns['platform'].python_version(),
        'dataset_sha256': ns['provenance']['sha256'], 'source_commit': ns['provenance']['commit'],
        'split_seed': 42, 'sampling_seed': 2026,
        'split_sizes': {'train': len(ns['train_names']), 'validation': len(ns['validation_names']), 'test': len(ns['test_names'])},
        'metric': 'total negative natural log probability / predictions, including END; START not scored',
        'frozen_selection': ns['frozen'], 'models': ns['records'],
        'first_12_samples': ns['sample_batches'], 'test': ns['test_results'],
        'uniform_test_nll': ns['math'].log(len(ns['models'][1].outcomes)),
        'test_set_note': 'same held-out split previously reported in Episode 01; not a new independent dataset',
    }
    (ns['OUTPUT'] / 'coding_results.json').write_text(json.dumps(json_safe(report), indent=2, allow_nan=False)+'\n')
