"""
Allow sorting data.

In principle, the order of graph data does not matter. In practice, the implementation(s) will plot graphical elements
in order, so this will control the order of entries in a bar chart, or, for scatter plots, later data will overwrite
earlier data. It is therefore sometimes useful to reorder the data before giving it to the plot function.

.. todo::

    Add functions for clustering and/or ordering 2D data for heatmaps into the `.reorders` module.
"""

from __future__ import annotations

from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
from daf import Frame
from daf import Series
from daf import as_vector
from daf import be_series

__all__ = [
    "tidy_sort_by",
    "tidy_randomize",
]


def tidy_sort_by(frame: Frame, order: Union[Callable[[Series], Any], Sequence[str]]) -> Frame:
    """
    Sort the `tidy <https://en.wikipedia.org/wiki/Tidy_data>`_ ``frame`` rows using the ``order``.

    If the order is a function, we apply it to each frame row and sort the frame by the resulting keys.

    Otherwise, the order is a sequence of ``<name`` or ``>name`` listing the columns to sort by in ascending or
    descending order.
    """
    if callable(order):
        keys = as_vector(be_series(frame.apply(order, axis=1)))
        return frame.iloc[np.argsort(keys), :]

    columns: List[str] = []
    ascending: List[bool] = []
    for name in order:
        assert name.startswith(">") or name.startswith("<")
        columns.append(name[1:])
        ascending.append(name[0] == "<")
    return frame.sort_values(by=columns, ascending=ascending)


def tidy_randomize(frame: Frame, *, random_seed: Optional[int] = None) -> Frame:
    """
    Randomize the order of the `tidy <https://en.wikipedia.org/wiki/Tidy_data>`_ ``frame`` rows.

    If the ``random_seed`` is ``None``, then then the result will not be reproducible.

    .. note::

        Randomization is a quick way to ensure all data subsets get a fair chance to be "on top", based on their size.
    """
    np.random.seed(random_seed)
    indices = np.random.permutation(frame.shape[0])
    return frame.iloc[indices, :]
