import pickle

import requests
from bs4 import BeautifulSoup

from snulms.utils import extract_url_param
from snulms.exceptions import (
    BadCredentials,
    MissingCredentials,
    SessionExpired,
    UnknownError,
)
from snulms.constants import BASE_URL, LOGIN_URL, LOGOUT_URL


class AuthMixin:
    def __init__(self):
        self.LOGIN_URL = "https://lms.snuchennai.edu.in/login/index.php"
        self.BASE_URL = "https://lms.snuchennai.edu.in"

        self.session = super().session  # type:ignore
        self.get_profile = super().get_profile  # type:ignore

    def login(
        self,
        username: str = "",
        password: str = "",
        session: str = "",
        relogin: bool = False,
    ):
        """
        Login to the LMS with the given credentials or the session file dump

        Args:
            username (str): Username of the user
            password (str): Password of the user
            session (str, optional): Path to the session dump file. Generated by dump_session().
            relogin (bool, optional): Relogin to the LMS. Defaults to False

        Returns:
            User: User object with logged in user details

        Raises:
            BadCredentials: If login credentials are invalid
            SessionExpired: If session is expired
        """

        # If credentials are not provided, stop the login process
        if (not (username and password)) and (not session):
            raise MissingCredentials(
                "Either username and password or session file is required"
            )

        # If session file is provided, attempt to restore session
        if session:
            self.restore_session(session)

            # If session is valid, return the logged in user profile
            if self.check_session():
                return self.get_profile()
            # If session is invalid
            else:
                # If relogin is set to False, raise SessionExpired
                if not relogin:
                    raise SessionExpired("Session expired, please login again")
                # Else attept to login with username and password (continue with login flow)
                else:
                    pass

        login_token = BeautifulSoup(
            self.session.get(LOGIN_URL).text, "html.parser"
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

        self.session.post(LOGIN_URL, data=payload)

        if self.check_session():
            return self.get_profile()

        else:
            raise BadCredentials("Invalid login credentials")

    def check_session(self) -> bool:
        """
        Check if the current session is logged in or not

        Args:
            None

        Returns:
            bool: True if session is valid, False otherwise
        """

        response = self.session.get(LOGIN_URL)

        soup = BeautifulSoup(response.text, "html.parser")

        if "You are logged in as" in (soup.find(class_="logininfo").text):  # type:ignore
            self.sesskey = self.get_sesskey()
            return True
        elif "You are not logged in." in (soup.find(class_="logininfo").text):  # type:ignore
            return False
        else:
            raise UnknownError("Unknown error occurred")

    def get_sesskey(self) -> str:
        response = self.session.get(BASE_URL)

        soup = BeautifulSoup(response.text, "html.parser")

        logout_button = ""

        # Get the dropdown button list and extract href from Profile button
        for btn in soup.find_all("a", class_="dropdown-item"):
            if "Log out" in btn.text:
                logout_button = btn.get("href")
                break

        return extract_url_param("sesskey", logout_button)

    def dump_session(self, filename: str = "session"):
        """
        Dump sesion object to a file to use logged in session later

        Args:
            filename (str): name of the file to dump the session object
        """

        with open(filename, "wb") as file:
            pickle.dump(self.session, file)

    def restore_session(self, filename: str):
        """
        Restore session object from a dumped file

        Args:
            filename (str): name of the file to restore the session object
        """

        with open(filename, "rb") as file:
            self.session = pickle.load(file)

    def logout(self):
        """
        Logout from the LMS
        """

        # Logout from the LMS
        self.session.get(LOGOUT_URL.format(self.sesskey))
