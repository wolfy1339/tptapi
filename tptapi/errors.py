from requests.exceptions import HTTPError


class InvalidLogin(HTTPError):
    pass
