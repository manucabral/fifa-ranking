"""
pyfifa - A Python easy-to-use wrapper for fetching data from FIFA.com
"""

import sys
import platform

from .constants import absolute_path
from .utilities import exist_file, create_directory
from .ranking import Ranking, ranking_ids

if sys.version_info < (3, 8):
    raise ImportError("Python 3.8 or higher is required.")
del sys

if platform.system() != "Windows":
    raise ImportError("pyfifa only works on Windows.")
del platform

cache_file = absolute_path("cache")
if not exist_file(cache_file):
    create_directory(cache_file)
del cache_file

__all__ = ["Ranking", "ranking_ids"]
__version__ = "0.0.1"
