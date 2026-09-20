"""Integration checks for the committed, executed teaching artifact (stdlib only)."""
import inspect
import json
import math
from pathlib import Path
import unittest
import lab

HERE = Path(__file__).resolve().parent


class CodingNotebookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads((HERE / 'episode_02.ipynb').read_text())
        cls.report = json.loads((HERE / 'outputs/coding_results.json').read_text())

    def test_visible_core_is_the_tested_implementation(self):
        sources = [''.join(c['source']).strip() for c in self.notebook['cells'] if c['cell_type'] == 'code']
        for fn in [lab.windows, lab.CountModel, lab.evaluate, lab.generate, lab.load_splits]:
            self.assertIn(inspect.getsource(fn).strip(), sources)

    def test_saved_notebook_is_fully_executed_without_errors(self):
        count = 0
        for cell in self.notebook['cells']:
            source = ''.join(cell['source'])
            self.assertFalse(any(ord(c) < 32 and c not in '\n\t' for c in source))
            if cell['cell_type'] == 'code':
                count += 1
                self.assertEqual(cell['execution_count'], count)
                compile(source, '<notebook>', 'exec')
                self.assertFalse(any(o['output_type'] == 'error' for o in cell['outputs']))
        self.assertGreater(count, 0)

    def test_validation_reference_and_episode_one_continuity(self):
        earlier = json.loads((HERE / 'outputs/study_results.json').read_text())
        self.assertEqual(self.report['dataset_sha256'], earlier['dataset_sha256'])
        self.assertEqual(self.report['split_sizes'], earlier['split_sizes'])
        for a, b in zip(self.report['models'], earlier['models'], strict=True):
            for key in ['context_size', 'selected_k', 'observed_rows', 'singleton_rows']:
                self.assertEqual(a[key], b[key])
            positive = [r for r in a['validation_sweep'] if r['k'] > 0]
            raw = a['validation_sweep'][0]
            self.assertEqual(raw['k'], 0)
            self.assertEqual(raw['nll'], a['unsmoothed_validation']['nll'])
            self.assertGreater(raw['zero_probability_predictions'] + raw['unseen_context_predictions'], 0)
            for x, y in zip(positive, b['validation_sweep'], strict=True):
                self.assertEqual(x['k'], y['k'])
                self.assertEqual(x['predictions'], 21141)
                self.assertAlmostEqual(x['nll'], y['nll'], places=12)
        self.assertAlmostEqual(self.report['test']['1']['nll'], 2.460499355213333, places=10)
        for result in self.report['test'].values():
            self.assertEqual(result['predictions'], 21053)
            self.assertTrue(math.isfinite(result['nll']))
            self.assertEqual(result['zero_probability_predictions'], 0)

    def test_frozen_selection_comes_from_validation(self):
        frozen = json.loads((HERE / 'outputs/frozen_selection.json').read_text())
        self.assertEqual(frozen, self.report['frozen_selection'])
        for r in self.report['models']:
            best = min(r['validation_sweep'], key=lambda x: float(x['nll']))
            key = str(r['context_size'])
            self.assertEqual(frozen['selected_k_by_context'][key], best['k'])
            self.assertEqual(self.report['test'][key]['k'], best['k'])
            self.assertEqual(len(self.report['first_12_samples'][key]), 12)
        winner = min(self.report['models'], key=lambda r: r['validation']['nll'])
        self.assertEqual(frozen['chosen_context'], winner['context_size'])
        self.assertEqual(frozen['chosen_k'], winner['selected_k'])


if __name__ == '__main__':
    unittest.main()
