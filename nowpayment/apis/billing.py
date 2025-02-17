from typing import Union, List

from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required


class BillingAPI(BaseAPI):

    @jwt_required
    def create_new_subpartner(
            self,
            name: str,
            **kwargs
    ) -> dict:
        """
        Create new sub-partner
        This is a method to create a sub-partner account for your user. After this you'll be able to generate a payment(/v1/sub-partner/payment) or deposit(/v1/sub-partner/deposit) for topping up its balance as well as withdraw funds from it.

        :param name: a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
        :return: Sub-partner.
        :rtype: dict
        """
        data = {
            "name": name,
            **kwargs
        }
        return self._request('POST', "sub-partner/balance", json=data)

    @jwt_required
    def create_subpartner_recurring_payments(
            self,
            subscription_plan_id: int,
            sub_partner_id: int,
            **kwargs
    ) -> dict:
        """
        Create sub-partner recurring payments
        This method creates a recurring charge from a sub-account.
        The funds are transferred from a sub-account to the main account when a new payment is generated or a paid period is coming to an end. The amount depends on the plan a customer chooses.
        If you specify a particular currency your customer should pay in, and the sub-account has enough funds stored in it, the amount will be charged automatically. In case a customer has other currency on their sub-account, the equivalent sum will be charged.

        :param subscription_plan_id: a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
        :param sub_partner_id: a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
        :return: Sub-partner recurring payment.
        :rtype: dict
        """
        data = {
            "subscription_plan_id": subscription_plan_id,
            "sub_partner_id": sub_partner_id,
            **kwargs
        }
        return self._request('POST', "sub-partner/balance", json=data)

    def get_subpartner_balance(self, sub_partner_id: int) -> dict:
        """
        Get sub-partner balance
        This request can be made only from a whitelisted IP.
        If IP whitelisting is disabled, this request can be made by any user that has an API key.

        :param sub_partner_id: a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
        :return: Sub-partner balance.
        :rtype: dict
        """
        return self._request('GET', f"sub-partner/balance/{sub_partner_id}")

    # noinspection PyShadowingBuiltins
    @jwt_required
    def get_subpartners(
            self,
            id: Union[int, List[int]],
            offset: Union[None, int] = None,
            limit: Union[None, int] = None,
            order: Union[None, str] = None
    ) -> dict:
        """
        Get sub-partners
        This method returns the entire list of your sub-partners.

        :param id: int or array of int (optional)
        :param offset: (optional) default 0
        :param limit: (optional) default 10
        :param order: ASC / DESC (optional) default ASC
        :return: Sub-partners.
        :rtype: dict
        """

        path = "sub-partner?"

        if id is int:
            path += f"id={id}"
        elif id is list:
            path += f"id={[str(i) for i in id]}"
        else:
            raise ValueError("id must be int or list of int")
        if offset:
            path += f"&offset={offset}"
        if limit:
            path += f"&limit={limit}"
        if order:
            path += f"&order={order}"

        return self._request('GET', path)

    # noinspection PyShadowingBuiltins
    def get_subpartner_transfers(
            self,
            id: Union[int, List[int]],
            status: Union[str, List[str]],
            offset: Union[None, int] = None,
            limit: Union[None, int] = None,
            order: Union[None, str] = None
    ) -> dict:
        """
        Get sub-partner transfers
        This method returns the entire list of transfers created by your sub-partners.

        :param id: int or array of int (optional)
        :param status: string or array of string "WAITING"/"CREATED"/"FINISHED"/"REJECTED" (optional)
        :param offset: (optional) default 0
        :param limit: (optional) default 10
        :param order: ASC / DESC (optional) default ASC
        :return: Sub-partner transfers.
        :rtype: dict
        """

        path = "sub-partner/transfers"
        add_path = ""

        if not id:
            pass
        elif id is int:
            add_path += f"id={id}"
        elif id is list:
            add_path += f"id={[str(i) for i in id]}"
        else:
            raise ValueError("id may be int or list of int")
        if status is str:
            add_path += f"&status={status}"
        elif status is list:
            add_path += f"&status={[str(i) for i in status]}"
        else:
            raise ValueError("status must be str or list of str")
        if offset:
            add_path += f"&offset={offset}"
        if limit:
            add_path += f"&limit={limit}"
        if order:
            add_path += f"&order={order}"

        if add_path:
            path += "?" + add_path

        return self._request('GET', path)

    def get_transfer(self, transfer_id: int) -> dict:
        """
        Get transfer
        Get the actual information about the transfer. You need to provide the transfer ID in the request.

        :param transfer_id: Transfer ID.
        :return: Transfer.
        :rtype: dict
        """
        return self._request('GET', f"sub-partner/transfer/{transfer_id}")

    @jwt_required
    def transfer(
            self,
            currency: str,
            amount: float,
            from_id: int,
            to_id: int,
            **kwargs
    ) -> dict:
        """
        Transfer
        This method allows creating transfers between sub-partners' accounts.
        You can check the transfer's status using Get transfer method.

        :param currency: Currency.
        :param amount: Amount.
        :param from_id: From ID.
        :param to_id: To ID.
        :return: Transfer.
        :rtype: dict
        """
        data = {
            "currency": currency,
            "amount": amount,
            "from_id": from_id,
            "to_id": to_id,
            **kwargs
        }
        return self._request('POST', "sub-partner/transfer", json=data)

    @jwt_required
    def deposit_with_payment(
        self,
        currency: str,
        amount: float,
        sub_partner_id: int,
        fixed_rate: bool,
        **kwargs
    ) -> dict:
        """
        Deposit with payment
        This method allows you to top up a sub-partner account with a general payment.
        You can check the actual payment status by using GET 9 Get payment status request.

        :param currency: Currency.
        :param amount: Amount.
        :param sub_partner_id: Sub-partner ID.
        :param fixed_rate: Fixed rate.
        :return: Deposit with payment.
        :rtype: dict
        """
        data = {
            "currency": currency,
            "amount": amount,
            "sub_partner_id": sub_partner_id,
            "fixed_rate": fixed_rate,
            **kwargs
        }
        return self._request('POST', "sub-partner/payment", json=data)

    @jwt_required
    def deposit_from_master_account(
        self,
        currency: str,
        amount: float,
        sub_partner_id: int,
        **kwargs
    ) -> dict:
        """
        Deposit from master account
        This is a method for transferring funds from a master account to a sub-partner's one.
        The actual information about the transfer's status can be obtained via Get transfer method.

        :param currency: Currency.
        :param amount: Amount.
        :param sub_partner_id: Sub-partner ID.
        :return: Deposit from master account.
        :rtype: dict
        """
        data = {
            "currency": currency,
            "amount": amount,
            "sub_partner_id": sub_partner_id,
            **kwargs
        }
        return self._request('POST', "sub-partner/deposit", json=data)

    @jwt_required
    def write_off_on_master_account(
        self,
        currency: str,
        amount: float,
        sub_partner_id: int,
        **kwargs
    ) -> dict:
        """
        Write off on master account
        With this method you can withdraw funds from a sub-partner's account and transfer them to a master one.

        The actual status of the transaction can be checked with Get transfer method.

        :param currency: Currency.
        :param amount: Amount.
        :param sub_partner_id: Sub-partner ID.
        :return: Write off on master account.
        :rtype: dict
        """
        data = {
            "currency": currency,
            "amount": amount,
            "sub_partner_id": sub_partner_id,
            **kwargs
        }
        return self._request('POST', "sub-partner/write-off", json=data)
