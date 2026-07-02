import os
from unittest.mock import patch

import pytest

from nowpayment import NowPayments
from nowpayment.models import AddressValidation, PayoutFee, SubscriptionPlan
from nowpayment.webhooks import IPNVerificationError, extract_ipn_signature, verify_ipn_payload

pytestmark = pytest.mark.skipif(
    not os.getenv("NOWPAYMENTS_SANDBOX_API_KEY"),
    reason="Set NOWPAYMENTS_SANDBOX_API_KEY to run sandbox integration tests",
)


@pytest.mark.integration
def test_sandbox_api_status():
    client = NowPayments(os.environ["NOWPAYMENTS_SANDBOX_API_KEY"], sandbox=True)
    status = client.get_api_status(as_model=True)
    assert status.message is not None


@pytest.mark.integration
def test_sandbox_currencies():
    client = NowPayments(os.environ["NOWPAYMENTS_SANDBOX_API_KEY"], sandbox=True)
    currencies = client.currency.get_available_currencies(as_model=True)
    assert currencies.currencies


@patch("requests.Session.request")
def test_validate_address(mock_request, mock_response):
    mock_request.return_value = mock_response(json_data={"valid": True})

    client = NowPayments("api-key")
    result = client.payout.validate_address(
        address="TAddr",
        currency="trx",
        as_model=True,
    )

    assert isinstance(result, AddressValidation)
    assert result.valid is True
    assert mock_request.call_args.args[1].endswith("/v1/payout/validate-address")


@patch("requests.Session.request")
def test_get_payout_fee(mock_request, mock_response):
    mock_request.return_value = mock_response(json_data={"fee": "0.1", "currency": "trx"})

    client = NowPayments("api-key")
    result = client.payout.get_payout_fee(currency="trx", amount=10, as_model=True)

    assert isinstance(result, PayoutFee)
    params = mock_request.call_args.kwargs["params"]
    assert params["currency"] == "trx"
    assert params["amount"] == 10


@patch("requests.Session.request")
def test_cancel_payout(mock_request, mock_response):
    mock_request.return_value = mock_response(status_code=200, text="OK")

    client = NowPayments("api-key", jwt_token="jwt")
    result = client.payout.cancel_payout("5001", as_model=True)

    assert result.status == "OK"
    assert mock_request.call_args.args[1].endswith("/v1/payout/5001/cancel")


@patch("requests.Session.request")
def test_create_subscription_plan(mock_request, mock_response):
    mock_request.return_value = mock_response(
        json_data={"id": 1, "title": "Pro", "amount": 10, "currency": "usd"}
    )

    client = NowPayments("api-key", jwt_token="jwt")
    plan = client.subscription.create_plan(
        title="Pro",
        interval_day=30,
        amount=10,
        currency="usd",
        as_model=True,
    )

    assert isinstance(plan, SubscriptionPlan)
    assert plan.title == "Pro"


@patch("requests.Session.request")
def test_create_email_subscription(mock_request, mock_response):
    mock_request.return_value = mock_response(json_data={"id": 99, "status": "WAITING"})

    client = NowPayments("api-key", jwt_token="jwt")
    result = client.subscription.create_subscription(
        subscription_plan_id=1,
        email="user@example.com",
        as_model=True,
    )

    assert result.id == 99
    payload = mock_request.call_args.kwargs["json"]
    assert payload["email"] == "user@example.com"


@patch("requests.Session.request")
def test_get_subscription_plans(mock_request, mock_response):
    mock_request.return_value = mock_response(
        json_data={"result": [{"id": 1, "title": "Basic"}], "count": 1}
    )

    client = NowPayments("api-key")
    plans = client.subscription.get_plans(limit=5, as_model=True)

    assert plans.count == 1
    assert plans.result[0].title == "Basic"


def test_verify_ipn_payload_accepts_valid_signature():
    data = {"payment_id": "1", "payment_status": "finished"}
    secret = "secret"
    from nowpayment import NowPayments

    signature = NowPayments.compute_payment_signature(data, secret)
    assert verify_ipn_payload(data, secret, signature) == data


def test_verify_ipn_payload_rejects_invalid_signature():
    with pytest.raises(IPNVerificationError):
        verify_ipn_payload({"payment_id": "1"}, "secret", "bad-signature")


def test_extract_ipn_signature_is_case_insensitive():
    headers = {"X-Nowpayments-Sig": "abc123"}
    assert extract_ipn_signature(headers) == "abc123"
