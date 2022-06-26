"""
Extract common data from the ``daf`` repository.
"""

from __future__ import annotations

from typing import Callable
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from daf import DafReader

__all__ = [
    "tooltips",
    "TooltipsData",
    "TooltipsEntry",
    "TooltipsFunction",
]

#: How to extract a single entry (line) of the tooltip.
#:
#: * If a simple string, this is the name of some property, and the tooltip entry (line) will have the format
#:   ``property: value``.
#:
#: * If a tuple of two strings, they will contain the name of some property and a title to use for it, and the tooltip
#:   entry (line) will have the format ``title: value``.
TooltipsEntry = Union[str, Tuple[str, str]]

#: A function computing the additional tooltip lines for all the objects.
#:
#: This should return a sequence of (optional) strings, one per object. If the value is not ``None``, it will be
#: appended to the object name in the tooltip.
TooltipsFunction = Callable[[DafReader], Sequence[Optional[str]]]

#: How to extract tooltip data from the repository.
#:
#: * If ``None``, the tooltip data is just the name of the object. This is always the 1st line of the tooltip.
#:
#: * If a single `.TooltipsEntry`, then a single line containing that tooltip entry will be added.
#:
#: * If a sequence of `.TooltipsEntry`, then one line will be added to the tooltip for each one.
#:
#: * If a `.TooltipsFunction`, it will be called to get the (optional) tooltip text for each objects, which will
#:   be appended to the object name.
TooltipsData = Union[None, TooltipsEntry, Sequence[TooltipsEntry], TooltipsFunction]


def tooltips(data: DafReader, axis: str, tooltips_data: TooltipsData = None) -> Sequence[str]:
    """
    Compute the ``tooltips_data`` for each entry along some ``axis`` of the ``data``.
    """

    entries = data.axis_entries(axis)
    if tooltips_data is None:
        return entries  # type: ignore

    if callable(tooltips_data):
        return [
            entry if tooltip is None else entry + "\n" + tooltip for entry, tooltip in zip(entries, tooltips_data(data))
        ]

    if isinstance(tooltips_data, (str, tuple)):
        tooltips_data = [tooltips_data]  # type: ignore

    results: Sequence[str] = entries  # type: ignore
    for tooltips_entry in tooltips_data:
        if isinstance(tooltips_entry, str):
            property_name = title = tooltips_entry
        else:
            property_name, title = tooltips_entry
        values = data.get_vector(f"{axis};{property_name}")
        results = [f"{prefix}\n{title}: {value}" for prefix, value in zip(results, values)]
    return results
