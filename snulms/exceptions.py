class ClientError(Exception):
    response = None
    code = None
    message = ""

    def __init__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 0:
            self.message = str(args.pop(0))
        for key in list(kwargs.keys()):
            setattr(self, key, kwargs.pop(key))
        if not self.message:
            self.message = "{title} ({body})".format(
                title=getattr(self, "reason", "Unknown"),
                body=getattr(self, "error_type", vars(self)),
            )
        super().__init__(self.message, *args, **kwargs)
        if self.response:
            self.code = self.response.status_code


class BadCredentials(ClientError):
    """
    Raised when login fails.
    Username or password is incorrect.
    """


class MissingCredentials(ClientError):
    """
    Raised when username or password is not provided.
    """


class SessionExpired(ClientError):
    """
    Raised when session is expired.
    """


class UnknownError(ClientError):
    """
    Raised when an unknown error occurs.
    """
