from typing import Any, Dict, Optional, Union

import requests

from nowpayment.constants import PRODUCTION_BASE_URL
from nowpayment.exceptions import NowPaymentsAPIError


class BaseAPI:
    """Base API class for NOWPayments HTTP requests."""

    def __init__(
        self,
        api_key: str,
        jwt_token: Optional[str] = None,
        timeout: Optional[Union[int, float]] = None,
        base_url: str = PRODUCTION_BASE_URL,
        session: Optional[requests.Session] = None,
    ):
        self.api_key = api_key
        self.jwt_token = jwt_token
        self.timeout = timeout
        self.base_url = base_url.rstrip("/")
        self._session = session
        self._owns_session = session is None

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def close(self) -> None:
        if self._owns_session and self._session is not None:
            self._session.close()
            self._session = None

    def _build_headers(self, headers: Optional[dict] = None) -> dict:
        set_headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }
        if self.jwt_token:
            set_headers["Authorization"] = f"Bearer {self.jwt_token}"
        if headers:
            set_headers.update(headers)
        return set_headers

    def _parse_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.text == "OK":
            return {"status": "OK"}

        if not response.ok:
            message = response.text or response.reason
            payload: Optional[Dict[str, Any]] = None
            try:
                payload = response.json()
                if isinstance(payload, dict):
                    message = payload.get("message", message)
            except ValueError:
                pass
            raise NowPaymentsAPIError(response.status_code, str(message), payload)

        if not response.text:
            return {}

        try:
            return response.json()
        except ValueError as exc:
            raise NowPaymentsAPIError(
                response.status_code,
                "Invalid JSON response from NOWPayments API",
            ) from exc

    def _request(
        self,
        method: str,
        path: str,
        headers: Optional[dict] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Make a request to the NOWPayments API.

        :param method: HTTP method.
        :param path: API path relative to the base URL.
        :param headers: Optional headers merged into defaults.
        :param kwargs: Additional arguments passed to requests.
        :return: Parsed API response.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(
            method,
            url,
            headers=self._build_headers(headers),
            timeout=self.timeout,
            **kwargs,
        )
        return self._parse_response(response)

    def get_api_status(self) -> dict:
        """Return the current API status."""
        return self._request("GET", "status")
