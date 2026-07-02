from typing import List, Optional, Union

from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required
from nowpayment.models import (
    AddressValidation,
    AuthToken,
    Balance,
    Payout,
    PayoutFee,
    PayoutVerification,
    WithdrawalModel,
    parse_response,
)


class PayoutAPI(BaseAPI):

    def login(
        self,
        email: str,
        password: str,
        as_model: bool = False,
    ) -> Union[dict, AuthToken]:
        """
        Log in to the payout system and obtain a JWT token.

        :param email: Account email.
        :param password: Account password.
        :param as_model: When True, return an ``AuthToken`` model.
        :return: Auth response containing a JWT token.
        """
        data = {
            'email': email,
            'password': password
        }
        response = self._request('POST', "auth", json=data)
        return parse_response(response, AuthToken, as_model)

    @jwt_required
    def create_payout(
            self,
            withdrawals: Union[List[WithdrawalModel], WithdrawalModel],
            ipn_callback_url: str,
            as_model: bool = False,
    ) -> Union[dict, Payout]:
        """
        Create a payout batch.

        :param withdrawals: One or more ``WithdrawalModel`` instances.
        :param ipn_callback_url: IPN callback URL for the batch.
        :param as_model: When True, return a ``Payout`` model.
        :return: Payout response.
        """
        if isinstance(withdrawals, list):
            withdrawals = [w.to_dict() for w in withdrawals]
        else:
            withdrawals = [withdrawals.to_dict()]

        if len(withdrawals) == 0:
            raise ValueError(
                'withdrawals cannot be empty. Should be a list of WithdrawalModel or a single WithdrawalModel.'
            )
        response = self._request(
            'POST',
            "payout",
            json={
                "ipn_callback_url": ipn_callback_url,
                "withdrawals": withdrawals,
            },
        )
        return parse_response(response, Payout, as_model)

    def get_payout_status(
        self,
        payout_id: str,
        as_model: bool = False,
    ) -> Union[dict, Payout]:
        """
        Get payout status.

        :param payout_id: Payout ID.
        :param as_model: When True, return a ``Payout`` model.
        :return: Payout status response.
        """
        data = self._request('GET', f"payout/{payout_id}")
        return parse_response(data, Payout, as_model)

    def get_balance(self, as_model: bool = False) -> Union[dict, Balance]:
        """
        Get account balance by currency.

        :param as_model: When True, return a ``Balance`` model.
        :return: Balance response.
        """
        data = self._request('GET', "balance")
        if as_model:
            return Balance.from_dict(data)
        return data

    def validate_address(
        self,
        address: str,
        currency: str,
        extra_id: Optional[str] = None,
        as_model: bool = False,
    ) -> Union[dict, AddressValidation]:
        """
        Validate a cryptocurrency address before creating a payout.

        :param address: Wallet address.
        :param currency: Currency ticker.
        :param extra_id: Optional memo/tag for the address.
        :param as_model: When True, return an ``AddressValidation`` model.
        :return: Validation response.
        """
        payload = {"address": address, "currency": currency}
        if extra_id is not None:
            payload["extra_id"] = extra_id
        data = self._request('POST', "payout/validate-address", json=payload)
        return parse_response(data, AddressValidation, as_model)

    def get_payout_fee(
        self,
        currency: str,
        amount: Union[int, float],
        as_model: bool = False,
    ) -> Union[dict, PayoutFee]:
        """
        Estimate the network fee for a payout.

        :param currency: Currency ticker.
        :param amount: Payout amount.
        :param as_model: When True, return a ``PayoutFee`` model.
        :return: Fee estimate response.
        """
        params = {"currency": currency, "amount": amount}
        data = self._request('GET', "payout/fee", params=params)
        return parse_response(data, PayoutFee, as_model)

    @jwt_required
    def cancel_payout(
        self,
        withdrawal_id: str,
        as_model: bool = False,
    ) -> Union[dict, PayoutVerification]:
        """
        Cancel a scheduled payout.

        :param withdrawal_id: Withdrawal or batch ID to cancel.
        :param as_model: When True, return a ``PayoutVerification`` model.
        :return: Cancellation response.
        """
        data = self._request('POST', f"payout/{withdrawal_id}/cancel")
        return parse_response(data, PayoutVerification, as_model)

    @jwt_required
    def verify_payout(
        self,
        verification_code: str,
        withdrawals_id: Optional[str] = None,
        *,
        payout_id: Optional[str] = None,
        as_model: bool = False,
    ) -> Union[dict, PayoutVerification]:
        """
        Verify a payout with a 2FA verification code.

        :param verification_code: Verification code from email or authenticator.
        :param withdrawals_id: Payout or batch withdrawal ID.
        :param payout_id: Alias for ``withdrawals_id``.
        :param as_model: When True, return a ``PayoutVerification`` model.
        :return: Payout verification response.
        """
        batch_id = withdrawals_id or payout_id
        if not batch_id:
            raise ValueError("withdrawals_id or payout_id is required")
        data = self._request(
            'POST',
            f"payout/{batch_id}/verify",
            json={"verification_code": verification_code},
        )
        return parse_response(data, PayoutVerification, as_model)
