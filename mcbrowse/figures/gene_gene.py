"""
A gene-gene scatter figure.

This figure is the workhorse of annotating metacells with "cell types". It shows which combinations of the two genes
exist, gradients between different states, and how all these match the current type annotation.
"""

from dataclasses import dataclass
from typing import NewType
from typing import Optional
from typing import Union

import pandas as pd  # type: ignore
from daf import DafReader
from plotly.basedatatypes import BaseFigure  # type: ignore

from ..common import ContinuousAxisVeneer
from ..common import ContinuousColorScale
from ..common import DiscreteAxisVeneer
from ..common import PointsVeneer
from ..common import TooltipsData
from ..common import TooltipsVeneer
from ..common import tooltips
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

    #: How to compute a tooltip for each metacell.
    metacell_tooltip: TooltipsData = None

    def collect(self, data: DafReader) -> GeneGeneData:
        x_gene_fractions = data.get_vector(f"metacell,gene={self.x_gene_name};fraction")
        y_gene_fractions = data.get_vector(f"metacell,gene={self.y_gene_name};fraction")

        metacell_names = data.axis_entries("metacell")
        metacell_values = data.get_vector("metacell;" + self.metacell_value)
        metacell_tooltips = tooltips(data, "metacell", self.metacell_tooltip)

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
