"""
Test the ``mcbrowse.common.reorders`` module.
"""

import numpy as np
import pandas as pd  # type: ignore

from mcbrowse.common.reorders import *  # pylint: disable=wildcard-import,unused-wildcard-import

# pylint: disable=missing-function-docstring


def test_sort_by_columns() -> None:
    tidy = pd.DataFrame(dict(age=[0, 0, 1, 1], beauty=[0, 1, 0, 1]))
    age_before_beauty = tidy_sort_by(tidy, [">age", "<beauty"])
    assert np.all(age_before_beauty.values == np.array([[1, 0], [1, 1], [0, 0], [0, 1]]))

    quality = tidy_sort_by(tidy, lambda series: (series["age"] + series["beauty"], series["age"], series["beauty"]))
    assert np.all(quality.values == np.array([[0, 0], [0, 1], [1, 0], [1, 1]]))


def test_randomise() -> None:
    tidy = pd.DataFrame(dict(age=[0, 0, 1, 1], beauty=[0, 1, 0, 1]))
    randomized = tidy_randomize(tidy, random_seed=123456)
    assert np.all(randomized.values == np.array([[1, 1], [0, 0], [1, 0], [0, 1]]))
