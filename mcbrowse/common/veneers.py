"""
Common veneer parameters.

Some veneer parameters are also all(most) universal, for example, how to control the figure size, controlling font sizes
of title and/or axes, etc. Well-behaved figures therefore use the types defined here inside their own more detailed
veneer objects.

For simplicity **all** sizes are specified in "points" (72 points to the inch). This is somewhat unnatural for
specifying the overall width and height of figures, but having consistent size for **everything** is a huge
simplification.

.. note::

    The veneers defined here and in ``mcbrowse`` in general and a small subset of what is possible to achieve using
    ``plotly`` or ``ggplot``. They were chosen to provide the 80% of the functionality commonly used in a convenient
    way. If you wish to go beyond this, you can either modify the figure object returned by ``mcbrowse``/``mcbrowse``,
    or plot the data yourself using the full framework interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from daf import Series

__all__ = [
    "FigureVeneer",
    "TooltipsVeneer",
    "DiscreteAxisVeneer",
    "ContinuousAxisVeneer",
    "DiscreteColorScale",
    "PointsVeneer",
    "RegionVeneer",
    "LinesVeneer",
    "ContinuousColorScale",
    "STANDARD_COLORS",
    "color_rgb",
]


@dataclass
class FigureVeneer:
    """
    Common parameters controlling the figure as a whole.

    .. todo::

        Should `.FigureVeneer` provide some sort of "theme" control?
    """

    #: The width of the figure in points. If ``None``, a size will be chosen by the implementation.
    width: Optional[float] = None

    #: The height of the figure in points. If ``None``, a size will be chosen by the implementation.
    height: Optional[float] = None

    #: The height of the overall figure title in points. If ``None``, the title will be hidden.
    title_font_size: Optional[float] = 18


@dataclass
class TooltipsVeneer:
    """
    Common parameters controlling the appearance of tooltips.
    """

    #: The height of the tooltip text font in points. If ``None``, the title will be hidden.
    text_font_size: Optional[float] = 12

    #: The color of the tooltip text. If this is the name of a frame column, this column should contain the fill colors.
    #: Otherwise this should be a color name.
    text_color: str = "black"

    #: The color for filling the tooltip box. If this is the name of a frame column, this column should contain the fill
    #: colors. Otherwise this should be a color name.
    fill_color: str = "white"

    #: The width of the tooltip box border, in points. If this is a string, it is the name of a frame column containing
    #: the border width. If this is ``None``, no border will be drawn.
    border_width: Union[None, float, str] = 1

    #: The color of the tooltip box border. If this is the name of a frame column, this column should contain the border
    #: colors. If ``None``, no border will be drawn.
    border_color: Optional[str] = "black"

    #: The transparency of the point (0 - fully opaque, 1 - fully transparent).
    transparency: float = 0


@dataclass
class DiscreteAxisVeneer:
    """
    Common parameters controlling how a discrete axis is formatted.
    """

    #: The height of the axis title (if any) in points. If ``None``, the title will be hidden.
    title_font_size: Optional[float] = 16

    #: The height of the axis labels (if any) in points. If ``None``, the labels will be hidden.
    label_font_size: Optional[float] = 12


@dataclass
class ContinuousAxisVeneer:
    """
    Common parameters controlling how a continuous axis is formatted.

    Typically a complete figure veneer would have two instances of this, one for the ``x_axis`` and one for the
    ``y_axis``.
    """

    #: The height of the axis title (if any) in points. If ``None``, the title will be hidden.
    title_font_size: Optional[float] = 16

    #: The minimal value to display. If ``None``, the value will be chosen automatically.
    min_value: Optional[float] = None

    #: The maximal value to display. If ``None``, the value will be chosen automatically.
    max_value: Optional[float] = None

    #: The height of the axis tick labels (if any) in points. If ``None``, the tick labels will be hidden.
    label_font_size: Optional[float] = 12

    #: The step(s) for the tick labels. If ``None``, tick labels will be automatic. If this is a number, then this will
    #: be the step between the tick labels. Otherwise, this will be a sequence of tick label positions, or a sequence of
    #: tick positions and the label for each one. An empty sequence will disable the tick labels.
    label_positions: Union[None, float, Sequence[float], Sequence[Tuple[float, str]]] = None

    #: The step(s) for the grid. If ``None``, the grid will be automatic. If this is a number, then this will be the
    #: step between the grid lines. Otherwise, this will be a sequence of grid line positions. An empty sequence will
    #: disable the grid lines.
    grid_positions: Union[None, float, Sequence[float]] = None


#: How to color a discrete value.
#:
#: This is typically fetched from the data repository (e.g., assigning colors to cell types). However logically it is
#: part of the veneer.
DiscreteColorScale = Union[Mapping[Any, str], Series]


@dataclass
class ContinuousColorScale:
    """
    How to color a continuous value.
    """

    #: The height of the legend title (if any) in points. If ``None``, the title will be hidden.
    title_font_size: Optional[float] = 16

    #: The height of the legend labels (if any) in points. If ``None``, the legend labels will be hidden.
    label_font_size: Optional[float] = 12

    #: The positions of the legend labels. If ``None``, the positions will be chosen automatically. If this is a number,
    #: then this will be the step between the labeled breaks. Otherwise, this will be a sequence of labeled legend
    #: positions, or a sequence of legend positions and the label for each one. An empty sequence will disable the
    #: legend labels.
    label_positions: Union[None, float, Sequence[float], Sequence[Tuple[float, str]]] = None

    #: How to map values to colors. If this is a string, it is the name of a color scale. Otherwise, it is a sequence of
    #: monotonically increasing values and colors (either ``#rrggbb`` or a "standard" color name), and will interpolate
    #: between them. Values lower than or higher than the maximum will be clipped to the range covered by this.
    #:
    #: .. note::
    #:
    #:    The names of built-in colors and color scales is different between ``plotly`` and ``ggplot``. We work around
    #:    the former using `.color_rgb` which knows "all" the standard colors, but there's not much we can do about the
    #:    latter.
    #:
    #: If any value is repeated, this creates a discontinuous color scale. For example:
    #:
    #: * ``color=[(1, "magenta"), (1, "white"), (2, "blue")]`` will color all values less than 1 in magenta, values
    #:   between 1 and 2 in a white-blue gradient, and values above 2 in blue.
    #:
    #: * ``color=[(1, "white"), (2, "blue"), (2, "magenta")]`` will color all values less than or equal to 1 in white.
    #:   values between 1 and 2 in a white-blue gradient, and values above 2 in magenta.
    #:
    #: * ``color=[(1, "white"), (2, "blue"), (2, "red"), (3, "green")]`` will color all values less than 1 in white,
    #:   values between 1 and 2 in a white-blue gradient, values between 2 and 3 in a red-green gradient, and values
    #:   above 2 in green.
    #:
    #: * ``color=[(1, "white"), (2, "blue"), (2, "red"), (3, "green")]`` will color all values less than 1 in white,
    #:   values between 1 and 2 in a white-blue gradient, a value of exactly 2 as blue, values between 2 and 3 in a
    #:   red-green gradient, and values above 2 in green.
    #:
    #: * ``color=[(1, "white"), (2, "blue"), (2, "magenta"), (2, "red"), (3, "green")]`` will color all values less than
    #:   1 in white, values between 1 and 2 in a white-blue gradient, a value of exactly 2 as magenta, values between 2
    #:   and 3 in a red-green gradient, and values above 2 in green.
    color: Union[str, Sequence[Tuple[float, str]]] = "viridis"

    #: The minimal value to include, if using a built-in color scale, and not specifying explicit label positions. If
    #: ``None``, the value will be chosen automatically.
    min_value: Optional[float] = None

    #: The maximal value to include, if using a built-in color scale, and not specifying explicit label positions. If
    #: ``None``, the value will be chosen automatically.
    max_value: Optional[float] = None


#: Standard web colors from `Wikipedia <https://en.wikipedia.org/wiki/Web_colors>`_.
#:
#: All names are in lower case.
STANDARD_COLORS = dict(
    aliceblue="#f0f8ff",
    antiquewhite="#faebd7",
    aqua="#00ffff",
    aquamarine="#7fffd4",
    azure="#f0ffff",
    beige="#f5f5dc",
    bisque="#ffe4c4",
    black="#000000",
    blanchedalmond="#ffebcd",
    blue="#0000ff",
    blueviolet="#8a2be2",
    brown="#a52a2a",
    burlywood="#deb887",
    cadetblue="#5f9ea0",
    chartreuse="#7fff00",
    chocolate="#d2691e",
    coral="#ff7f50",
    cornflowerblue="#6495ed",
    cornsilk="#fff8dc",
    crimson="#dc143c",
    cyan="#00ffff",
    darkblue="#00008b",
    darkcyan="#008b8b",
    darkgoldenrod="#b8860b",
    darkgray="#a9a9a9",
    darkgreen="#006400",
    darkkhaki="#bdb76b",
    darkmagenta="#8b008b",
    darkolivegreen="#556b2f",
    darkorange="#ff8c00",
    darkorchid="#9932cc",
    darkred="#8b0000",
    darksalmon="#e9967a",
    darkseagreen="#8fbc8f",
    darkslateblue="#483d8b",
    darkslategray="#2f4f4f",
    darkturquoise="#00ced1",
    darkviolet="#9400d3",
    deeppink="#ff1493",
    deepskyblue="#00bfff",
    dimgray="#696969",
    dodgerblue="#1e90ff",
    firebrick="#b22222",
    floralwhite="#fffaf0",
    forestgreen="#228b22",
    fuchsia="#ff00ff",
    gainsboro="#dcdcdc",
    ghostwhite="#f8f8ff",
    goldenrod="#daa520",
    gold="#ffd700",
    gray="#808080",
    green="#008000",
    greenyellow="#adff2f",
    honeydew="#f0fff0",
    hotpink="#ff69b4",
    indianred="#cd5c5c",
    indigo="#4b0082",
    ivory="#fffff0",
    khaki="#f0e68c",
    lavenderblush="#fff0f5",
    lavender="#e6e6fa",
    lawngreen="#7cfc00",
    lemonchiffon="#fffacd",
    lightblue="#add8e6",
    lightcoral="#f08080",
    lightcyan="#e0ffff",
    lightgoldenrodyellow="#fafad2",
    lightgray="#d3d3d3",
    lightgreen="#90ee90",
    lightpink="#ffb6c1",
    lightsalmon="#ffa07a",
    lightseagreen="#20b2aa",
    lightskyblue="#87cefa",
    lightslategray="#778899",
    lightsteelblue="#b0c4de",
    lightyellow="#ffffe0",
    lime="#00ff00",
    limegreen="#32cd32",
    linen="#faf0e6",
    magenta="#ff00ff",
    maroon="#800000",
    mediumaquamarine="#66cdaa",
    mediumblue="#0000cd",
    mediumorchid="#ba55d3",
    mediumpurple="#9370db",
    mediumseagreen="#3cb371",
    mediumslateblue="#7b68ee",
    mediumspringgreen="#00fa9a",
    mediumturquoise="#48d1cc",
    mediumvioletred="#c71585",
    midnightblue="#191970",
    mintcream="#f5fffa",
    mistyrose="#ffe4e1",
    moccasin="#ffe4b5",
    navajowhite="#ffdead",
    navy="#000080",
    oldlace="#fdf5e6",
    olive="#808000",
    olivedrab="#6b8e23",
    orange="#ffa500",
    orangered="#ff4500",
    orchid="#da70d6",
    palegoldenrod="#eee8aa",
    palegreen="#98fb98",
    paleturquoise="#afeeee",
    palevioletred="#db7093",
    papayawhip="#ffefd5",
    peachpuff="#ffdab9",
    peru="#cd853f",
    pink="#ffc0cb",
    plum="#dda0dd",
    powderblue="#b0e0e6",
    purple="#800080",
    red="#ff0000",
    rosybrown="#bc8f8f",
    royalblue="#4169e1",
    saddlebrown="#8b4513",
    salmon="#fa8072",
    sandybrown="#f4a460",
    seagreen="#2e8b57",
    seashell="#fff5ee",
    sienna="#a0522d",
    silver="#c0c0c0",
    skyblue="#87ceeb",
    slateblue="#6a5acd",
    slategray="#708090",
    snow="#fffafa",
    springgreen="#00ff7f",
    steelblue="#4682b4",
    tan="#d2b48c",
    teal="#008080",
    thistle="#d8bfd8",
    tomato="#ff6347",
    turquoise="#40e0d0",
    violet="#ee82ee",
    wheat="#f5deb3",
    white="#ffffff",
    whitesmoke="#f5f5f5",
    yellow="#ffff00",
    yellowgreen="#9acd32",
)


def color_rgb(color: str) -> str:
    """
    Convert a color name to ``#rrggbb`` (unless it is already in that format).

    This uses the list of `.STANDARD_COLORS` from `Wikipedia <https://en.wikipedia.org/wiki/Web_colors>`_.
    """
    if color.startswith("#"):
        return color
    color = color.lower()
    assert color in STANDARD_COLORS, f"unknown color: {color}"
    return STANDARD_COLORS[color]


@dataclass
class PointsVeneer:
    """
    How to display points (e.g. in a scatter plot or a UMAP 2D projection).
    """

    #: The shape of the point, one of ``circle``, ``square`` or ``diamond``.
    shape: str = "circle"

    #: The size (diameter) of the point, in points. If this is a string, it is the name of a frame column containing the
    #: diameter.
    fill_diameter: Union[float, str] = 6

    #: The color to fill the point with. If this is the name of a frame column, this column should contain the fill
    #: colors. Otherwise this should be a color name.
    fill_color: str = "black"

    #: The width of the border, in points. If this is a string, it is the name of a frame column containing the
    #: border width. If this is ``None``, no border will be drawn.
    #:
    #: .. note::
    #:
    #:    The border width is in addition to the diameter.
    border_width: Union[None, float, str] = 1

    #: The color of the border. If this is the name of a frame column, this column should contain the border colors. If
    #: ``None``, no border will be drawn.
    border_color: Optional[str] = "black"

    #: The transparency of the point (0 - fully opaque, 1 - fully transparent). If this is a string, it is the name of a
    #: frame column containing the transparency.
    transparency: Union[float, str] = 0


@dataclass
class RegionVeneer:
    """
    How to display filled regions (e.g. in a bar plot).
    """

    #: The color to fill the region with. If this is the name of a frame column, this column should contain the fill
    #: colors. Otherwise this should be a color name.
    fill_color: str = "black"

    #: The width of the border, in points. If this is a string, it is the name of a frame column containing the
    #: border width. If this is ``None``, no border will be drawn.
    border_width: Union[None, float, str] = 1

    #: The color of the border. If this is the name of a frame column, this column should contain the border colors. If
    #: ``None``, no border will be drawn.
    border_color: Optional[str] = "black"


@dataclass
class LinesVeneer:
    """
    How to display lines (e.g. edges of the KNN graph in a UMAP projection).
    """

    #: The width of the line, in points. If this is a string, it is the name of a frame column containing the
    #: border width. If this is ``None``, no lines will be drawn.
    width: Union[None, float, str] = 1

    #: The color of the line. If this is the name of a frame column, this column should contain the border colors. If
    #: ``None``, no lines will be drawn.
    color: Optional[str] = "black"

    #: The transparency of the lines (0 - fully opaque, 1 - fully transparent). If this is a string, it is the name of a
    #: frame column containing the transparency.
    transparency: Union[float, str] = 0
