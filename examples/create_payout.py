from nowpayment import NowPayments
from nowpayment.models import WithdrawalModel

api = NowPayments("API_KEY")

EMAIL = "EMAIL"
PASSWORD = "PASSWORD"
TO_ADDRESS = "TO_ADDRESS"  # Address to send to
CURRENCY = "TRX"  # Currency to send


# First we should log in using email and password
login = api.payout.login(email=EMAIL, password=PASSWORD)
# if the login is successful, we will get a token in the response
# we will use this token to fill the `jwt_token` parameter

# if not successful, we will get an error message
if not login.get("token"):
    raise Exception("Login failed. Check your email and password.")

api.jwt_token = login["token"]

payout = api.payout.create_payout(
    withdrawals=[
        WithdrawalModel(
            amount=5.0,
            address=TO_ADDRESS,
            currency=CURRENCY,
            # The IPN callback URL is an url that will be called when the payout is done
            ipn_callback_url="https://nowpayments.io",
        )
    ],
    ipn_callback_url="https://nowpayments.io",
)

print(payout)

# The response will be a dictionary with the following keys
# See: https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest#21331cbf-c7c0-45ff-9709-0653f31d3803
# {
#   "id": "5000000713",
#   "withdrawals": [
#     {
#       "id": "5000000000",
#       "address": "TEmGwPeRTPiLFLVfBxXkSP91yc5GMNQhfS",
#       "currency": "trx",
#       "amount": "200",
#       "batchWithdrawalId": "5000000000",
#       "status": "WAITING",
#       "extra_id": null,
#       "hash": null,
#       "error": null,
#       "createdAt": "2020-11-12T17:06:12.791Z",
#       "requestedAt": null,
#       "updatedAt": null
#     },
#     ...
#     ],
# }
#
