"""
NowPayments.io Python Client
"""

__version__ = "1.9.0"

from typing import Optional, Union

import requests

from nowpayment.apis.billing import BillingAPI
from nowpayment.apis.currencies import CurrencyAPI
from nowpayment.apis.payment import PaymentAPI
from nowpayment.apis.payout import PayoutAPI
from nowpayment.apis.subscriptions import SubscriptionAPI
from nowpayment.constants import PRODUCTION_BASE_URL, SANDBOX_BASE_URL
from nowpayment.exceptions import NowPaymentsAPIError, NowPaymentsError
from nowpayment.models import (
    AddressValidation,
    APIStatus,
    AuthToken,
    Balance,
    Currency,
    CurrencyList,
    Estimate,
    Invoice,
    MinAmount,
    Payment,
    PaymentList,
    Payout,
    PayoutFee,
    PayoutVerification,
    Subscription,
    SubscriptionList,
    SubscriptionPlan,
    SubscriptionPlanList,
    WithdrawalModel,
)
from nowpayment.signatures import compute_payment_signature, verify_payment_signature
from nowpayment.webhooks import IPNVerificationError, extract_ipn_signature, verify_ipn_payload

__all__ = [
    "NowPayments",
    "NowPaymentsAPIError",
    "NowPaymentsError",
    "IPNVerificationError",
    "APIStatus",
    "AddressValidation",
    "AuthToken",
    "Balance",
    "Currency",
    "CurrencyList",
    "Estimate",
    "Invoice",
    "MinAmount",
    "Payment",
    "PaymentList",
    "Payout",
    "PayoutFee",
    "PayoutVerification",
    "Subscription",
    "SubscriptionList",
    "SubscriptionPlan",
    "SubscriptionPlanList",
    "WithdrawalModel",
    "extract_ipn_signature",
    "verify_ipn_payload",
    "__version__",
]


class NowPayments:

    def __init__(
        self,
        api_key: str,
        jwt_token: Optional[str] = None,
        timeout: Optional[Union[int, float]] = None,
        sandbox: bool = False,
        session: Optional[requests.Session] = None,
    ):
        self.api_key = api_key
        self.jwt_token = jwt_token
        self.timeout = timeout
        self.sandbox = sandbox
        self.base_url = SANDBOX_BASE_URL if sandbox else PRODUCTION_BASE_URL
        self._session = session
        self._owns_session = session is None

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def _client_kwargs(self) -> dict:
        return {
            "api_key": self.api_key,
            "jwt_token": self.jwt_token,
            "timeout": self.timeout,
            "base_url": self.base_url,
            "session": self.session,
        }

    @property
    def payment(self) -> PaymentAPI:
        return PaymentAPI(**self._client_kwargs())

    @property
    def currency(self) -> CurrencyAPI:
        return CurrencyAPI(**self._client_kwargs())

    @property
    def payout(self) -> PayoutAPI:
        return PayoutAPI(**self._client_kwargs())

    @property
    def billing(self) -> BillingAPI:
        return BillingAPI(**self._client_kwargs())

    @property
    def subscription(self) -> SubscriptionAPI:
        return SubscriptionAPI(**self._client_kwargs())

    def close(self) -> None:
        if self._owns_session and self._session is not None:
            self._session.close()
            self._session = None

    def __enter__(self) -> "NowPayments":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def get_api_status(self, as_model: bool = False) -> Union[dict, APIStatus]:
        """
        Obtain information about the status of the API.

        :param as_model: When True, return an ``APIStatus`` model.
        :return: API status.
        """
        return self.payment.get_api_status(as_model=as_model)

    @staticmethod
    def compute_payment_signature(data: dict, ipn_secret: str) -> str:
        return compute_payment_signature(data, ipn_secret)

    @staticmethod
    def verify_payment_signature(
        data: dict,
        ipn_secret: str,
        signature: Optional[str] = None,
    ) -> Union[str, bool]:
        return verify_payment_signature(data, ipn_secret, signature)
