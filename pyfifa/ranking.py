"""
Provides the ranking class and the ranking ids function to get all the ranking ids.

Example:
    >>> import pyfifa
    >>> ranking = pyfifa.Ranking()
    >>> ranking
    Ranking(id=FifaRankingId(date=2021-04-07), lang=en,  limit=None)
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
            date (str): The date of the id (format: ISO).
        """
        self.__value = value
        self.__date = date

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
        ranking_id (FifaRankingId): The id of the ranking, defaults to the last ranking id.
        lang (str): The language of the ranking, defaults to "en".

    Other Attributes:
        limit (int): The limit of the ranking items (teams) to get, defaults to None (all).

    """

    __slots__ = ("__id", "__lang", "__limit", "__data")

    def __init__(self, ranking_id: FifaRankingId = None, lang: str = "en", **kwargs):
        """
        Args:
            ranking_id (FifaRankingId): The id of the ranking.
            lang (str, optional): The language of the ranking. Defaults to "en".
        """
        if not ranking_id:
            ranking_id = ranking_ids()[0]
        self.__id = ranking_id
        self.__lang = lang
        self.__limit = kwargs.get("limit", None)
        self.__update_data()

    def __update_data(self) -> None:
        """
        Updates the ranking data.
        """
        path = CACHE.FIFA_RANKING(ranking_id=self.__id.value, lang=self.__lang)
        if exist_file(path):
            self.__data = load_pickle(path)
        else:
            self.__data = self.__get_data()
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
        return f"Ranking(id={self.__id}, lang={self.__lang},  limit={self.__limit})"

    def __repr__(self) -> str:
        """
        Returns:
            str: The representation of the ranking.
        """
        return str(self)

    @property
    def id_(self) -> FifaRankingId:
        """
        Returns:
            FifaRankingId: The id of the ranking.
        """
        return self.__id

    @id_.setter
    def id_(self, value: FifaRankingId):
        """
        Sets the id of the ranking.
        """
        if not isinstance(value, FifaRankingId):
            raise TypeError("Invalid type for the ranking id.")
        self.__id = value

    @property
    def lang(self) -> str:
        """
        Returns:
            str: The language of the ranking.
        """
        return self.__lang

    @lang.setter
    def lang(self, value: str) -> None:
        """
        Sets the language of the ranking.
        """
        if not isinstance(value, str):
            raise TypeError("Invalid type for the language.")
        self.__lang = value

    @property
    def limit(self) -> int:
        """
        Returns:
            int: The limit of the ranking items (teams) to get.
        """
        return self.__limit

    @limit.setter
    def limit(self, value: int) -> None:
        """
        Sets the limit of the ranking items (teams) to get.
        """
        if not isinstance(value, int):
            raise TypeError("Invalid type for the limit.")
        self.__limit = value

    def update(self) -> None:
        """
        Updates the ranking after a change in the ranking ID or the language.
        Please don't use this method if you don't need to update the ranking.
        """
        self.__update_data()

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

    def export(
        self, extension: typing.Literal["json", "csv"], filename: str = None
    ) -> None:
        """
        Exports the ranking data to a file.

        Args:
            extension (str): The extension of the file ("json" or "csv").
            filename (str, optional): The name of the file. Defaults to None.
        """
        if extension not in ["json", "csv"]:
            raise ValueError("Invalid format.")
        if extension == "json":
            self.export_json(filename)
        else:
            self.export_csv(filename)

    def export_json(self, filename: str) -> None:
        """
        Exports the ranking data to a json file.

        Args:
            filename (str): The name of the json file.
        """
        if not filename:
            filename = f"ranking_{self.__id.date}.json"
        try:
            with open(filename, "w", encoding="utf-8", errors="ignore") as file:
                data = self.__data.copy()
                data["rankings"] = data["rankings"][: self.__limit]
                json.dump(data, file, indent=4, ensure_ascii=False)
        except OSError as exc:
            print(f"Failed to export the ranking to {filename}: {exc}")
            print("Please make sure that the file is not open and try again.")

    def export_csv(self, filename: str = None) -> None:
        """
        Exports the ranking data to a csv file.

        Args:
            filename (str, optional): The name of the csv file. Defaults to None.
        """
        if not filename:
            filename = f"ranking_{self.__id.date}.csv"
        if not filename.endswith(".csv"):
            filename += ".csv"
        try:
            with open(filename, "w", encoding="utf-8", errors="ignore") as file:
                file.write(
                    "Rank,Team,Total Points,Previous Points,Country Code,Confederation,Flag\n"
                )
                for item in self.items():
                    file.write(
                        ",".join(
                            map(
                                str,
                                [
                                    item.rank,
                                    item.name,
                                    item.total_points,
                                    item.previous_points,
                                    item.country_code,
                                    item.confederation,
                                    item.flag.src,
                                ],
                            )
                        )
                        + "\n"
                    )
        except OSError as exc:
            print(f"Failed to export the ranking to {filename}: {exc}")
            print("Please make sure that the file is not open and try again.")


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
        FifaRankingId(value=i["id"], date=i["iso"])
        for d in data["ranking"]["dates"]
        for i in d["dates"]
    ]
    save_pickle(cache_path, ids)
    del xpath_data, data
    return ids
