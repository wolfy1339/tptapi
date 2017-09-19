from requests.exceptions import HTTPError


class InvalidLogin(HTTPError):
    """You have entered invlaid credentials"""
    pass
