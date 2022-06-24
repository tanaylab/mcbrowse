"""
Test the ``mcbrowse.common.filters`` module.
"""

import numpy as np
import pandas as pd  # type: ignore
from daf import be_vector

from mcbrowse.common.filters import *  # pylint: disable=wildcard-import,unused-wildcard-import

# pylint: disable=missing-function-docstring


def test_vector_filter_mask() -> None:
    data = be_vector(np.array([0, 1, 2, 3]))
    assert np.all(vector_filter_mask(data, lambda values: values % 2 == 0) == np.array([True, False, True, False]))
    assert np.all(vector_filter_mask(data, [1, 2]) == np.array([False, True, True, False]))


def test_tidy_filter_mask() -> None:
    tidy = pd.DataFrame(dict(age=[0, 0, 1, 1], beauty=[0, 1, 0, 1]))
    mask = tidy_filter_mask(tidy, lambda series: series["age"] == series["beauty"])
    assert np.all(mask == np.array([True, False, False, True]))

    mask = tidy_filter_mask(tidy, {"|age": [0], "&beauty": [1]})
    assert np.all(mask == np.array([False, True, False, False]))

    mask = tidy_filter_mask(tidy, {"&age": [0], "&beauty": [1]})
    assert np.all(mask == np.array([False, True, False, False]))

    mask = tidy_filter_mask(tidy, {"|age": [0], "|beauty": [1]})
    assert np.all(mask == np.array([True, True, False, True]))

    mask = tidy_filter_mask(tidy, {})
    assert np.all(mask == np.array([True, True, True, True]))


def test_tidy_filter_data() -> None:
    tidy = pd.DataFrame(dict(age=[0, 0, 1, 1], beauty=[0, 1, 0, 1]))
    filtered = tidy_filter_data(tidy, lambda series: series["age"] == series["beauty"])
    assert np.all(filtered.values == np.array([[0, 0], [1, 1]]))

    filtered = tidy_filter_data(tidy, {"|age": [0], "&beauty": [1]})
    assert np.all(filtered.values == np.array([[0, 1]]))

    filtered = tidy_filter_data(tidy, {"&age": [0], "&beauty": [1]})
    assert np.all(filtered.values == np.array([[0, 1]]))

    filtered = tidy_filter_data(tidy, {"|age": [0], "|beauty": [1]})
    assert np.all(filtered.values == np.array([[0, 0], [0, 1], [1, 1]]))

    filtered = tidy_filter_data(tidy, {})
    assert np.all(filtered.values == np.array([[0, 0], [0, 1], [1, 0], [1, 1]]))


def test_matrix_filter_data() -> None:
    matrix = pd.DataFrame([[0, 1, 2], [3, 4, 5], [5, 6, 7]], index=["a", "b", "c"], columns=["x", "y", "z"])
    filtered = matrix_filter_data(matrix, rows_filter=["a", "b"], columns_filter=["x", "z"])
    assert np.all(filtered.values == np.array([[0, 2], [3, 5]]))
