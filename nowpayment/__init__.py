from nowpayment.apis.currencies import CurrencyAPI
from nowpayment.apis.payment import PaymentAPI
from nowpayment.apis.payout import PayoutAPI


class NowPayments:

    def __init__(self, api_key: str, jwt_token: str = None):
        self.api_key = api_key
        self.jwt_token = jwt_token

    @property
    def payment(self):
        return PaymentAPI(self.api_key, self.jwt_token)

    @property
    def currency(self):
        return CurrencyAPI(self.api_key, self.jwt_token)

    @property
    def payout(self):
        return PayoutAPI(self.api_key, self.jwt_token)

    def get_api_status(self) -> dict:
        """
        This is a method for obtaining information about the status of the API.

        :return: API status.
        :rtype: dict
        """
        return self.payment.get_api_status()
