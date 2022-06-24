"""
Test the ``mcbrowse.common.veneers`` module.
"""

from mcbrowse.common.veneers import *  # pylint: disable=wildcard-import,unused-wildcard-import

# pylint: disable=missing-function-docstring


def test_color_rgb() -> None:
    assert color_rgb("black") == "#000000"
    assert color_rgb("#010203") == "#010203"
