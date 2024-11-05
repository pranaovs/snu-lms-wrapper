from datetime import datetime

from bs4 import BeautifulSoup

from snulms.constants import BASE_URL, USER_DETAILS_URL
from snulms.types import User
from snulms.utils import extract_url_param, parse_login_activity


class UserMixin:
    def __init__(self):
        # Get the session object from the parent class
        self.session = super().session  # type:ignore

    def get_user(self, userid: int) -> User:
        """
        Get the user details of a user with the given userid

        Args:
            userid (int): User id of the user

        Returns:
            User: User object with the details of the user
        """

        response = self.session.get(USER_DETAILS_URL.format(userid))

        soup = BeautifulSoup(response.text, "html.parser")

        # Get user name
        userName: str = str(
            soup.find("div", class_="page-header-headings").find("h1").text  # type:ignore
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
        courseList: dict[int, str] = {}

        for course in sections["Course details"].find_all("a"):  # type:ignore
            courseList.update(
                {
                    int(
                        extract_url_param("course", course.get("href"))  # type:ignore
                    ): str(course.text),  # type:ignore
                }
            )

        # Get login activity
        loginActivity: dict[str, datetime] = {}
        for item in sections["Login activity"].find_all("dl"):  # type: ignore
            loginActivity.update(
                {
                    item.select_one("dt").text: parse_login_activity(
                        str(item.select_one("dd").text)
                    )
                }
            )

        # Get user profile photo

        userPic = str(
            soup.find("div", id="page").find(class_="userpicture").get("src")  # type:ignore
        )

        return User(
            userid=userid,
            name=userName,
            email=userEmail,
            picture=userPic,
            courses=courseList,
            first_access=loginActivity["First access to site"],
            last_access=loginActivity["Last access to site"],
        )
