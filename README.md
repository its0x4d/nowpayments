## nowpayment - A payment gateway client for NowPayments.io
![PyPI - Downloads](https://img.shields.io/pypi/dw/nowpayment)
![PyPI](https://img.shields.io/pypi/v/nowpayment)

**[NOWPayments](https://nowpayments.io) is a noncustodial crypto payment gateway that lets you accept payments in 75+ cryptocurrencies and auto coin conversion supported.
The gateway is designed to be simple and fast to integrate, with low fees and no minimum balance required. 
It also supports instant settlement and has a variety of features, including integrated invoices and a donation page builder.**
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
If you're looking for a more detailed example, check out the [examples](https://github.com/its0x4d/nowpayments/tree/main/examples).
