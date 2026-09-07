# Names dataset

Bundled from [karpathy/makemore](https://github.com/karpathy/makemore), commit
`988aa59e4d8fefa526d06f3b453ad116258398d4`.

- [Exact names file](https://github.com/karpathy/makemore/blob/988aa59e4d8fefa526d06f3b453ad116258398d4/names.txt)
- [Upstream README and attribution](https://github.com/karpathy/makemore/blob/988aa59e4d8fefa526d06f3b453ad116258398d4/README.md)
- [Upstream MIT license](https://github.com/karpathy/makemore/blob/988aa59e4d8fefa526d06f3b453ad116258398d4/LICENSE), preserved in `LICENSE.makemore`

The upstream README attributes the names to US Social Security data for 2018.
This lesson uses the upstream text file, not a new extraction from SSA.
The lesson's implementation and narration were written for this repository.

The bytes are unchanged: 32,033 lines, 228,145 bytes. `provenance.json` records
the SHA-256 checksum, and the notebook checks it before loading the data.
No network download is needed to run the notebook after installing dependencies.

Preprocessing validates nonempty lowercase ASCII alphabetic names, sorts unique
spellings, then shuffles with `random.Random(42)`. Removing 2,539 repeated
spellings leaves 29,494 examples. Each unique spelling has equal weight; the
experiment does not model how frequently people receive a name.

The fixed 80/10/10 split yields 23,595 training, 2,949 validation, and 2,950 test
names. It is not adjusted in response to evaluation results. The training
vocabulary contains 26 letters, with no unknown held-out characters. Names are
split as whole examples, and duplicate spellings cannot cross split boundaries.

This finite list represents particular source and preprocessing choices. It is
not a comprehensive collection of names, languages, or naming traditions.
