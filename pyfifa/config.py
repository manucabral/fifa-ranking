"""
This module contains the configuration of pyfifa.
"""

import sys
import platform
from .constants import absolute_path
from .utilities import create_directory, exist_file

if sys.version_info < (3, 8):
    raise ImportError("Python 3.8 or higher is required.")
del sys

if platform.system() != "Windows":
    raise ImportError("pyfifa only works on Windows.")
del platform

cache_file = absolute_path("cache")
if not exist_file(cache_file):
    create_directory(cache_file)

del cache_file, create_directory, exist_file, absolute_path
