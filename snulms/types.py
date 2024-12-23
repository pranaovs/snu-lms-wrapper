# This file contains the dataclasses for the various types used in the wrapper

from dataclasses import dataclass  # Importing the dataclass decorator
from datetime import datetime


@dataclass
class User:
    userid: int
    name: str
    email: str | None
    picture: str | None
    courses: dict[int, str]
    first_access: datetime
    last_access: datetime

    def __init__(
        self,
        userid: int,
        name: str,
        email: str | None,
        picture: str | None,
        courses: dict[int, str],
        first_access: datetime,
        last_access: datetime,
    ) -> None:
        """
        Initialize a user object with the given details

        Args:
            userid (int): User id of the user
            name (str): Name of the user
            email (str | None): Email of the user
            picture (str | None): URL of the user's profile picture
            courses (dict[int, str]): Courses the user is enrolled in. Key: Course ID, Value: Course Name
            first_access (datetime): First access to the site by the user
            last_access (datetime): Last access to the site by the user
        """

        self.userid = userid
        self.name = name
        self.email = email
        self.picture = picture
        self.courses = courses
        self.first_access = first_access
        self.last_access = last_access
