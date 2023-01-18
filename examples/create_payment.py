from nowpayment import NowPayments

api = NowPayments("API_KEY")

payment = api.payment.create_payment(
    price_amount=10,
    price_currency="USD",
    pay_currency="TRX",
    order_id="74364712",
    ipn_callback_url="https://nowpayments.io",

    # Optional parameters
    # See: https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest#5e37f3ad-0fa1-4292-af51-5c7f95730486
    order_description="Test payment"
)
print(payment)
