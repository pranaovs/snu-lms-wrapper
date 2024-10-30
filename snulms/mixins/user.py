from bs4 import BeautifulSoup

from snulms.utils import extractId, extractCourseId
from snulms.types import User


class UserMixin:
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
        self.profile = self.getUserDetails(extractId(profileUrl))
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
                        extractCourseId(course.select_one("a").get("href"))  # type:ignore
                    ),
                }
            )

        return User(userid, userName, userEmail, courseList)
