from nowpayment import NowPayments

api = NowPayments("API_KEY")

invoice = api.payment.create_invoice(
    price_amount=10,
    price_currency="USD",
)
payment = api.payment.create_invoice_payment(
    invoice_id=invoice["id"],
    pay_currency="TRX"
)
print(payment)
