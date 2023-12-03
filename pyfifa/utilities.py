"""
This module contains only utility functions used by the other modules.
"""
import os
import pickle
import httpx
import lxml.html as parser


def save_pickle(path: str, data: object) -> None:
    """
    Saves the given data in a pickle file.

    Args:
        path (str): The path of the pickle file.
        data (object): The data to save.
    """
    with open(path, "wb") as file:
        pickle.dump(data, file)


def load_pickle(path: str) -> object:
    """
    Loads the data from a pickle file.

    Args:
        path (str): The path of the pickle file.

    Returns:
        object: The loaded data.
    """
    with open(path, "rb") as file:
        return pickle.load(file)


def exist_file(path: str) -> bool:
    """
    Checks if the given file exists.

    Args:
        path (str): The path of the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    try:
        with open(path, "r", encoding="utf-8"):
            return True
    except FileNotFoundError:
        return False


def create_directory(path: str) -> None:
    """
    Creates a directory.

    Args:
        path (str): The path of the directory.
    """
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def get(url: str) -> str:
    """
    Gets the content of the given url.

    Args:
        url (str): The url.

    Returns:
        str: The content of the url.
    """
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.content
    except Exception as exc:
        raise RuntimeError(f"Failed to get the url: {url}") from exc


def extract_xpath(content: str, xpath_expression: str) -> list:
    """
    Extracts the data from the given content using the given xpath expression.

    Args:
        content (str): The content.
        xpath_expression (str): The xpath expression.

    Returns:
        list: The extracted data.
    """
    return parser.fromstring(content).xpath(xpath_expression)
