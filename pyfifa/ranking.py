"""
Provides the ranking class and the ranking ids function to get all the ranking ids.

Example:
    >>> import pyfifa
    >>> last = pyfifa.ranking_ids()[0]
    >>> ranking = pyfifa.Ranking(ranking_id=last)
"""

import json
import typing
from datetime import datetime
from .constants import ENDPOINTS, CACHE
from .utilities import get, extract_xpath, exist_file, load_pickle, save_pickle


class FifaRankingId:
    """
    Represents a FIFA ranking id (supports men and women ranking).
    """

    __slots__ = ("__value", "__date")

    def __init__(self, value: str, date: str):
        """
        Args:
            value (str): The value of the id (format: "id123").
            date (str): The date of the id (format: "%d %b %Y").
        """
        self.__value = value
        date = date.replace("Sept", "Sep")
        self.__date = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")

    @property
    def value(self) -> str:
        """
        Returns:
            str: The id value of the ranking.
        """
        return self.__value

    @property
    def date(self) -> str:
        """
        Returns:
            str: The date of the ranking id.
        """
        return self.__date

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation of the ranking id.
        """
        return f"FifaRankingId(date={self.__date})"


class Ranking:
    """
    Represents a FIFA ranking.

    Attributes:
        ranking_id (FifaRankingId): The id of the ranking.
        lang (str): The language of the ranking.
    """

    def __init__(self, ranking_id: FifaRankingId, lang: str = "en", **kwargs):
        """
        Args:
            ranking_id (FifaRankingId): The id of the ranking.
            lang (str, optional): The language of the ranking. Defaults to "en".
        """
        self.__id = ranking_id
        self.__lang = lang
        path = CACHE.FIFA_RANKING(ranking_id=ranking_id.value, lang=lang)
        if exist_file(path):
            self.__data = load_pickle(path)
        else:
            self.__data = self.__get_data(**kwargs)
            save_pickle(path, self.__data)

    def __get_data(self, **kwargs) -> dict:
        """
        Returns the ranking data.

        Returns:
            dict: The ranking data.
        """
        response = get(
            ENDPOINTS.RANKING.API.format(lang=self.__lang, id=self.__id.value)
        )
        if not response:
            raise RuntimeError("Failed to get the ranking data.")
        data = json.loads(response)
        if not data:
            raise RuntimeError("Failed to extract the ranking data.")
        return data

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation of the ranking.
        """
        return f"Ranking(id={self.__id}, lang={self.__lang})"


def ranking_ids(
    genre: typing.Literal["men", "women"] = "men"
) -> typing.List[FifaRankingId]:
    """
    Gets all the ranking ids of the given genre.

    Args:
        genre (str): The genre of the ranking ('men' or 'women').

    Returns:
        list[FifaRankingId]: The ranking ids.
    """
    if genre not in ["men", "women"]:
        raise ValueError("Invalid genre.")
    cache_path = CACHE.FIFA_RANKING_ID(genre=genre)
    if exist_file(cache_path):
        return load_pickle(cache_path)
    response = get(ENDPOINTS.RANKING.HTML.format(genre=genre))
    if not response:
        raise RuntimeError("Failed to get the ranking ids.")
    xpath_data = extract_xpath(response, '//script[contains(., "dates")]/text()')
    if not xpath_data:
        raise RuntimeError("Failed to extract the ranking ids.")
    data = json.loads(xpath_data.pop())["props"]["pageProps"]["pageData"]
    ids = [
        FifaRankingId(value=d["id"], date=d["text"]) for d in data["ranking"]["dates"]
    ]
    save_pickle(cache_path, ids)
    del xpath_data, data
    return ids
