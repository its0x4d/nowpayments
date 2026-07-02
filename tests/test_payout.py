from unittest.mock import patch

import pytest

from nowpayment import NowPayments
from nowpayment.models import WithdrawalModel


@patch("requests.Session.request")
def test_login(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"token": "jwt-token"})

    client = NowPayments("api-key")
    result = client.payout.login(email="a@b.com", password="secret")

    assert result["token"] == "jwt-token"
    assert mock_request.call_args.kwargs["json"]["email"] == "a@b.com"


@patch("requests.Session.request")
def test_create_payout_requires_jwt(mock_request):
    client = NowPayments("api-key")
    withdrawal = WithdrawalModel(
        address="addr",
        currency="trx",
        amount=1.0,
        ipn_callback_url="https://example.com/ipn",
    )

    with pytest.raises(ValueError, match="JWT token"):
        client.payout.create_payout(
            withdrawals=withdrawal,
            ipn_callback_url="https://example.com/ipn",
        )


@patch("requests.Session.request")
def test_create_payout_sends_withdrawals(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"id": "payout-1"})

    client = NowPayments("api-key", jwt_token="jwt")
    withdrawal = WithdrawalModel(
        address="addr",
        currency="trx",
        amount=1.0,
        ipn_callback_url="https://example.com/ipn",
    )
    result = client.payout.create_payout(
        withdrawals=withdrawal,
        ipn_callback_url="https://example.com/batch-ipn",
    )

    assert result["id"] == "payout-1"
    payload = mock_request.call_args.kwargs["json"]
    assert payload["withdrawals"][0]["address"] == "addr"


@patch("requests.Session.request")
def test_verify_payout_accepts_payout_id_alias(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(status_code=200, text="OK")

    client = NowPayments("api-key", jwt_token="jwt")
    result = client.payout.verify_payout(
        payout_id="5000000191",
        verification_code="123456",
    )

    assert result == {"status": "OK"}
    assert mock_request.call_args.args[1].endswith("/v1/payout/5000000191/verify")
