import requests


class BaseAPI:
    """Base API class.

    Args:
        api_key (str): API key.
    """

    def __init__(self, api_key: str, jwt_token: str = None):
        self.api_key = api_key
        self.jwt_token = jwt_token

    def _request(self, method: str, path: str, **kwargs):
        """Make request to API.

        Args:
            method (str): HTTP method.
            url (str): URL of API.
            **kwargs: Keyword arguments.

        Returns:
            dict: Response of API.
        """
        headers: dict = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        if self.jwt_token:
            headers['Authorization'] = self.jwt_token
        url = f"https://api.nowpayments.io/v1/{path}"
        return requests.request(
            method,
            url,
            headers=headers,
            **kwargs
        ).json()

    def get_api_status(self) -> dict:
        """This is a method for obtaining the status of the API.

        Returns:
            dict: Status of the API.
        """
        return self._request('GET', "status")
