"""
pyfifa - A Python easy-to-use wrapper for fetching data from FIFA.com
"""
from .config import *
from .ranking import Ranking, ranking_ids

__all__ = ["Ranking", "ranking_ids"]
__version__ = "0.0.1"
