"""Checks against hand arithmetic and the independent 03A verifier."""
import contextlib
import io
from pathlib import Path
import runpy
import unittest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import verify_theory as theory


class CodingChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            cls.lesson = runpy.run_path(str(Path(__file__).with_name('lesson.py')))

    def test_nine_pairs_and_name_boundaries(self):
        g = self.lesson
        assert_array_equal(np.column_stack([g['x'], g['y']]), theory.pairs(theory.TRAIN))
        self.assertEqual(g['encode']([''], g['row_id'], g['target_id'])[1].tolist(), [3])

    def test_all_three_models_match_theory(self):
        g = self.lesson
        for weights in g['models'].values():
            self.assertAlmostEqual(g['nll'](weights, g['x'], g['y']), theory.evaluate(weights, theory.TRAIN)['nll'])
        values = [g['nll'](w, g['x'], g['y']) for w in g['models'].values()]
        self.assertLess(values[1], values[0])
        self.assertGreater(values[2], values[0])

    def test_loss_weights_predictions_not_names(self):
        g = self.lesson
        w = g['models']['chosen_log2']
        scores = [g['nll'](w, *g['encode']([name], g['row_id'], g['target_id'])) for name in g['TRAIN']]
        self.assertAlmostEqual(g['nll'](w, g['x'], g['y']), (5*scores[0] + 4*scores[1])/9)

    def test_stability_and_normalization(self):
        g = self.lesson
        scores = np.array([[1000, -1000, 0, 0], [0, 1, 2, 3.]])
        assert_allclose(g['softmax'](scores).sum(-1), [1, 1])
        assert_allclose(g['log_softmax'](scores), theory.log_softmax(scores))
        assert_allclose(g['softmax'](scores), g['softmax'](scores + 123))
        self.assertEqual(-g['log_softmax'](scores)[0, 1], 2000)

    def test_sampler_translates_output_to_input_and_marks_end(self):
        g = self.lesson
        w = np.full((4, 4), -1000.)
        w[0, 0] = 0  # START -> a, whose output ID differs from its input ID
        w[1, 3] = 0  # a -> END
        w[2:, 3] = 0
        self.assertEqual(g['generate'](w, g['rows'], g['columns'], number=2),
                         [{'text': 'a', 'ended': True}] * 2)
        self.assertEqual(g['generate'](w, g['rows'], g['columns'], number=1, max_length=1),
                         [{'text': 'a', 'ended': False}])
        w[0] = [-1000, -1000, -1000, 0]
        self.assertEqual(g['generate'](w, g['rows'], g['columns'], number=1),
                         [{'text': '', 'ended': True}])

    def test_notebook_matches_source(self):
        import nbformat
        from build_notebook import make_notebook
        saved = nbformat.read(Path(__file__).with_name('episode_03.ipynb'), as_version=4)
        self.assertEqual([c.source for c in saved.cells], [c.source for c in make_notebook().cells])
        for cell in saved.cells:
            if cell.cell_type == 'code':
                self.assertIsNotNone(cell.execution_count)
                self.assertFalse(any(o.output_type == 'error' for o in cell.outputs))


if __name__ == '__main__':
    unittest.main()
