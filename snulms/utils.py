from datetime import datetime
import re
from dateutil.parser import parse


def extractId(url: str) -> int:
    """
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


def parseLoginActivity(input: str) -> datetime:
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
