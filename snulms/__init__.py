from snulms.mixins.user import UserMixin
from snulms.mixins.auth import AuthMixin
import requests


class LMS(AuthMixin, UserMixin):
    def __init__(self) -> None:
        """
        Initialize the LMS object with a session
        """

        self.session = requests.session()
