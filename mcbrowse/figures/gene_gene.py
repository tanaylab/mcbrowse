"""
A gene-gene scatter figure.

This figure is the workhorse of annotating metacells with "cell types". It shows which combinations of the two genes
exist, gradients between different states, and how all these match the current type annotation.
"""

from dataclasses import dataclass
from typing import Callable
from typing import NewType
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import pandas as pd  # type: ignore
from daf import DafReader
from plotly.basedatatypes import BaseFigure  # type: ignore

from ..common import ContinuousAxisVeneer
from ..common import ContinuousColorScale
from ..common import DiscreteAxisVeneer
from ..common import PointsVeneer
from ..common import TooltipsVeneer
from .interface import FigureFilter
from .interface import FigureVeneer
from .interface import TidyFigureData

__all__ = ["GeneGeneFilter", "GeneGeneData", "GeneGeneVeneer"]

#: Contain the data for a gene-gene figure.
#:
#: It will contain the columns: ``x_gene_fraction``, ``y_gene_fraction``, ``metacell_value`` and ``metacell_tooltip``.
GeneGeneData = NewType("GeneGeneData", TidyFigureData)


@dataclass
class GeneGeneFilter(FigureFilter[GeneGeneData]):
    """
    Collect the data for a gene-gene figure.
    """

    #: The name of the gene to use for the X axis.
    #:
    #: This is stored in a column called ``x_gene_fractions`` in the collected data frame.
    x_gene_name: str

    #: The name of the gene to use for the Y axis.
    #:
    #: This is stored in a column called ``y_gene_fractions`` in the collected data frame.
    y_gene_name: str

    #: The value to assign a value to each metacell (for coloring).
    #:
    #: This is stored in a column called ``metacell_value`` in the collected data frame. It should be the name of some
    #: 1D data associated with each metacell in the ``daf`` data, that is, ``type`` will be used to access the
    #: ``metacell;type`` 1D data.
    #:
    #: Converting the values to colors is done in the `.GeneGeneVeneer`.
    metacell_value: str = "type"

    #: The value to place in the tooltip for each metacell.
    #:
    #: This is stored in a column called ``metacell_tooltip`` in the collected data frame. If ``None``, the metacell
    #: names are used as tooltips. If this is a string, it is the name of some additional 1D data associated with each
    #: metacell. If it is a sequence of strings, then lists the names of multiple such data (each will be shown in its
    #: own line), and optionally give a nicer name to each one. If this is a function, it should take the ``daf`` data
    #: as input and return a sequence of strings, one per metacell.
    metacell_tooltip: Union[
        None, str, Sequence[Union[str, Tuple[str, str]]], Callable[[DafReader], Sequence[str]]
    ] = None

    def collect(self, data: DafReader) -> GeneGeneData:
        x_gene_index = data.axis_index("gene", self.x_gene_name)
        y_gene_index = data.axis_index("gene", self.y_gene_name)

        gene_metacell_fractions = data.get_matrix("gene,metacell;fraction")
        x_gene_fractions = gene_metacell_fractions[x_gene_index, :]
        y_gene_fractions = gene_metacell_fractions[y_gene_index, :]

        metacell_names = data.axis_entries("metacell")
        metacell_values = data.get_vector("metacell;" + self.metacell_value)
        metacell_tooltips: Sequence[str]
        if self.metacell_tooltip is None:
            metacell_tooltips = metacell_names  # type: ignore
        elif callable(self.metacell_tooltip):
            metacell_tooltips = self.metacell_tooltip(data)
        else:
            properties: Sequence[Union[str, Tuple[str, str]]]
            if isinstance(self.metacell_tooltip, str):
                properties = [self.metacell_tooltip]
            else:
                properties = self.metacell_tooltip

            metacell_tooltips = metacell_names  # type: ignore
            for property_data in properties:
                if isinstance(property_data, str):
                    property_title = property_data
                    property_name = property_data
                else:
                    property_name, property_title = property_data
                metacell_tooltips = [
                    f"{tooltip}\n{property_title}: {value}"
                    for tooltip, value in zip(metacell_tooltips, data.get_vector("metacell;" + property_name))
                ]

        return GeneGeneData(
            pd.DataFrame(
                dict(
                    x_gene_fraction=x_gene_fractions,
                    y_gene_fraction=y_gene_fractions,
                    metacell_value=metacell_values,
                    metacell_tooltip=metacell_tooltips,
                ),
                index=metacell_names,
            )
        )


class GeneGeneVeneer(FigureVeneer[GeneGeneData]):  # pylint: disable=too-few-public-methods
    """
    Control the appearance of a gene-gene figure.
    """

    #: The overall figure parameters.
    figure: Optional[FigureVeneer] = None

    #: Control the X axis.
    x_axis: Optional[ContinuousAxisVeneer] = None

    #: Control the Y axis.
    y_axis: Optional[ContinuousAxisVeneer] = None

    #: Control the point appearance.
    points: Optional[PointsVeneer] = None

    #: Control the appearance of highlighted points.
    highlighted_points: Optional[PointsVeneer] = None

    #: Control the appearance of the tooltips.
    tooltips: Optional[TooltipsVeneer]

    #: How to color the metacells.
    colors: Union[DiscreteAxisVeneer, ContinuousColorScale]

    def plot(self, data: GeneGeneData) -> BaseFigure:
        assert False, "not implemented"
