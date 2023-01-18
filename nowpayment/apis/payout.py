import json
from typing import Union, List

from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required
from nowpayment.models import WithdrawalModel


class PayoutAPI(BaseAPI):

    def login(self, email: str, password: str) -> dict:
        """
        This is the method to log in to the payout system.

        :param email: email
        :param password: password
        :return: JWT token.
        :rtype: dict
        """
        data = {
            'email': email,
            'password': password
        }
        data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        return self._request('POST', "auth", data=data, headers=headers)

    @jwt_required
    def create_payout(
            self,
            withdrawals: Union[List[WithdrawalModel], WithdrawalModel],
            ipn_callback_url: str,
    ) -> dict:
        """
        This is the method to create a payout.
        See: https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest#21331cbf-c7c0-45ff-9709-0653f31d3803

        :param withdrawals: Withdrawal data. Should be a list of WithdrawalModel or a single WithdrawalModel.
        :param ipn_callback_url: IPN callback URL.
        :return: Payout data.
        :rtype: dict
        """
        if isinstance(withdrawals, list):
            withdrawals = [w.to_dict() for w in withdrawals]
        else:
            withdrawals = [withdrawals.to_dict()]

        if len(withdrawals) == 0:
            raise ValueError(
                'withdrawals cannot be empty. Should be a list of WithdrawalModel or a single WithdrawalModel.'
            )
        data = json.dumps({
            "ipn_callback_url": ipn_callback_url,
            "withdrawals": withdrawals,
        })
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jwt_token}'
        }
        return self._request('POST', "payout", data=data, headers=headers)

    def get_payout_status(self, payout_id: str) -> dict:
        """
        This is the method to get the payout status.

        :param payout_id: payout id
        :return: Payout data.
        :rtype: dict
        """
        return self._request('GET', f"payout/{payout_id}")

    def get_balance(self) -> dict:
        """
        This is the method to get the payout balance.

        :return: Payout balance.
        :rtype: dict
        """
        return self._request('GET', "balance")

    @jwt_required
    def verify_payout(self, withdrawals_id: str, verification_code: str) -> dict:
        """
        This is the method to verify the payout.

        :param withdrawals_id: withdrawals id
        :param verification_code: verification code
        :return: Payout data.
        :rtype: dict
        """
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jwt_token}'
        }
        data = json.dumps({
            'verification_code': verification_code
        })
        return self._request('POST', f"payout/{withdrawals_id}/verify", data=data, headers=headers)
