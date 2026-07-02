from unittest.mock import patch

import pytest

from nowpayment import NowPayments
from nowpayment.decorators import jwt_required


class _JwtClient:
    jwt_token = None

    @jwt_required
    def protected(self):
        return "ok"


def test_jwt_required_raises_without_token():
    with pytest.raises(ValueError, match="JWT token"):
        _JwtClient().protected()


def test_jwt_required_allows_with_token():
    client = _JwtClient()
    client.jwt_token = "token"
    assert client.protected() == "ok"


@patch("requests.Session.request")
def test_get_user_payments_omits_payment_id_when_none(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"data": []})

    client = NowPayments("api-key", jwt_token="jwt")
    client.billing.get_user_payments(sub_partner_id=42)

    params = mock_request.call_args.kwargs["params"]
    assert params["sub_partner_id"] == 42
    assert "id" not in params


@patch("requests.Session.request")
def test_get_user_payments_includes_payment_id_when_set(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"data": []})

    client = NowPayments("api-key", jwt_token="jwt")
    client.billing.get_user_payments(sub_partner_id=42, payment_id=99)

    params = mock_request.call_args.kwargs["params"]
    assert params["id"] == 99


@patch("requests.Session.request")
def test_create_recurring_payments_uses_subscriptions_endpoint(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"result": {}})

    client = NowPayments("api-key", jwt_token="jwt")
    client.billing.create_recurring_payments(
        subscription_plan_id=1,
        sub_partner_id=2,
    )

    assert mock_request.call_args.args[1].endswith("/v1/subscriptions")


@patch("requests.Session.request")
def test_get_users_builds_query_params(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"result": []})

    client = NowPayments("api-key", jwt_token="jwt")
    client.billing.get_users(sub_partner_id=[1, 2], limit=5)

    params = mock_request.call_args.kwargs["params"]
    assert params["id"] == "1,2"
    assert params["limit"] == 5
