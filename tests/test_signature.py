import pytest

from nowpayment import NowPayments


def test_compute_payment_signature_is_deterministic():
    data = {"b": 2, "a": 1}
    secret = "ipn-secret"

    first = NowPayments.compute_payment_signature(data, secret)
    second = NowPayments.compute_payment_signature(data, secret)

    assert first == second
    assert isinstance(first, str)
    assert len(first) == 128


def test_verify_payment_signature_without_header_returns_digest():
    data = {"payment_id": "1", "payment_status": "finished"}
    digest = NowPayments.verify_payment_signature(data, "secret")

    assert digest == NowPayments.compute_payment_signature(data, "secret")


def test_verify_payment_signature_with_header_returns_bool():
    data = {"payment_id": "1"}
    secret = "secret"
    digest = NowPayments.compute_payment_signature(data, secret)

    assert NowPayments.verify_payment_signature(data, secret, digest) is True
    assert NowPayments.verify_payment_signature(data, secret, "invalid") is False


def test_compute_payment_signature_validates_inputs():
    with pytest.raises(ValueError, match="dictionary"):
        NowPayments.compute_payment_signature([], "secret")

    with pytest.raises(ValueError, match="string"):
        NowPayments.compute_payment_signature({}, None)
