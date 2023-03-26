class ConnectionError(Exception):
    """failed to connect to vts api"""

    pass


class AuthenticationError(Exception):
    """failed to get authenticated"""

    pass


class UnexceptedResponse(Exception):
    """received server response with unexpected request ID"""

    pass


class APIError(Exception):
    """received error from api"""

    pass
