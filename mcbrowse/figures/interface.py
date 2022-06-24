"""
The common interface implemented by all figures.

In general, each figure defines the following:

* A `.FigureFilter` object that describes how to collect the data.

* A `.FigureData` object that contains the collected data.

* A `.FigureVeneer` object that defines how to format the figure.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Generic
from typing import Optional
from typing import Sequence
from typing import TypeVar
from typing import Union

import numpy as np
from daf import DafReader
from daf import Frame
from daf import Series
from plotly.basedatatypes import BaseFigure  # type: ignore

from ..common import TidyFilter
from ..common import VectorFilter
from ..common import tidy_filter_data
from ..common import tidy_filter_mask
from ..common import tidy_randomize
from ..common import tidy_sort_by

__all__ = ["FigureFilter", "FigureData", "TidyFigureData", "HeatmapData", "FigureVeneer"]


class FigureData(ABC):
    """
    Contain the data to be included in the figure.

    .. note::

        This applies to most figures, but not to heatmaps.
    """

    @abstractmethod
    def filter(
        self,
        filter: Union[TidyFilter, Callable[[Series], bool]],  # pylint: disable=redefined-builtin
    ) -> None:
        """
        Filter the contained data using `.tidy_filter_data`.

        .. note::

            To filter the rows or columns of a heatmap, specify a `.TidyFilter` that filters the rows or columns axis
            used by the figure.
        """

    @abstractmethod
    def highlight(
        self,
        filter: Union[TidyFilter, Callable[[Series], bool]],  # pylint: disable=redefined-builtin
    ) -> None:
        """
        Mark everything matching the ``filter`` as "highlighted" using `.tidy_filter_mask`. This will trigger using a
        different veneer for the highlighted data (the details will depend on the specific figure).

        Figures are expected to plot the normal data first and the highlighted data later ("on top" of the normal data).

        .. note::

            This can only be called once.
        """

    @abstractmethod
    def sort(self, order: Union[Callable[[Series], Any], Sequence[str]]) -> None:
        """
        Sort the contained data using `.tidy_sort_by`.

        Figures are expected to plot the normal data first and the highlighted data later ("on top" of the normal data),
        but will use the sort ``order`` within each category.
        """

    @abstractmethod
    def randomize(self, random_seed: Optional[int]) -> None:
        """
        Randomize the contained data using `.tidy_randomize`.

        Figures are expected to plot the normal data first and the highlighted data later ("on top" of the normal data),
        but will randomize the order within each group.
        """


class HeatmapData(ABC):  # pylint: disable=too-few-public-methods
    """
    Contain the heatmap data to be included in the figure.

    .. todo::

        Add clustering control and clustering-preserving sorting to `.HeatmapData`.

    .. todo::

        Create a SimpleHeatmapData implementation that keeps both a 2D matrix and a frame of annotations
        for the rows and the columns.
    """

    @abstractmethod
    def filter(
        self, *, rows_filter: Optional[VectorFilter] = None, columns_filter: Optional[VectorFilter] = None
    ) -> None:
        """
        Filter the contained data using `.matrix_filter_data`.
        """


#: Any data used to generate a figure.
AnyData = Union[FigureData, HeatmapData]

#: A type variable for any data used to generate a figure.
AnyDataT = TypeVar("AnyDataT", bound=AnyData)


class TidyFigureData(FigureData):
    """
    Implement `.FigureData` for the very common case of a tidy ``pandas.DataFrame``.
    """

    def __init__(self, tidy: Frame) -> None:
        #: The tidy data frame containing the figures data.
        #:
        #: If we are highlighting, this will only contain the "normal" (non-highlighted) data.
        #:
        #: If all the data is highlighted, this will be ``None``.
        self.tidy: Optional[Frame] = tidy

        #: If we are highlighting, this will only contain the highlighted data.
        self.highlighted: Optional[Frame] = None

    def filter(
        self,
        filter: Union[TidyFilter, Callable[[Series], bool]],  # pylint: disable=redefined-builtin
    ) -> None:
        if self.tidy is not None:
            self.tidy = tidy_filter_data(self.tidy, filter)
            if self.tidy.shape[0] == 0:
                self.tidy = None

        if self.highlighted is not None:
            self.highlighted = tidy_filter_data(self.highlighted, filter)
            if self.highlighted.shape[0] == 0:
                self.highlighted = None

    def highlight(
        self,
        filter: Union[TidyFilter, Callable[[Series], bool]],  # pylint: disable=redefined-builtin
    ) -> None:
        assert self.highlighted is None, "repeated calls to FigureData.highlight"
        assert self.tidy is not None

        highlighted_mask = tidy_filter_mask(self.tidy, filter)
        if not np.any(highlighted_mask):
            return

        if np.all(highlighted_mask):
            self.highlighted = self.tidy
            self.tidy = None
            return

        self.highlighted = self.tidy.iloc[highlighted_mask, :]
        self.tidy = self.tidy.iloc[~highlighted_mask, :]

    def sort(self, order: Union[Callable[[Series], Any], Sequence[str]]) -> None:
        if self.tidy is not None:
            self.tidy = tidy_sort_by(self.tidy, order)
        if self.highlighted is not None:
            self.highlighted = tidy_sort_by(self.highlighted, order)

    def randomize(self, random_seed: Optional[int] = None) -> None:
        if self.tidy is not None:
            self.tidy = tidy_randomize(self.tidy, random_seed=random_seed)
        if self.highlighted is not None:
            self.highlighted = tidy_randomize(self.highlighted, random_seed=random_seed)


class FigureFilter(ABC, Generic[AnyDataT]):  # pylint: disable=too-few-public-methods
    """
    Control how to extract the figure data from the ``daf`` repository.
    """

    @abstractmethod
    def collect(self, data: DafReader) -> AnyDataT:
        """
        Collect the matching `.FigureData` out of the ``data``.
        """


class FigureVeneer(ABC, Generic[AnyDataT]):  # pylint: disable=too-few-public-methods
    """
    Contain the parameters controlling the figure's appearance.
    """

    @abstractmethod
    def plot(self, data: AnyDataT) -> BaseFigure:
        """
        Generate the ``plotly`` figure using the specified ``data``.
        """
