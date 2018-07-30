import json
import time
import requests
import hmac
import hashlib
import base64
from .constants import HTTPMethod, OrderWay


class Request:
    """Base class for sending API request"""

    BASE_URL = 'https://api.gtcprojects.com/'

    def __init__(
            self,
            private_key: str,
            public_key: str,
            command: str,
            http_method: HTTPMethod = HTTPMethod.GET,
            params: object = {}):
        """Request object initialization"""
        self.private_key = private_key
        self.public_key = public_key
        self.command = command
        self.http_method = http_method
        self.params = params
        self.content_type = '' if self.http_method == HTTPMethod.GET else 'application/json'
        self.url = self.__class__.BASE_URL + self.command

    def send(self):
        """Method to launch the request"""
        timestamp = '{:.3f}'.format(time.time())

        signature = self.message_signature(timestamp)

        headers = {
            'API_PUBLIC_KEY': self.public_key,
            'API_REQUEST_SIGNATURE': signature,
            'API_REQUEST_DATE': timestamp,
            'Content-Type': self.content_type,
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

        payload = json.dumps(self.params)

        if self.http_method == HTTPMethod.GET:
            F = requests.get
        elif self.http_method == HTTPMethod.POST:
            F = requests.post
        elif self.http_method == HTTPMethod.DELETE:
            F = requests.delete
        elif self.http_method == HTTPMethod.PUT:
            F = requests.put
        else:
            return {
                "responseStatus": {
                    "errorCode": "500",
                    "message": "Unsupported request type"
                }
            }

        response = F(self.url, data=payload, headers=headers)

        return response.json()

    def message_signature(self, timestamp: str) -> str:
        """Return the message signature to sign the request with"""
        message = (self.http_method + self.url +
                   self.content_type + timestamp).lower()
        digest = hmac.new(self.private_key.encode(),
                          message.encode(), hashlib.sha256).digest()
        b64_digest = base64.b64encode(digest, altchars=None)
        return str(b64_digest, 'UTF-8')
