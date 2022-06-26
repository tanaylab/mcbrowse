"""
Generic utilities used by multiple figures.

In general, each figure can define its own data and veneer objects as it sees fit. However, there are some common
concepts used by all(most) figures, which are provided here.
"""

from .data import *
from .filters import *
from .reorders import *
from .veneers import *
