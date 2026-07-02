from unittest.mock import patch

import pytest

from nowpayment import NowPayments
from nowpayment.exceptions import NowPaymentsAPIError


@patch("requests.Session.request")
def test_get_api_status(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"message": "OK"})

    client = NowPayments("api-key")
    assert client.get_api_status() == {"message": "OK"}

    assert mock_request.call_args.args[0] == "GET"
    assert mock_request.call_args.args[1].endswith("/v1/status")


@patch("requests.Session.request")
def test_create_payment(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(
        json_data={"payment_id": "123", "payment_status": "waiting"}
    )

    client = NowPayments("api-key")
    result = client.payment.create_payment(
        price_amount=10,
        price_currency="USD",
        pay_currency="TRX",
        order_id="order-1",
        ipn_callback_url="https://example.com/ipn",
    )

    assert result["payment_id"] == "123"
    assert mock_request.call_args.kwargs["json"]["order_id"] == "order-1"


@patch("requests.Session.request")
def test_create_invoice(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(json_data={"id": "invoice-1"})

    client = NowPayments("api-key")
    result = client.payment.create_invoice(price_amount=1, price_currency="USD")

    assert result["id"] == "invoice-1"


@patch("requests.Session.request")
def test_api_error_propagates(mock_request):
    from tests.test_base_api import _mock_response

    mock_request.return_value = _mock_response(
        status_code=403,
        text='{"message": "Invalid api key"}',
        json_data={"message": "Invalid api key"},
    )

    client = NowPayments("bad-key")
    with pytest.raises(NowPaymentsAPIError) as exc_info:
        client.currency.get_available_currencies()

    assert exc_info.value.status_code == 403
