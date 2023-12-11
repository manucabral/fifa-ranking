"""
Constants used in the pyfifa package.
"""

import os
import pathlib


def absolute_path(path: str) -> str:
    """
    Returns the absolute path of the given path.

    Args:
        path (str): The relative path.

    Returns:
        str: The absolute path.
    """
    return os.path.join(pathlib.Path(__file__).parent.absolute(), path)


# pylint: disable=R0903
class ENDPOINTS:
    """
    Endspoints which are used to get the data.
    """

    class RANKING:
        """
        Ranking endpoints.
        """

        API = "https://www.fifa.com/api/ranking-overview?locale={lang}&dateId={id}"
        HTML = "https://www.fifa.com/fifa-world-ranking/{genre}?locale=en_US"

    class CONFEDERATIONS:
        """
        Confederations endpoints.
        """

        ALL = ["CAF", "CONCACAF", "CONMEBOL", "OFC", "AFC", "UEFA"]
        API = "https://api.fifa.com/api/v3/confederations/{confederation_id}"

    class TEAMS:
        """
        Teams endpoints.
        """

        class CONMEBOL:
            """
            CONMEBOL endpoints.
            """

            TEAM_IDS = {
                43922: "Argentina",
                43923: "Bolivia",
                43924: "Brazil",
                43925: "Chile",
                43926: "Colombia",
                43927: "Ecuador",
                43928: "Paraguay",
                43929: "Peru",
                43930: "Uruguay",
                43931: "Venezuela",
            }

        class UEFA:
            """
            UEFA endpoints.
            """

            TEAM_IDS = {
                43932: "Albania",
                43933: "Armenia",
                43934: "Austria",
                43935: "Belgium",
                43936: "Bulgaria",
                # ...
            }


class CACHE:
    """
    Cache paths which are used to save the data.
    """

    # pylint: disable=C0103
    @staticmethod
    def FIFA_RANKING_ID(genre: str) -> str:
        """
        Returns the path of the FIFA ranking ids cache file (depends on the genre)

        Args:
            genre (str): The genre of the ranking "men" or "women"

        Returns:
            str: The absolute path of the FIFA ranking ids cache file.
        """
        return absolute_path(f"cache/fifa_ranking_{genre}_ids.pyfifa")

    # pylint: disable=C0103
    @staticmethod
    def FIFA_RANKING(ranking_id: str, lang: str) -> str:
        """
        Returns the path of the a FIFA ranking cache file with the given id.

        Args:
            ranking_id (str): The id of the ranking.
            lang (str): The language of the ranking.

        Returns:
            str: The absolute path of the FIFA ranking cache file.
        """
        return absolute_path(f"cache/fifa_ranking_{ranking_id}_{lang}.pyfifa")
