from nowpayment import NowPayments

api = NowPayments("API_KEY")

print(api.payout.get_balance())
