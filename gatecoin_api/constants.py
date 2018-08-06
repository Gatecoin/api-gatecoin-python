"""Common constants and enums"""
from enum import Enum


class HTTPMethod(Enum):
    """HTTP methods enumeration"""
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'

    def __add__(self, other):
        return self.value + other


# Order Ways
BID = 'bid'
ASK = 'ask'
