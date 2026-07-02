from unittest.mock import MagicMock

import pytest
import requests


@pytest.fixture
def mock_response():
    def _factory(status_code=200, text='{"message": "OK"}', json_data=None):
        response = MagicMock(spec=requests.Response)
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

    return _factory
