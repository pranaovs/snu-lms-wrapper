from datetime import datetime
import re
from dateutil.parser import parse

from urllib.parse import parse_qs, urlparse


def extractId(url: str) -> int:
    """
    DEPRECATED: Use extractUrlParam instead.
    Extract the user id from the url of format: https://lms.snuchennai.edu.in/user/profile.php?id={userid}/

    Args:
        url (str): a url

    Returns:
        int: user id from the url

    Raises:
        ValueError: If id= part is not found in the url
    """

    match = re.search(r"[?&]id=(\d+)", url)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("Invalid URL")


def extractCourseId(url: str) -> int:
    """
    DEPRECATED: Use extractUrlParam instead.

    Extract the user id from the url of format: https://lms.snuchennai.edu.in/user/profile.php?course={courseid}/

    Args:
        url (str): a url

    Returns:
        int: course id from the url

    Raises:
        ValueError: If course= part is not found in the url
    """

    match = re.search(r"[?&]course=(\d+)", url)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("Invalid URL")


def extract_url_param(param: str, url: str) -> str:
    """
    Extract the value of the given parameter from the url
    Args:
        param (str): parameter to extract
        url (str): a url

    Returns:
        str: value of the parameter

    Raises:
        ValueError: If the parameter is not found in the url
    """

    try:
        # parse_qs returns a dictionary with the parameter as key and value as list
        return str(parse_qs((urlparse(url)).query)[param][0])

    except KeyError:
        # If the parameter is not found in the url
        raise ValueError(f"Parameter {param} not found in the url")


def parse_login_activity(input: str) -> datetime:
    """
    Convert the login date and time recieved from from the webpage to datetime format

    Args:
        input (str): the date string from the website of the format 'Tuesday, 20 August 2024, 9:36 AM  (71 days 13 hours)'

    Returns:
        datetime: a datetime object with converted date

    Raises:
        dateutil.parser._parser.ParserError: if unable to parse the date string
    """
    return parse(re.sub(r"\s*\(.*?\)", "", input))
