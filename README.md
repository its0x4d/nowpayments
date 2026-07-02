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

## Testing

See **[docs/TESTING.md](docs/TESTING.md)** for the full guide. Quick start:

```bash
# Unit tests (mocked, no API key needed)
pip install -e ".[dev]"
pytest

# Sandbox integration tests (real API)
export NOWPAYMENTS_SANDBOX_API_KEY=your_sandbox_key
pytest -m integration

# Manual smoke test
python examples/sandbox_smoke_test.py
```

Copy `.env.example` to `.env` for local sandbox credentials (never commit `.env`).

## Quick start

```python
from nowpayment import NowPayments

# Production
np = NowPayments("API_KEY")

# Sandbox
np = NowPayments("SANDBOX_API_KEY", sandbox=True)

# Reuse a single HTTP session
with NowPayments("API_KEY") as client:
    invoice = client.payment.create_invoice(
        price_amount=1,
        price_currency="USD",
        as_model=True,
    )
    print(invoice.invoice_url)
```

## Response models

By default, API methods return plain `dict` responses for backward compatibility.
Pass `as_model=True` to get typed dataclass models with a `.raw` field for the full payload.

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

assert isinstance(payment, Payment)
print(payment.payment_status)

# Or parse manually
payment = Payment.from_dict(np.payment.get_payment_status("123"))
```

## Webhooks (IPN)

```python
from nowpayment import extract_ipn_signature, verify_ipn_payload, IPNVerificationError

def handle_request(headers, body: dict, ipn_secret: str):
    signature = extract_ipn_signature(headers)
    try:
        event = verify_ipn_payload(body, ipn_secret, signature)
    except IPNVerificationError:
        return 401
    return event
```

Local testing: `python examples/webhook_server.py` (see [docs/TESTING.md](docs/TESTING.md)).

## Error handling

API failures raise `NowPaymentsAPIError` with `status_code`, `message`, and parsed `response` when available.

```python
from nowpayment import NowPayments, NowPaymentsAPIError

np = NowPayments("API_KEY")

try:
    np.payment.get_payment_status("invalid-id")
except NowPaymentsAPIError as exc:
    print(exc.status_code, exc.message)
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check nowpayment tests
```

## Releasing to PyPI

Publishing runs via [`.github/workflows/publish.yml`](.github/workflows/publish.yml) when you **publish a GitHub Release**, or manually from the Actions tab (`workflow_dispatch`).

### One-time setup (trusted publishing — recommended)

1. On [PyPI](https://pypi.org/manage/account/publishing/), add a **trusted publisher**:
   - PyPI project: `nowpayment`
   - Owner: `its0x4d`
   - Repository: `nowpayments`
   - Workflow: `publish.yml`
   - Environment: `pypi`
2. On GitHub → **Settings → Environments**, create environment **`pypi`** (optional protection rules).

No API token is required when trusted publishing is configured.

### Fallback: API token

Add repository secret **`PYPI_API_TOKEN`** (PyPI → Account → API tokens). The publish action uses it if trusted publishing is not set up.

### Release steps

1. Bump `version` in `pyproject.toml` and `nowpayment/__init__.py` (keep in sync).
2. Update `CHANGELOG.md`.
3. Commit, push, and create a GitHub Release with tag **`v1.9.0`** (must match `pyproject.toml` version without the `v`).
4. The workflow builds with `python -m build` and uploads to PyPI.

```bash
git tag v1.9.0
git push origin v1.9.0
# Then create the release on GitHub for that tag
```

## Examples

```python
from nowpayment import NowPayments

np = NowPayments("API_KEY")

invoice = np.payment.create_invoice(
    price_amount=1,
    price_currency="USD",
)

currencies = np.currency.get_available_currencies()
```

If you're looking for more detailed examples, check out the [examples](https://github.com/its0x4d/nowpayments/tree/main/examples).
