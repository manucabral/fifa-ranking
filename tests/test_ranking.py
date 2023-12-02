"""
Test the Ranking stuff.
"""

import unittest
from pyfifa import Ranking, ranking_ids
from pyfifa.ranking import FifaRankingId


class TestRanking(unittest.TestCase):
    """
    Test the Ranking stuff.
    """

    def test_men_ranking_ids(self):
        """> Should return a list of men FifaRankingId's."""
        men_ids = ranking_ids(genre="men")
        last_id = men_ids[0]
        self.assertIsInstance(men_ids, list, msg="Should be a list.")
        self.assertIsInstance(last_id, FifaRankingId, msg="Should be a FifaRankingId.")

    def test_women_ranking_ids(self):
        """> Shoud return a list of women FifaRankingId's."""
        women_ids = ranking_ids(genre="women")
        last_id = women_ids[0]
        self.assertIsInstance(women_ids, list, msg="Should be a list.")
        self.assertIsInstance(last_id, FifaRankingId, msg="Should be a FifaRankingId.")

    def test_men_ranking(self):
        """> Should return a Ranking object."""
        last_id = ranking_ids()[0]
        ranking = Ranking(ranking_id=last_id)
        self.assertIsInstance(ranking, Ranking, msg="Should be a Ranking.")
