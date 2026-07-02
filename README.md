## nowpayment - A payment gateway client for NowPayments.io
![PyPI - Downloads](https://img.shields.io/pypi/dw/nowpayment)
![PyPI](https://img.shields.io/pypi/v/nowpayment)

**[NOWPayments](https://nowpayments.io) is a noncustodial crypto payment gateway that lets you accept payments in 300+ cryptocurrencies with auto coin conversion supported.
The gateway is designed to be simple and fast to integrate, with low fees and no minimum balance required. 
It also supports instant settlement and has a variety of features, including integrated invoices and a donation page builder.**

## Requirements

- Python 3.8+

## Installation

```bash
pip install nowpayment
```

## Supported APIs

- [x] Payments API
- [x] Currency API
- [x] Payout API
- [x] Custody / Billing API (sub-partners)
- [x] Subscriptions API (plans & recurring payments)
- [x] Webhook / IPN verification helpers

## Quick start

```python
from nowpayment import NowPayments

np = NowPayments("API_KEY")
# np = NowPayments("SANDBOX_API_KEY", sandbox=True)

invoice = np.payment.create_invoice(
    price_amount=1,
    price_currency="USD",
)

currencies = np.currency.get_available_currencies()
```

Pass `as_model=True` on API methods to get typed response models instead of `dict`.

```python
from nowpayment import Payment

payment = np.payment.create_payment(
    price_amount=10,
    price_currency="USD",
    pay_currency="TRX",
    order_id="order-1",
    ipn_callback_url="https://example.com/ipn",
    as_model=True,
)
print(payment.payment_status)
```

## Webhooks (IPN)

```python
from nowpayment import extract_ipn_signature, verify_ipn_payload, IPNVerificationError

signature = extract_ipn_signature(request.headers)
event = verify_ipn_payload(request.json, IPN_SECRET, signature)
```

## Error handling

```python
from nowpayment import NowPayments, NowPaymentsAPIError

try:
    np.payment.get_payment_status("invalid-id")
except NowPaymentsAPIError as exc:
    print(exc.status_code, exc.message)
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

More examples: [examples/](examples/). Testing guide: [docs/TESTING.md](docs/TESTING.md).
