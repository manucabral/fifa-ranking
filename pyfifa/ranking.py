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


class Flag:
    """
    Represents a flag.
    """

    __slots__ = ("__src", "__title")

    def __init__(self, src: str, title: str):
        """
        Args:
            src (str): The source of the flag (url).
            title (str): The title of the flag (country name).
        """
        self.__src = src
        self.__title = title

    @property
    def src(self) -> str:
        """
        Returns:
            str: The source of the flag (url).
        """
        return self.__src

    @property
    def title(self) -> str:
        """
        Returns:
            str: The title of the flag (country name).
        """
        return self.__title

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation of the flag.
        """
        return f"Flag(title={self.__title})"

    def __repr__(self) -> str:
        """
        Returns:
            str: The representation of the flag.
        """
        return str(self)


class RankingItem:
    """
    Represents a ranking item (team).
    """

    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: The ranking item data (see the attributes below).

        Attributes:
            rank (int): The rank of the team.
            name (str): The name of the team.
            total_points (int): The total points of the team.
            previous_points (int): The previous points of the team.
            country_code (str): The country code of the team.
            confederation (str): The confederation of the team (e.g. "UEFA")
            flag (Flag): The flag of the team.
        """
        self.__rank = kwargs.get("rank", 0)
        self.__name = kwargs.get("name", "Unknown")
        self.__total_points = kwargs.get("totalPoints", 0)
        self.__previous_points = kwargs.get("previousPoints", 0)
        self.__country_code = kwargs.get("countryCode", "Unknown")
        self.__confederation = kwargs.get("confederation", "Unknown")
        self.__flag = Flag(
            src=kwargs["flag"]["src"],
            title=kwargs["flag"]["title"],
        )

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation of the ranking item.
        """
        return f"RankingItem({self.__dict__})"

    def __repr__(self) -> str:
        """
        Returns:
            str: The representation of the ranking item.
        """
        return str(self)

    @property
    def rank(self) -> int:
        """
        Returns:
            int: The rank of the team.
        """
        return self.__rank

    @property
    def name(self) -> str:
        """
        Returns:
            str: The name of the team.
        """
        return self.__name

    @property
    def total_points(self) -> int:
        """
        Returns:
            int: The total points of the team.
        """
        return self.__total_points

    @property
    def previous_points(self) -> int:
        """
        Returns:
            int: The previous points of the team.
        """
        return self.__previous_points

    @property
    def country_code(self) -> str:
        """
        Returns:
            str: The country code of the team.
        """
        return self.__country_code

    @property
    def confederation(self) -> str:
        """
        Returns:
            str: The confederation of the team (e.g. "UEFA")
        """
        return self.__confederation

    @property
    def flag(self) -> Flag:
        """
        Returns:
            Flag: The flag of the team.
        """
        return self.__flag


class Ranking:
    """
    Represents a FIFA ranking.

    Attributes:
        ranking_id (FifaRankingId): The id of the ranking.
        lang (str): The language of the ranking.

    Other Attributes:
        limit (int): The limit of the ranking items (teams).
        data (dict): The crude ranking data.

    """

    def __init__(self, ranking_id: FifaRankingId, lang: str = "en", **kwargs):
        """
        Args:
            ranking_id (FifaRankingId): The id of the ranking.
            lang (str, optional): The language of the ranking. Defaults to "en".
        """
        self.__id = ranking_id
        self.__lang = lang
        self.__limit = kwargs.get("limit", None)
        path = CACHE.FIFA_RANKING(ranking_id=ranking_id.value, lang=lang)
        if exist_file(path):
            self.__data = load_pickle(path)
        else:
            self.__data = self.__get_data(**kwargs)
            save_pickle(path, self.__data)

    def __get_data(self) -> dict:
        """
        Gets the ranking data from the API and returns it.

        Returns:
            dict: The ranking data.
        """
        response = get(
            ENDPOINTS.RANKING.API.format(lang=self.__lang, id=self.__id.value)
        )
        print(
            "making response to ",
            ENDPOINTS.RANKING.API.format(lang=self.__lang, id=self.__id.value),
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

    def __repr__(self) -> str:
        """
        Returns:
            str: The representation of the ranking.
        """
        return str(self)

    def items(self) -> typing.List[RankingItem]:
        """
        Returns the ranking items (teams).

        Returns:
            list[RankingItem]: The ranking items.
        """
        return [
            RankingItem(
                **item["rankingItem"],
                previousPoints=item["previousPoints"],
                confederation=item["tag"]["id"],
            )
            for item in self.__data["rankings"][: self.__limit]
        ]


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
