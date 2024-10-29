#!./.venv/bin/python
# Python wrapper for SNU LMS

import re
from dataclasses import dataclass
from os import environ

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


class LMS:
    # LMS Login url
    LOGIN_URL = "https://lms.snuchennai.edu.in/login/index.php"

    # Predefined message displayed when login successful and credentials incorrect
    # May change in future
    WELCOME_MSG = "Welcome to the Learning Management System (LMS) at Shiv Nadar University, Chennai !!"
    ERROR_MSG = "Invalid login, please try again"

    def __init__(self) -> None:
        """
        Initialize the LMS object with a session
        """

        self.session = requests.session()

    def login(self, username: str, password: str):
        """
        Login to the LMS with the given credentials

        Args:
            username (str): Username of the user
            password (str): Password of the user

        Raises:
            ValueError: If login credentials are invalid
        """

        # Fetch the login token (changed everytime)
        login_token = BeautifulSoup(
            self.session.get(self.LOGIN_URL).text, "html.parser"
        ).find(
            "input",
            {"name": "logintoken"},  # type:ignore
        )["value"]

        # default login payloads
        payload = {
            "anchor": "",
            "logintoken": login_token,
            "username": username,
            "password": password,
        }

        response = self.session.post(self.LOGIN_URL, data=payload)

        # If login successful, get self user details
        if self.checkLogin(response):
            return self.getSelfDetails()
        else:
            raise ValueError("Invalid login credentials")

    def checkLogin(self, response: requests.models.Response) -> bool:
        """
        Check if the login was successful or not

        Args:
            response (requests.models.Response): Response object from the login page

        Returns:
            bool: True if login successful, False otherwise
        """

        soup = BeautifulSoup(response.text, "html.parser")

        # Check if welcome message is in content
        if str(soup.p.contents[0].text) == self.WELCOME_MSG:  # type:ignore
            return True
        # Check if error message is in alert (id) box
        elif soup.body.select_one(".alert").text == self.ERROR_MSG:  # type:ignore
            return False
        # Raise exception if something unexpected happens
        else:
            return False

    def getSelfDetails(self):
        """
        Get the user details of the logged in user
        Expects a response object from the home page

        Returns:
            User: User object with the details of the logged in user
        """

        response = self.session.get("https://lms.snuchennai.edu.in/")
        soup = BeautifulSoup(response.text, "html.parser")

        profileUrl: str = ""

        # Get the dropdown button list and extract href from Profile button
        for btn in soup.find_all("a", class_="dropdown-item"):
            if "Profile" in btn.text:
                profileUrl = btn.get("href")
                break

        # Set a profile variable containing logged in user details
        self.profile = self.getUserDetails(self.extractId(profileUrl))
        return self.profile

    def getUserDetails(self, userid: int):
        """
        Get the user details of a user with the given userid

        Args:
            userid (int): User id of the user

        Returns:
            User: User object with the details of the user
        """

        USER_DETAILS_URL = f"https://lms.snuchennai.edu.in/user/profile.php?id={userid}"
        response = self.session.get(USER_DETAILS_URL.format(userid))

        soup = BeautifulSoup(response.text, "html.parser")

        # Get user name
        userName: str = str(
            soup.select_one(".page-header-headings > h1:nth-child(1)").text  # type:ignore
        )

        # Get all sections in the page and save it inside a dict with its key being the title of the section
        # HACK: The page is inconsistent for different profiles
        sections: dict[str, str] = {}
        for section in soup.select("section.node_category"):
            sections[str(section.select_one("h3").text)] = section.select_one("div")  # type:ignore

        try:
            userEmail = str(
                sections["User details"].select_one("dd").select_one("a").text  # type:ignore
            )
        except AttributeError:
            # Check if email is in the name section
            try:
                userEmail = str(soup.select_one(".no-overflow").text)  # type:ignore
            except AttributeError:
                userEmail = None

        # Iterate through the list of courses and extract the course name and courseid
        courseList: list[dict[str, str | int]] = []
        for course in sections["Course details"].select("ul"):  # type:ignore
            courseList.append(
                {
                    "name": str(course.select_one("a").text),  # type:ignore
                    "courseid": int(
                        self.extractCourseId(course.select_one("a").get("href"))  # type:ignore
                    ),
                }
            )

        return User(userid, userName, userEmail, courseList)

    def extractId(self, url: str) -> int:
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

    def extractCourseId(self, url: str) -> int:
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


if __name__ == "__main__":
    user1 = LMS()
    user1.login(str(environ.get("LMS_USERNAME")), str(environ.get("LMS_PASSWORD")))
