from typing import Union

import requests


class Empty:
    pass


class BaseAPI:
    """Base API class.

    Args:
        api_key (str): API key.
    """

    def __init__(self, api_key: str, jwt_token: str = None):
        self.api_key = api_key
        self.jwt_token = jwt_token

    def _request(self, method: str, path: str, headers: Union[None, dict] = Empty, **kwargs):
        """
        This is the method to make a request to the API.

        :param method: HTTP method
        :param path: API path
        :param headers: HTTP headers
        :param kwargs: See: https://requests.readthedocs.io/en/master/api/#main-interface
        :return: API response.
        """
        set_headers: dict = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        if self.jwt_token:
            set_headers['Authorization'] = self.jwt_token
        if headers is not Empty:
            set_headers = headers
        url = f"https://api.nowpayments.io/v1/{path}"
        print(set_headers)
        req = requests.request(
            method,
            url,
            headers=set_headers,
            **kwargs
        )
        if req.status_code == 200:
            return req.json()
        return req.content

    def get_api_status(self) -> dict:
        """This is a method for obtaining the status of the API.

        Returns:
            dict: Status of the API.
        """
        return self._request('GET', "status")
