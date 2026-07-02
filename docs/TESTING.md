# Testing NOWPayments endpoints

This project supports **three levels** of testing: fast unit tests (mocked), sandbox integration tests (real API), and manual end-to-end checks (payments, IPN, payouts).

## 1. Unit tests (recommended for development)

Unit tests mock HTTP and never call NOWPayments. Run them on every change:

```bash
pip install -e ".[dev]"
pytest
```

Run a single file or test:

```bash
pytest tests/test_subscriptions.py -v
pytest tests/test_payout.py::test_validate_address -v
```

With coverage:

```bash
pytest --cov=nowpayment --cov-report=term-missing
```

### How unit tests work

Tests patch `requests.Session.request` and return fake JSON:

```python
from unittest.mock import patch

@patch("requests.Session.request")
def test_create_plan(mock_request, mock_response):
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
    assert plan.title == "Pro"
```

Add a new test whenever you add or fix an endpoint.

---

## 2. Sandbox integration tests (real API)

Use the **NOWPayments sandbox** to hit real endpoints without production money.

### Setup

1. Create a sandbox account: https://account-sandbox.nowpayments.io/
2. Generate a sandbox API key in the dashboard.
3. Copy `.env.example` to `.env` and set:

```bash
NOWPAYMENTS_SANDBOX_API_KEY=your_sandbox_key
```

### Run integration tests

```bash
export NOWPAYMENTS_SANDBOX_API_KEY=your_sandbox_key
pytest -m integration
```

These tests only run when the env var is set. They use read-only or low-risk calls (`status`, `currencies`, `estimate`).

### Smoke test script

For a quick manual check of several endpoints:

```bash
export NOWPAYMENTS_SANDBOX_API_KEY=your_sandbox_key
python examples/sandbox_smoke_test.py
```

### Sandbox client in code

```python
from nowpayment import NowPayments

client = NowPayments("SANDBOX_API_KEY", sandbox=True)
print(client.get_api_status())
print(client.currency.get_available_currencies())
```

Sandbox base URL: `https://api.sandbox.nowpayments.io/v1`

---

## 3. Testing write endpoints (payments, payouts, subscriptions)

Some endpoints create real resources even in sandbox.

| Endpoint | Auth | How to test safely |
|----------|------|-------------------|
| `payment.create_payment` | API key | Use sandbox + small amount + your `ipn_callback_url` |
| `payment.create_invoice` | API key | Same; open `invoice_url` from response |
| `payout.login` | email/password | Sandbox account credentials |
| `payout.create_payout` | API key + JWT + 2FA | Login → create → verify with email code |
| `payout.validate_address` | API key | Safe; no funds moved |
| `payout.get_payout_fee` | API key | Safe; read-only estimate |
| `subscription.create_plan` | API key + JWT | Requires JWT from `payout.login` |
| `subscription.create_subscription` | API key + JWT | Email or `sub_partner_id` |

### Payout flow (sandbox)

```python
from nowpayment import NowPayments
from nowpayment.models import WithdrawalModel

client = NowPayments("SANDBOX_API_KEY", sandbox=True)

login = client.payout.login(email="...", password="...", as_model=True)
client.jwt_token = login.token

# Optional: validate address first
client.payout.validate_address(address="T...", currency="trx")

# Optional: fee estimate
client.payout.get_payout_fee(currency="trx", amount=10)

payout = client.payout.create_payout(
    withdrawals=WithdrawalModel(
        address="T...",
        currency="trx",
        amount=10,
        ipn_callback_url="https://your-server/ipn",
    ),
    ipn_callback_url="https://your-server/ipn",
)

# Check email for 2FA code, then:
client.payout.verify_payout(
    payout_id=payout.id,
    verification_code="123456",
)
```

### Subscription flow (sandbox)

```python
login = client.payout.login(email="...", password="...", as_model=True)
client.jwt_token = login.token

plan = client.subscription.create_plan(
    title="Monthly",
    interval_day=30,
    amount=9.99,
    currency="usd",
    as_model=True,
)

subscription = client.subscription.create_subscription(
    subscription_plan_id=plan.id,
    email="customer@example.com",
    as_model=True,
)
```

---

## 4. Testing IPN webhooks

NOWPayments sends POST callbacks to your `ipn_callback_url` with header `x-nowpayments-sig`.

### Local webhook server

```bash
export NOWPAYMENTS_IPN_SECRET=your_ipn_secret_from_dashboard
python examples/webhook_server.py
```

Expose it with [ngrok](https://ngrok.com/) or similar:

```bash
ngrok http 8080
# Use https://xxxx.ngrok.io as ipn_callback_url
```

### Verify in your app

```python
from nowpayment import extract_ipn_signature, verify_ipn_payload

def handle_ipn(request):
    payload = request.json()
    signature = extract_ipn_signature(request.headers)
    verified = verify_ipn_payload(payload, IPN_SECRET, signature)
    # process verified["payment_status"], etc.
```

### Unit test IPN verification

```bash
pytest tests/test_webhooks.py tests/test_signature.py -v
```

---

## 5. CI vs local integration tests

- **GitHub Actions CI** runs unit tests only (no secrets required).
- **Integration tests** (`pytest -m integration`) are opt-in via `NOWPAYMENTS_SANDBOX_API_KEY`.

Never commit `.env` or API keys. Use repository secrets if you later add sandbox tests to CI.

---

## 6. Debugging API errors

```python
from nowpayment import NowPaymentsAPIError

try:
    client.payment.get_payment_status("bad-id")
except NowPaymentsAPIError as exc:
    print(exc.status_code)
    print(exc.message)
    print(exc.response)  # raw JSON body when available
```

---

## Quick reference

| Goal | Command |
|------|---------|
| Fast tests | `pytest` |
| Sandbox integration | `NOWPAYMENTS_SANDBOX_API_KEY=... pytest -m integration` |
| Manual sandbox check | `python examples/sandbox_smoke_test.py` |
| Local IPN server | `python examples/webhook_server.py` |
| Lint | `ruff check nowpayment tests` |
