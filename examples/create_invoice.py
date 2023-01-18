from nowpayment import NowPayments

api = NowPayments("API_KEY")

invoice = api.payment.create_invoice(
    price_amount=10,
    price_currency="USD",
)
print(invoice)
