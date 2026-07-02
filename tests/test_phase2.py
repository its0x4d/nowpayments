from unittest.mock import MagicMock, patch

import requests

from nowpayment import NowPayments
from nowpayment.models import Invoice, Payment


@patch("requests.Session.request")
def test_sandbox_uses_sandbox_base_url(mock_request, mock_response):
    mock_request.return_value = mock_response(json_data={"message": "OK"})

    client = NowPayments("api-key", sandbox=True)
    client.get_api_status()

    assert mock_request.call_args.args[1].startswith("https://api.sandbox.nowpayments.io/v1/")


@patch("requests.Session.request")
def test_production_uses_production_base_url(mock_request, mock_response):
    mock_request.return_value = mock_response(json_data={"message": "OK"})

    client = NowPayments("api-key")
    client.get_api_status()

    assert mock_request.call_args.args[1].startswith("https://api.nowpayments.io/v1/")


@patch("requests.Session.close")
@patch("requests.Session.request")
def test_context_manager_closes_owned_session(mock_request, mock_close, mock_response):
    mock_request.return_value = mock_response(json_data={"message": "OK"})

    with NowPayments("api-key") as client:
        client.get_api_status()

    mock_close.assert_called_once()


def test_external_session_is_not_closed():
    session = MagicMock(spec=requests.Session)
    client = NowPayments("api-key", session=session)
    client.close()
    session.close.assert_not_called()


@patch("requests.Session.request")
def test_create_payment_as_model(mock_request, mock_response):
    mock_request.return_value = mock_response(
        json_data={
            "payment_id": "123",
            "payment_status": "waiting",
            "order_id": "order-1",
        }
    )

    client = NowPayments("api-key")
    payment = client.payment.create_payment(
        price_amount=10,
        price_currency="USD",
        pay_currency="TRX",
        order_id="order-1",
        ipn_callback_url="https://example.com/ipn",
        as_model=True,
    )

    assert isinstance(payment, Payment)
    assert payment.payment_id == "123"
    assert payment.raw["payment_status"] == "waiting"


@patch("requests.Session.request")
def test_create_invoice_as_model(mock_request, mock_response):
    mock_request.return_value = mock_response(
        json_data={
            "id": "invoice-1",
            "invoice_url": "https://nowpayments.io/payment/?iid=invoice-1",
        }
    )

    client = NowPayments("api-key")
    invoice = client.payment.create_invoice(
        price_amount=1,
        price_currency="USD",
        as_model=True,
    )

    assert isinstance(invoice, Invoice)
    assert invoice.id == "invoice-1"
    assert invoice.invoice_url.endswith("invoice-1")
