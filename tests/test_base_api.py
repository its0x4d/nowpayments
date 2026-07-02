from unittest.mock import patch

import pytest
import requests

from nowpayment.apis import BaseAPI
from nowpayment.exceptions import NowPaymentsAPIError


def _mock_response(status_code=200, text='{"message": "OK"}', json_data=None):
    response = __import__("unittest.mock").mock.MagicMock(spec=requests.Response)
    response.status_code = status_code
    response.ok = 200 <= status_code < 300
    response.reason = "OK" if response.ok else "Error"
    response.text = text
    if json_data is not None:
        response.json.return_value = json_data
    elif response.ok and text not in ("", "OK"):
        response.json.return_value = {"message": "OK"}
    else:
        response.json.side_effect = ValueError("No JSON")
    return response


@patch("requests.Session.request")
def test_request_merges_custom_headers(mock_request):
    mock_request.return_value = _mock_response()

    api = BaseAPI("test-api-key", jwt_token="jwt-token")
    api._request("GET", "status", headers={"X-Custom": "1"})

    headers = mock_request.call_args.kwargs["headers"]
    assert headers["x-api-key"] == "test-api-key"
    assert headers["Authorization"] == "Bearer jwt-token"
    assert headers["X-Custom"] == "1"


@patch("requests.Session.request")
def test_request_raises_on_http_error(mock_request):
    mock_request.return_value = _mock_response(
        status_code=400,
        text='{"message": "Bad request"}',
        json_data={"message": "Bad request"},
    )

    api = BaseAPI("test-api-key")
    with pytest.raises(NowPaymentsAPIError) as exc_info:
        api._request("GET", "status")

    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Bad request"


@patch("requests.Session.request")
def test_request_parses_plain_ok_response(mock_request):
    mock_request.return_value = _mock_response(status_code=200, text="OK")

    api = BaseAPI("test-api-key")
    assert api._request("POST", "payout/1/verify") == {"status": "OK"}


@patch("requests.Session.request")
def test_request_raises_on_invalid_json(mock_request):
    response = _mock_response(status_code=200, text="not-json")
    response.json.side_effect = ValueError("No JSON")
    mock_request.return_value = response

    api = BaseAPI("test-api-key")
    with pytest.raises(NowPaymentsAPIError) as exc_info:
        api._request("GET", "status")

    assert "Invalid JSON" in exc_info.value.message
