from snulms.mixins.user import UserMixin
from snulms.mixins.auth import AuthMixin
from snulms.mixins.profile import ProfileMixin
import requests


class LMS(AuthMixin, UserMixin, ProfileMixin):
    def __init__(self) -> None:
        """
        Initialize the LMS object with a session
        """

        self.session = requests.session()
