from typing import Union

import requests


class BaseAPI:
    """Base API class.

    Args:
        api_key (str): API key.
    """

    def __init__(self, api_key: str, jwt_token: str = None, timeout = None):
        self.api_key = api_key
        self.jwt_token = jwt_token
        self.timeout = timeout

    def _request(self, method: str, path: str, headers: Union[None, dict] = None, **kwargs):
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
            set_headers['Authorization'] = "Bearer " + self.jwt_token
        if headers:
            set_headers = headers
        url = f"https://api.nowpayments.io/v1/{path}"
        req = requests.request(
            method,
            url,
            headers=set_headers,
            timeout=self.timeout,
            **kwargs
        )
        if req.text == 'OK':
            # This response is used for verify payout method!
            # TODO: Refactor and create some better response
            return {'status': 'OK'}
        return req.json()

    def get_api_status(self) -> dict:
        """This is a method for obtaining the status of the API.

        Returns:
            dict: Status of the API.
        """
        return self._request('GET', "status")
