"""
The top-level ``mcbrowse`` module re-exports everything all the sub-modules, so, for example, you can write ``from
mcbrowse import GeneGeneData`` or ``mcbrowse.GeneGeneData`` instead of the full name
``mcbrowse.gene_gene.GeneGeneData``.
"""

# See https://github.com/jwilk/python-syntax-errors
# pylint: disable=using-constant-test,missing-function-docstring,pointless-statement
if 0:

    async def function(value):
        f"{await value}"  # Python >= 3.7 is required


__author__ = "Oren Ben-Kiki"
__email__ = "oren@ben-kiki.org"
__version__ = "0.1.0-dev.1"

# pylint: disable=wrong-import-position

import sys

from .common import *
