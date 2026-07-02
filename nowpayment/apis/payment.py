from typing import Union

from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required
from nowpayment.models import (
    APIStatus,
    Estimate,
    Invoice,
    MinAmount,
    Payment,
    PaymentList,
    parse_response,
)


class PaymentAPI(BaseAPI):

    def get_estimated_price(
            self,
            amount: Union[int, float],
            from_currency: str,
            to_currency: str,
            as_model: bool = False,
            **kwargs
    ) -> Union[dict, Estimate]:
        """
        Get estimated price.

        :param amount: Amount of money.
        :param from_currency: Currency of money.
        :param to_currency: Currency of money.
        :param as_model: When True, return an ``Estimate`` model.
        :return: Estimated price.
        """
        params = {
            "amount": amount,
            "currency_from": from_currency,
            "currency_to": to_currency,
            **kwargs
        }
        data = self._request('GET', "estimate", params=params)
        return parse_response(data, Estimate, as_model)

    def create_payment(
            self,
            price_amount: Union[int, float],
            price_currency: str,
            pay_currency: str,
            ipn_callback_url: str,
            order_id: str,
            as_model: bool = False,
            **kwargs
    ) -> Union[dict, Payment]:
        """
        Create payment.

        :param price_amount: Fiat equivalent of the price to be paid in crypto.
        :param price_currency: Fiat currency of ``price_amount`` (usd, eur, etc).
        :param pay_currency: Cryptocurrency ticker (btc, eth, etc).
        :param ipn_callback_url: Callback URL for IPN notifications.
        :param order_id: Internal store order ID.
        :param as_model: When True, return a ``Payment`` model.
        :return: Payment response.
        """
        data = {
            "price_amount": price_amount,
            "price_currency": price_currency,
            "pay_currency": pay_currency,
            "order_id": order_id,
            "ipn_callback_url": ipn_callback_url,
            **kwargs
        }
        response = self._request('POST', "payment", json=data)
        return parse_response(response, Payment, as_model)

    def create_invoice_payment(
            self,
            invoice_id: str,
            pay_currency: str,
            as_model: bool = False,
            **kwargs
    ) -> Union[dict, Payment]:
        """
        Create invoice payment.

        :param invoice_id: Invoice ID.
        :param pay_currency: Cryptocurrency ticker.
        :param as_model: When True, return a ``Payment`` model.
        :return: Invoice payment response.
        """
        data = {
            "iid": invoice_id,
            "pay_currency": pay_currency,
            **kwargs
        }
        response = self._request('POST', "invoice-payment", json=data)
        return parse_response(response, Payment, as_model)

    def get_payment_estimated(
            self,
            payment_id: str,
            as_model: bool = False,
    ) -> Union[dict, Payment]:
        """
        Get payment estimated.

        :param payment_id: Payment ID.
        :param as_model: When True, return a ``Payment`` model.
        :return: Payment estimate response.
        """
        data = self._request('POST', f"payment/{payment_id}/update-merchant-estimate")
        return parse_response(data, Payment, as_model)

    def get_payment_status(
            self,
            payment_id: str,
            as_model: bool = False,
    ) -> Union[dict, Payment]:
        """
        Get payment status.

        :param payment_id: Payment ID.
        :param as_model: When True, return a ``Payment`` model.
        :return: Payment status response.
        """
        data = self._request('GET', f"payment/{payment_id}")
        return parse_response(data, Payment, as_model)

    def get_minimum_payment_amount(
            self,
            from_currency: str,
            to_currency: str,
            as_model: bool = False,
            **kwargs
    ) -> Union[dict, MinAmount]:
        """
        Get minimum payment amount.

        :param from_currency: Source currency.
        :param to_currency: Target currency.
        :param as_model: When True, return a ``MinAmount`` model.
        :return: Minimum amount response.
        """
        params = {
            "currency_from": from_currency,
            "currency_to": to_currency,
            "fiat_equivalent": "usd",
            **kwargs
        }
        data = self._request('GET', "min-amount", params=params)
        return parse_response(data, MinAmount, as_model)

    @jwt_required
    def get_payment_list(
            self,
            limit: int = 10,
            page: int = 0,
            sort_by: str = 'created_at',
            order_by: str = 'desc',
            date_from: str = None,
            date_to: str = None,
            as_model: bool = False,
            **kwargs
    ) -> Union[dict, PaymentList]:
        """
        Get payment list.

        :param limit: Limit.
        :param page: Page.
        :param sort_by: Sort by.
        :param order_by: Order by.
        :param date_from: Date from. e.g. "2019-01-01"
        :param date_to: Date to. e.g. "2019-01-01"
        :param as_model: When True, return a ``PaymentList`` model.
        :return: Payment list response.
        """
        params = {
            "limit": limit,
            "page": page,
            "sortBy": sort_by,
            "orderBy": order_by,
            "dateFrom": date_from,
            "dateTo": date_to,
            **kwargs
        }
        data = self._request('GET', "payment", params=params)
        return parse_response(data, PaymentList, as_model)

    def create_invoice(
            self,
            price_amount: Union[int, float],
            price_currency: str,
            as_model: bool = False,
            **kwargs
    ) -> Union[dict, Invoice]:
        """
        Create invoice.

        :param price_amount: Fiat equivalent of the price to be paid in crypto.
        :param price_currency: Fiat currency of ``price_amount``.
        :param as_model: When True, return an ``Invoice`` model.
        :return: Invoice response.
        """
        data = {
            "price_amount": price_amount,
            "price_currency": price_currency,
            **kwargs
        }
        response = self._request('POST', 'invoice', json=data)
        return parse_response(response, Invoice, as_model)

    def get_api_status(self, as_model: bool = False) -> Union[dict, APIStatus]:
        data = super().get_api_status()
        return parse_response(data, APIStatus, as_model)
