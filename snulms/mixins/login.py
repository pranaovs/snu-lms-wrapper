import requests
from bs4 import BeautifulSoup

from snulms.utils import extract_url_param


class LoginMixin:
    def __init__(self):
        # Get the session object from the parent class
        self.session = super().session  # type:ignore
        self.get_profile = super().get_profile  # type:ignore

    def login(self, username: str, password: str):
        """
        Login to the LMS with the given credentials

        Args:
            username (str): Username of the user
            password (str): Password of the user

        Raises:
            ValueError: If login credentials are invalid
        """

        # LMS Login url
        self.LOGIN_URL = "https://lms.snuchennai.edu.in/login/index.php"

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
        if self.check_login(response):
            self.sesskey = self.get_sesskey(response)
            return self.get_profile()
        else:
            raise ValueError("Invalid login credentials")

    def get_sesskey(self, response: requests.Response) -> str:
        soup = BeautifulSoup(response.text, "html.parser")

        LOGOUT_URL: str = ""

        # Get the dropdown button list and extract href from Profile button
        for btn in soup.find_all("a", class_="dropdown-item"):
            if "Log out" in btn.text:
                LOGOUT_URL = btn.get("href")
                break

        return extract_url_param("sesskey", LOGOUT_URL)

    def check_login(self, response: requests.models.Response) -> bool:
        """
        Check if the login was successful or not

        Args:
            response (requests.models.Response): Response object from the login page

        Returns:
            bool: True if login successful, False otherwise
        """

        # Predefined message displayed when login successful and credentials incorrect
        # May change in future
        self.WELCOME_MSG = "Welcome to the Learning Management System (LMS) at Shiv Nadar University, Chennai !!"
        self.ERROR_MSG = "Invalid login, please try again"

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
    def logout(self):
        """
        Logout from the LMS
        """
        # LMS Logout url
        self.LOGOUT_URL = "https://lms.snuchennai.edu.in/login/logout.php?sesskey={}"

        # Logout from the LMS
        self.session.get(self.LOGOUT_URL.format(self.sesskey))
