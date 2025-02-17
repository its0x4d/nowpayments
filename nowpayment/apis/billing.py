from typing import Union, List

from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required


class BillingAPI(BaseAPI):

    @jwt_required
    def create_new_user_account(
            self,
            name: str,
            **kwargs
    ) -> dict:
        """
        Create new user account
        This is a method to create an account for your user. After this you'll be able to generate a payment or deposit for topping up its balance as well as withdraw funds from it.

        :param name: a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
        :return: User.
        :rtype: dict
        """
        data = {
            "name": name,
            **kwargs
        }
        return self._request('POST', "sub-partner/balance", json=data)

    @jwt_required
    def create_recurring_payments(
            self,
            subscription_plan_id: int,
            sub_partner_id: int,
            **kwargs
    ) -> dict:
        """
        Create recurring payments
        This method creates a recurring charge from a user account.

        The funds are transferred from a user account to your account when a new payment is generated or a paid period is coming to an end. The amount depends on the plan a customer chooses.
        If you specify a particular currency your customer should pay in, and their account have enough funds stored in it, the amount will be charged automatically. In case a customer has other currency on their account, the equivalent sum will be charged.

        Here is the list of available statuses:
            WAITING_PAY - the payment is waiting for user's deposit;
            PAID - the payment is completed;
            PARTIALLY_PAID - the payment is completed, but the final amount is less than required for payment to be fully paid;
            EXPIRED - is being assigned to unpaid payment after 7 days of waiting;
        Please note:
            Subscribtion amount will be deducted from your sub-user balance in any currency available; i.e. if your subscribtion plan is set up for 100USDTTRC20/month, and your customer has 100USDCMATIC on balance, USDCMATIC will be deducted and transferred to your custody.
            You can convert it manually using our conversions endpoints through api or in your Custody dashboard.

        :param subscription_plan_id: a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
        :param sub_partner_id: (user id) a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
        :return: Recurring payment.
        :rtype: dict
        """
        data = {
            "subscription_plan_id": subscription_plan_id,
            "sub_partner_id": sub_partner_id,
            **kwargs
        }
        return self._request('POST', "sub-partner/balance", json=data)

    def get_user_balance(self, sub_partner_id: int) -> dict:
        """
        Get user balance

        This request can be made only from a whitelisted IP.
        If IP whitelisting is disabled, this request can be made by any user that has an API key.

        :param sub_partner_id: ID of sub-user for balance request
        :return: User balance.
        :rtype: dict
        """
        return self._request('GET', f"sub-partner/balance/{sub_partner_id}")

    @jwt_required
    def get_users(
            self,
            sub_partner_id: Union[int, List[int]],
            offset: Union[None, int] = None,
            limit: Union[None, int] = None,
            order: Union[None, str] = None
    ) -> dict:
        """
        Get users
        This method returns the entire list of your sub-partners.

        :param sub_partner_id: int or array of int (optional)
        :param offset: (optional) default 0
        :param limit: (optional) default 10
        :param order: ASC / DESC (optional) default ASC
        :return: Users.
        :rtype: dict
        """
        path = "sub-partner?"

        if isinstance(sub_partner_id, int):
            path += f"id={sub_partner_id}"
        elif isinstance(sub_partner_id, list):
            path += f"id={",".join([str(i) for i in sub_partner_id])}"
        else:
            raise ValueError("id must be int or list of int")
        if offset:
            path += f"&offset={offset}"
        if limit:
            path += f"&limit={limit}"
        if order:
            path += f"&order={order}"

        return self._request('GET', path)

    def get_all_transfers(
            self,
            sub_partner_id: Union[int, List[int]],
            status: Union[str, List[str]],
            limit: Union[None, int] = None,
            offset: Union[None, int] = None,
            order: Union[None, str] = None
    ) -> dict:
        """
        Get all transfers
        Returns the entire list of transfers created by your users.

        The list of available statuses:
            CREATED - the transfer is being created;
            WAITING - the transfer is waiting for payment;
            FINISHED - the transfer is completed;
            REJECTED - for some reason, transaction failed;

        :param sub_partner_id: int or array of int (optional)
        :param status: string or array of string "WAITING"/"CREATED"/"FINISHED"/"REJECTED" (optional)
        :param limit: (optional) default 10
        :param offset: (optional) default 0
        :param order: ASC / DESC (optional) default ASC
        :return: User transfers.
        :rtype: dict
        """

        path = "sub-partner/transfers"
        add_path = ""

        if not sub_partner_id:
            pass
        elif isinstance(sub_partner_id, int):
            add_path += f"id={sub_partner_id}"
        elif isinstance(sub_partner_id, list):
            add_path += f"id={",".join([str(i) for i in sub_partner_id])}"
        else:
            raise ValueError("id may be int or list of int")
        if isinstance(status, str):
            add_path += f"&status={status}"
        elif isinstance(status, list):
            add_path += f"&status={",".join(status)}"
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
            from_id: Union[int, str],
            to_id: Union[int, str],
            **kwargs
    ) -> dict:
        """
        Transfer
        This method allows creating transfers between users' accounts.

        You can check the transfer's status using Get transfer method.
        The list of available statuses:
            CREATED - the transfer is being created;
            WAITING - the transfer is waiting for payment;
            FINISHED - the transfer is completed;
            REJECTED - for some reason, transaction failed;

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
            "from_id": str(from_id),
            "to_id": str(to_id),
            **kwargs
        }
        return self._request('POST', "sub-partner/transfer", json=data)

    @jwt_required
    def deposit_with_payment(
        self,
        currency: str,
        amount: float,
        sub_partner_id: Union[int, str],
        is_fixed_rate: Union[None, bool] = None,
        is_fee_paid_by_user: Union[None, bool] = None,
        ipn_callback_url: Union[None, str] = None,
        **kwargs
    ) -> dict:
        """
        Deposit with payment
        This method allows you to top up a sub-partner account with a general payment.
        You can check the actual payment status by using GET 9 Get payment status request.

        :param currency:
        :param amount:
        :param sub_partner_id:
        :param is_fixed_rate:
        :param is_fee_paid_by_user:
        :param ipn_callback_url:
        :return: Deposit with payment.
        :rtype: dict
        """
        data = {
            "currency": currency,
            "amount": amount,
            "sub_partner_id": str(sub_partner_id),
            **kwargs
        }
        if is_fixed_rate is not None:
            data["is_fixed_rate"] = is_fixed_rate
        if is_fee_paid_by_user is not None:
            data["is_fee_paid_by_user"] = is_fee_paid_by_user
        if ipn_callback_url:
            data["ipn_callback_url"] = ipn_callback_url
        return self._request('POST', "sub-partner/payment", json=data)

    @jwt_required
    def get_user_payments(
        self,
        sub_partner_id: int,
        limit: Union[None, int] = None,
        page: Union[None, int] = None,
        payment_id: Union[None, int] = None,
        pay_currency: Union[None, str] = None,
        status: Union[None, str] = None,
        date_from: Union[None, str] = None,
        date_to: Union[None, str] = None,
        orderBy: Union[None, str] = None,
        sortBy: Union[None, str] = None
    ) -> dict:
        """
        Get user payments
        This method returns the entire list of payments created by your users.

        :param sub_partner_id: Sub-partner ID.
        :param limit: Amount of listed results.
        :param page: Set the offset for listed results.
        :param payment_id: Filter by payment ID.
        :param pay_currency: Filter by deposit currency.
        :param status: Filter by status.
        :param date_from: Filter by date (from).
        :param date_to: Filter by date (to).
        :param orderBy: Set the order for listed results (asc, desc).
        :param sortBy: Sort results by 'id', 'status', 'pay_currency', 'created_at', 'updated_at'.
        :return: User payments.
        :rtype: dict
        """
        data = {
            "sub_partner_id": sub_partner_id,
        }
        if limit:
            data["limit"] = limit
        if page:
            data["page"] = page
        if id:
            data["id"] = payment_id
        if pay_currency:
            data["pay_currency"] = pay_currency
        if status:
            data["status"] = status
        if date_from:
            data["date_from"] = date_from
        if date_to:
            data["date_to"] = date_to
        if orderBy:
            data["orderBy"] = orderBy
        if sortBy:
            data["sortBy"] = sortBy
        return self._request('GET', "sub-partner/payments", json=data)

    @jwt_required
    def deposit_from_master_account(
        self,
        currency: str,
        amount: float,
        sub_partner_id: Union[int, str],
        **kwargs
    ) -> dict:
        """
        Deposit from your master account
        This is a method for transferring funds from your master account to a user's one.

        The actual information about the transfer's status can be obtained via Get transfer method.
        The list of available statuses:
            CREATED - the transfer is being created;
            WAITING - the transfer is waiting for payment;
            FINISHED - the transfer is completed;
            REJECTED - for some reason, transaction failed;

        :param currency: Currency.
        :param amount: Amount.
        :param sub_partner_id: Sub-partner ID.
        :return: Deposit from master account.
        :rtype: dict
        """
        data = {
            "currency": currency,
            "amount": amount,
            "sub_partner_id": str(sub_partner_id),
            **kwargs
        }
        return self._request('POST', "sub-partner/deposit", json=data)

    @jwt_required
    def write_off_on_master_account(
        self,
        currency: str,
        amount: float,
        sub_partner_id: Union[int, str],
        **kwargs
    ) -> dict:
        """
        Write off on your account
        With this method you can withdraw funds from a user's account and transfer them to your master account.

        The actual status of the transaction can be checked with Get transfer method.
        The list of available statuses:
            CREATED - the transfer is being created;
            WAITING - the transfer is waiting for payment;
            FINISHED - the transfer is completed;
            REJECTED - for some reason, transaction failed;

        :param currency:
        :param amount:
        :param sub_partner_id:
        :return:
        :rtype: dict
        """
        data = {
            "currency": currency,
            "amount": amount,
            "sub_partner_id": str(sub_partner_id),
            **kwargs
        }
        return self._request('POST', "sub-partner/write-off", json=data)

    # Aliases from another docs
    create_new_subpartner = create_new_user_account
    create_subpartner_recurring_payments = create_recurring_payments
    get_subpartner_balance = get_user_balance
    get_subpartners = get_users
    get_subpartner_transfers = get_all_transfers
