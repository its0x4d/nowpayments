## nowpayment - A payment gateway client for NowPayments.io

## Installation

```bash
pip install nowpayment
```

## Supported APIs

- [x] Payments  API
- [x] Currency API
- [x] Payout API
- [ ] Recurring Payments API
- [ ] Billing API

```python
from nowpayment import NowPayments

# Create a NowPayment instance
np = NowPayments("API_KEY")

# Create Invoice
invoice = np.payment.create_invoice(
    price_amount=1,
    price_currency="USD"
)

# Get Available Currencies
currencies = np.currency.get_available_currencies()

```

