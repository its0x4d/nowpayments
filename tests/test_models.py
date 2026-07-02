import pytest

from nowpayment.models import (
    Balance,
    Currency,
    CurrencyList,
    Payment,
    PaymentList,
    Payout,
)


def test_payment_from_dict_keeps_raw_payload():
    data = {
        "payment_id": "99",
        "payment_status": "finished",
        "custom_field": "value",
    }
    payment = Payment.from_dict(data)

    assert payment.payment_id == "99"
    assert payment.payment_status == "finished"
    assert payment.raw["custom_field"] == "value"


def test_payment_to_dict_returns_raw_payload():
    payment = Payment.from_dict({"payment_id": "1"})
    assert payment.to_dict() == {"payment_id": "1"}


def test_currency_list_parses_string_and_object_entries():
    result = CurrencyList.from_dict(
        {
            "currencies": [
                "btc",
                {"code": "ETH", "name": "Ethereum", "enable": True},
            ]
        }
    )

    assert result.currencies[0] == "btc"
    assert isinstance(result.currencies[1], Currency)
    assert result.currencies[1].code == "ETH"


def test_payment_list_parses_nested_payments():
    result = PaymentList.from_dict(
        {
            "data": [
                {"payment_id": "1", "payment_status": "waiting"},
                {"payment_id": "2", "payment_status": "finished"},
            ],
            "total": 2,
        }
    )

    assert len(result.data) == 2
    assert result.data[0].payment_id == "1"
    assert result.total == 2


def test_balance_parses_currency_map():
    result = Balance.from_dict(
        {
            "eth": {"amount": 1.5, "pendingAmount": 0.2},
            "trx": {"amount": 0, "pendingAmount": 0},
        }
    )

    assert result.balances["eth"].amount == 1.5
    assert result.balances["eth"].pending_amount == 0.2


def test_payout_parses_withdrawals():
    result = Payout.from_dict(
        {
            "id": "500",
            "withdrawals": [
                {"id": "1", "address": "addr", "currency": "trx", "amount": "10"},
            ],
        }
    )

    assert result.id == "500"
    assert result.withdrawals[0].address == "addr"


def test_from_dict_rejects_non_dict():
    with pytest.raises(TypeError):
        Payment.from_dict([])
