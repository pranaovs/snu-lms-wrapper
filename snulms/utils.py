import re


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
