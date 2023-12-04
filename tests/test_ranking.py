"""
Test the Ranking stuff.
"""

import os
import unittest
from pyfifa import Ranking, ranking_ids
from pyfifa.ranking import FifaRankingId, RankingItem, FifaRankingId


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
        ranking = Ranking()
        self.assertIsInstance(ranking, Ranking, msg="Should be a Ranking.")

    def test_ranking_items(self):
        """> Should return a list of RankingItem's (men and women)."""
        ranking = Ranking()
        self.assertIsInstance(ranking.items(), list, msg="Should be a list.")
        self.assertIsInstance(
            ranking.items()[0], RankingItem, msg="Should be a RankingItem."
        )

    def test_ranking_csv_export(self):
        """> Should export a CSV file."""
        filename = "ranking.csv"
        ranking = Ranking()
        ranking.export(extension="csv", filename=filename)
        self.assertTrue(os.path.isfile(filename), msg="Should be exported.")
        with open(filename, "r") as csv_file:
            self.assertTrue(csv_file.readable(), msg="Should be readable.")
        os.remove(filename)

    def test_ranking_json_export(self):
        """> Should export a JSON file."""
        filename = "ranking.json"
        ranking = Ranking()
        ranking.export(extension="json", filename=filename)
        self.assertTrue(os.path.isfile(filename), msg="Should be exported.")
        with open(filename, "r") as json_file:
            self.assertTrue(json_file.readable(), msg="Should be readable.")
        os.remove(filename)

    def test_ranking_limit(self):
        """> Should return a Ranking object with a limit."""
        ranking = Ranking(limit=10)
        self.assertIsInstance(ranking, Ranking, msg="Should be a Ranking.")
        self.assertEqual(len(ranking.items()), 10, msg="Should be 10 items.")

    def test_ranking_id(self):
        """> Should check if the default ranking id is a FifaRankingId."""
        ranking = Ranking()
        self.assertIsInstance(
            ranking.id_, FifaRankingId, msg="Should be a FifaRankingId."
        )
