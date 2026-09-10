"""Hand-worked recording examples: evidence, valid contexts, and probability rules."""
import itertools
import unittest

from lab import CountModel, START, END


class RecordingExamples(unittest.TestCase):
    def test_evidence_splits_without_necessarily_changing_prediction(self):
        names = ['anna', 'enna', 'inna', 'onna']
        models = [CountModel(names, size) for size in range(1, 6)]
        for model in models:
            self.assertEqual(sum(model.totals.values()), 20)
        trigram, fourgram = models[1:3]
        self.assertEqual(trigram.counts[('n', 'n')], {'a': 4})
        for initial in 'aeio':
            context = (initial, 'n', 'n')
            self.assertEqual(fourgram.counts[context], {'a': 1})
            self.assertEqual(fourgram.totals[context], 1)
            self.assertEqual(fourgram.probability(context, 'a'), 1)
        self.assertEqual(trigram.probability(('n', 'n'), 'a'), 1)
        # Every longer row uses a subset of its suffix row's observations.
        for short, long in zip(models, models[1:]):
            for context, total in long.totals.items():
                self.assertLessEqual(total, short.totals[context[1:]])

    def test_known_letters_can_form_an_unseen_longer_context(self):
        names = ['anna', 'enna', 'inna', 'onna']
        short, long = CountModel(names, 2), CountModel(names, 3)
        self.assertEqual(set(long.outcomes), set('aeino') | {END})
        self.assertEqual(short.probability(('n', 'n'), 'a'), 1)
        self.assertIsNone(long.probability(('n', 'n', 'n'), 'a'))
        self.assertNotIn(('n', 'n', 'n'), long.counts)
        self.assertEqual(len(long.outcomes), 6)
        for outcome in long.outcomes:
            self.assertAlmostEqual(long.probability(('n', 'n', 'n'), outcome, 1), 1 / 6)

    def test_whole_row_fallback_normalizes_but_keeps_seen_row_zeros(self):
        tri, bi = CountModel(['anna', 'ava'], 2), CountModel(['anna', 'ava'], 1)
        def fallback(context, target):
            p = tri.probability(context, target)
            if p is None:
                p = bi.probability(context[-1:], target)
            return 1 / len(tri.outcomes) if p is None else p
        self.assertEqual([fallback(('v', 'n'), t) for t in tri.outcomes], [0.5, 0.5, 0, 0])
        self.assertEqual(fallback(('a', 'n'), 'a'), 0)
        contexts = [(START, START)] + [(START, c) for c in 'anv'] + list(itertools.product('anv', repeat=2))
        for context in contexts:
            self.assertAlmostEqual(sum(fallback(context, t) for t in tri.outcomes), 1)

    def test_interpolation_arithmetic_and_entire_distribution(self):
        tri, bi = CountModel(['anna', 'ava'], 2), CountModel(['anna', 'ava'], 1)
        mixture = [0.5 * tri.probability(('a', 'n'), t, 1)
                   + 0.5 * bi.probability(('n',), t, 1) for t in tri.outcomes]
        for actual, expected in zip(mixture, [4 / 15, 11 / 30, 11 / 60, 11 / 60]):
            self.assertAlmostEqual(actual, expected)
        self.assertAlmostEqual(sum(mixture), 1)

    def test_valid_start_prefix_capacity(self):
        for size, expected in [(1, 4), (2, 13), (3, 40)]:
            all_slots = itertools.product([START, 'a', 'n', 'v'], repeat=size)
            def valid(context):
                ordinary_seen = False
                for token in context:
                    if token == START and ordinary_seen:
                        return False
                    ordinary_seen |= token != START
                return True
            self.assertEqual(sum(valid(c) for c in all_slots), expected)
        rows = [sum(26 ** power for power in range(m + 1)) for m in range(1, 6)]
        self.assertEqual(rows, [27, 703, 18279, 475255, 12356631])
        self.assertEqual([r * 27 for r in rows], [729, 18981, 493533, 12831885, 333629037])


if __name__ == '__main__':
    unittest.main()
