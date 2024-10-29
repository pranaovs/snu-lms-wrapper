#!./.venv/bin/python
# Python wrapper for SNU LMS

import re
import requests
from bs4 import BeautifulSoup
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
if __name__ == "__main__":
    user1 = LMS()
