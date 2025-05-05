"""
NowPayments.io Python Client
"""

__version__ = "1.6.0"

import hashlib
import hmac
import json

from nowpayment.apis.currencies import CurrencyAPI
from nowpayment.apis.payment import PaymentAPI
from nowpayment.apis.payout import PayoutAPI
from nowpayment.apis.billing import BillingAPI


class NowPayments:

    def __init__(self, api_key: str, jwt_token: str = None, timeout = None):
        self.api_key = api_key
        self.jwt_token = jwt_token
        self.timeout = timeout

    @property
    def payment(self):
        return PaymentAPI(self.api_key, jwt_token=self.jwt_token, timeout=self.timeout)

    @property
    def currency(self):
        return CurrencyAPI(self.api_key, jwt_token=self.jwt_token, timeout=self.timeout)

    @property
    def payout(self):
        return PayoutAPI(self.api_key, jwt_token=self.jwt_token, timeout=self.timeout)

    @property
    def billing(self):
        return BillingAPI(self.api_key, jwt_token=self.jwt_token, timeout=self.timeout)

    def get_api_status(self) -> dict:
        """
        This is a method for obtaining information about the status of the API.

        :return: API status.
        :rtype: dict
        """
        return self.payment.get_api_status()

    @staticmethod
    def verify_payment_signature(data: dict, ipn_secret: str) -> str:
        """
        This is a method for verifying the payment signature.

        :param data: data
        :param ipn_secret: ipn secret
        :return: True if the signature is valid, False otherwise.
        :rtype: bool
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        if not isinstance(ipn_secret, str):
            raise ValueError("IPN secret must be a string")
            
        request_data = dict(sorted(data.items()))
        sorted_request_json = json.dumps(request_data, separators=(',', ':'))
        return hmac.new(
            ipn_secret.encode('utf-8'),
            sorted_request_json.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
