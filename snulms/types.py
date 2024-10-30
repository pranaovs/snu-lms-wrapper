# This file contains the dataclasses for the various types used in the wrapper

from dataclasses import dataclass  # Importing the dataclass decorator


@dataclass
class User:
    userid: int
    name: str
    email: str | None
    courses: list[dict[str, str | int]]

    def __init__(
        self,
        userid: int,
        name: str,
        email: str | None,
        courses: list[dict[str, str | int]],
    ) -> None:
        """
        Initialize a user object with the given details

        Args:
            userid (int): User id of the user
            name (str): Name of the user
            email (str | None): Email of the user
            courses (list[int]): List of course ids the user is enrolled in
        """

        self.userid = userid
        self.name = name
        self.email = email
        self.courses = courses
