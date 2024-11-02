from bs4 import BeautifulSoup

from snulms.constants import BASE_URL
from snulms.types import User
from snulms.utils import extract_url_param


class ProfileMixin:
    def __init__(self) -> None:
        # Get objects from parent class to prevent LSP warnings
        self.session = super().session  # type:ignore
        self.profile = super().profile  # type:ignore
        self.get_user = super().get_user  # type:ignore

    def get_profile(self, refresh: bool = False) -> User:
        """
        Get the user details of the logged in user
        Expects a response object from the home page

        Args:
            refresh (bool, optional): force refreshes your details from the website.

        Returns:
            User: User object with the details of the logged in user
        """

        # Caching the profile details in self.profile variable
        if not refresh:
            # Check if self.profile variable exists
            try:
                self.profile
            # If AttributeError, do not do anything (proceed with fetching details)
            except AttributeError:
                pass
            # If self.profile exists, return it
            else:
                return self.profile

        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        profileUrl: str = ""

        # Get the dropdown button list and extract href from Profile button
        for btn in soup.find_all("a", class_="dropdown-item"):
            if "Profile" in btn.text:
                profileUrl = btn.get("href")
                break

        # Set a profile variable containing logged in user details
        self.profile: User = self.get_user(int(extract_url_param("id", profileUrl)))
        return self.profile

    def get_courses(self, refresh: bool = False) -> dict[int, str]:
        """
        Get the list of courses the logged in user is enrolled in
        Args:
            None
        Returns:
            list[dict[str, str | int]]: List of courses the user is enrolled in
        """

        # Caching the enrolled courses details in self.courses variable
        if not refresh:
            # Check if self.courses variable exists
            try:
                self.courses
            # If AttributeError, do not do anything (proceed with fetching details)
            except AttributeError:
                pass
            # If self.courses exists, return it
            else:
                return self.courses

        self.courses = self.get_profile(refresh=True).courses
        return self.courses
