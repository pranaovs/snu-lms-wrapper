from snulms.mixins.login import LoginMixin
from snulms.mixins.user import UserMixin
import requests


class LMS(LoginMixin, UserMixin):
    def __init__(self) -> None:
        """
        Initialize the LMS object with a session
        """

        self.session = requests.session()
