from nowpayment import NowPayments

api = NowPayments("API_KEY")

EMAIL = "EMAIL"
PASSWORD = "PASSWORD"
PAYOUT_ID = "PAYOUT_ID"
VERIFICATION_CODE = "VERIFICATION_CODE"

# First we should log in using email and password
login = api.payout.login(email=EMAIL, password=PASSWORD)
# if the login is successful, we will get a token in the response
# we will use this token to fill the `jwt_token` parameter

# if not successful, we will get an error message
if not login.get("token"):
    raise Exception("Login failed. Check your email and password.")

api.jwt_token = login["token"]

# You will have 10 attempts to verify the payout. If you fail to verify the payout
# after 10 attempts, the payout will be cancelled.
# You can use the `api.payout.get_payout_status` method to get the payout status

verify = api.payout.verify_payout(payout_id=PAYOUT_ID, verification_code=VERIFICATION_CODE)

if verify.get("status") == "OK":
    print("Payout verified successfully")
else:
    print("Payout verification failed")
