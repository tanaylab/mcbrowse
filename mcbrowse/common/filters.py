"""
Allow selecting a subset of the data. This is used for two purposes:

**Filtering**
    For example, suppose we have ``metacell;type`` 1D data assigning a type to each metacell, and we want to include
    just the data of metacells of specific type(s) in the figure.

**Highlighting**
    For example, suppose we have "selected" some metacells we want to focus on, and we'd want the figure to show these
    in a different way (larger size, different shape, etc.

Both operations require us to select a subset of the data. Convenience functions for doing so are provided here.
"""

from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Collection
from typing import Dict
from typing import Optional
from typing import Union

import numpy as np
from daf import Frame
from daf import Series
from daf import Vector
from daf import as_vector
from daf import be_series
from daf import be_vector

__all__ = [
    "VectorFilter",
    "vector_filter_mask",
    "TidyFilter",
    "tidy_filter_mask",
    "tidy_filter_data",
    "matrix_filter_data",
]


#: Describe how to filter a vector of values.
#:
#: This is either a collection of values to keep, or a function that looks at a 1D ``numpy.ndarray`` of values and
#: returns a boolean mask of values to keep.
VectorFilter = Union[Callable[[Vector], bool], Collection[Any]]


def vector_filter_mask(vector: Vector, filter: VectorFilter) -> Vector:  # pylint: disable=redefined-builtin
    """
    Return a 1D ``numpy.ndarray`` boolean mask specifying which elements are kept by ``filter`` in the ``vector``.
    """
    if callable(filter):
        mask = filter(vector)
    else:
        mask = np.isin(vector, filter)
    return be_vector(mask, dtype="bool")


#: Describe how to filter some `tidy data <https://en.wikipedia.org/wiki/Tidy_data>`_ data.
#:
#: The key is either ``|name`` or ``&name`` identifying the data frame column to filter by, and whether to  bitwise-OR
#: or bitwise-AND it into the overall result (see `.tidy_filter_mask`).
TidyFilter = Union[Dict[str, VectorFilter]]


def tidy_filter_mask(
    frame: Frame, filter: Union[TidyFilter, Callable[[Series], bool]]  # pylint: disable=redefined-builtin
) -> Vector:
    """
    Return a boolean 1D ``numpy.ndarray`` mask specifying which rows of the `tidy
    <https://en.wikipedia.org/wiki/Tidy_data>`_ ``frame`` survive the ``filter``.

    Given a ``pandas.DataFrame`` in `tidy data <https://en.wikipedia.org/wiki/Tidy_data>`_ format (that is, each column
    is some variable and each row is an observation)`,

    If the ``filter`` is a dictionary, it species filters to apply independently to each column. The key should start
    with either ``|`` or ``&``; the final mask would bitwise-OR all the column masks that started with ``|``, and then
    bitwise-AND the result with the column masks that started with ``&``.

    If the ``filter`` is a function, it is applied to each row of the frame and the results are collected as the mask.
    """
    if not isinstance(filter, dict):
        return as_vector(be_series(frame.apply(filter, axis=1), dtype="bool"))

    and_mask: Optional[Vector] = None
    or_mask: Optional[Vector] = None

    for name, name_filter in filter.items():
        assert name.startswith("|") or name.startswith("&")
        name_mask = vector_filter_mask(as_vector(frame[name[1:]]), name_filter)

        if name.startswith("|"):
            if or_mask is None:
                or_mask = be_vector(np.zeros(frame.shape[0], dtype="bool"))
            or_mask |= name_mask  # type: ignore
        else:
            if and_mask is None:
                and_mask = be_vector(np.full(frame.shape[0], True, dtype="bool"))
            and_mask &= name_mask  # type: ignore

    if or_mask is None:
        if and_mask is None:
            return be_vector(np.full(frame.shape[0], True, dtype="bool"))
        return and_mask

    if and_mask is None:
        return or_mask
    and_mask &= or_mask  # type: ignore
    return and_mask


def tidy_filter_data(
    frame: Frame, filter: Union[TidyFilter, Callable[[Series], bool]]  # pylint: disable=redefined-builtin
) -> Frame:
    """
    Similar to `.tidy_filter_mask` but return just the rows of the ``frame`` that were kept by the ``filter``.
    """
    return frame.iloc[tidy_filter_mask(frame, filter), :]


def matrix_filter_data(
    frame: Frame, *, rows_filter: Optional[VectorFilter] = None, columns_filter: Optional[VectorFilter] = None
) -> Frame:
    """
    Apply the ``rows_filter`` to the ``frame`` index and the ``columns_filter`` to its columns, and return a new frame
    containing just the rows and columns that were kept by the filter(s).
    """
    if rows_filter is not None:
        rows_mask = vector_filter_mask(as_vector(frame.index), rows_filter)
        frame = frame.iloc[rows_mask, :]

    if columns_filter is not None:
        columns_mask = vector_filter_mask(as_vector(frame.columns), columns_filter)
        frame = frame.iloc[:, columns_mask]

    return frame
