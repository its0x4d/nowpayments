from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required


class PayoutAPI(BaseAPI):

    def create_payout(self, address: str, currency: str, amount: str, **kwargs) -> dict:
        """
        This is the method to create a payout.

        :param address: the address where you want to send funds
        :param currency: payout currency
        :param amount: amount of the payout. Must not exceed 6 decimals (i.e. 0.123456)
        :param kwargs: See: https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest#21331cbf-c7c0-45ff-9709-0653f31d3803
        :return: Payout data.
        :rtype: dict
        """
        url = "https://api.nowpayments.io/v1/payout"
        data = {
            "address": address,
            "currency": currency,
            "amount": amount,
            **kwargs
        }
        data.update(kwargs)
        return self._request('POST', url, data=data)

    def get_payout_status(self, payout_id: str) -> dict:
        """
        This is the method to get the payout status.

        :param payout_id: payout id
        :return: Payout data.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/payout/{payout_id}"
        return self._request('GET', url)

    def get_balance(self) -> dict:
        """
        This is the method to get the payout balance.

        :return: Payout balance.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/balance"
        return self._request('GET', url)

    @jwt_required
    def verify_payout(self, withdrawals_id: str) -> dict:
        """
        This is the method to verify the payout.

        :param withdrawals_id: withdrawals id
        :return: Payout data.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/payout/f{withdrawals_id}/verify"
        return self._request('POST', url)
