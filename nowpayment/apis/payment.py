from typing import Union

from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required


class PaymentAPI(BaseAPI):

    def get_estimated_price(self, amount: Union[int, float], from_currency: str, to_currency: str) -> dict:
        """
        Get estimated price.

        :param amount: Amount of money.
        :param from_currency: Currency of money.
        :param to_currency: Currency of money.
        :return: Estimated price.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/estimate?" \
              f"amount={amount}&" \
              f"currency_from={from_currency}&" \
              f"currency_to={to_currency}"
        return self._request('GET', url)

    def create_payment(
            self,
            price_amount: Union[int, float],
            price_currency: str,
            pay_currency: str,
            ipn_callback_url: str = None,
            order_id: str = None,
            **kwargs
    ) -> dict:
        """
        Create payment.

        :param ipn_callback_url:
        :param price_amount: the fiat equivalent of the price to be paid in crypto.
            If the pay_amount parameter is left empty, our system will automatically convert this fiat price
             into its crypto equivalent. Please note that this does not enable fiat payments, only provides a fiat price
             for yours and the customer’s convenience and information.
        :param price_currency: the fiat currency in which the price_amount is specified (usd, eur, etc).
        :param pay_currency: the cryptocurrency in which the pay_amount is specified (btc, eth, etc)
        :param ipn_callback_url:  url to receive callbacks, should contain "http/https",  e.g: "https://nowpayments.io"
        :param order_id: inner store order ID, e.g. "RGDBP-21314"
        :param kwargs: Keyword arguments. See: https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest#5e37f3ad-0fa1-4292-af51-5c7f95730486
        :return: Payment.
        :rtype: dict
        """
        url = "https://api.nowpayments.io/v1/payment"
        data = {
            "price_amount": price_amount,
            "price_currency": price_currency,
            "pay_currency": pay_currency,
            "order_id": order_id,
            "ipn_callback_url": ipn_callback_url,
            **kwargs
        }
        return self._request('POST', url, json=data)

    def create_invoice_payment(self, invoice_id: str, pay_currency: str, **kwargs) -> dict:
        """
        Create invoice payment.

        :param invoice_id: Invoice ID.
        :param pay_currency: the cryptocurrency in which the pay_amount is specified (btc, eth, etc)
        :param kwargs: Keyword arguments. See: https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest#5bf0a8a7-ea42-4160-95c9-961601e6bb79
        :return: Invoice payment.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/invoice-payment"
        data = {
            "iid": invoice_id,
            "pay_currency": pay_currency,
            **kwargs
        }
        return self._request('POST', url, json=data)

    def get_payment_estimated(self, payment_id: str) -> dict:
        """
        Get payment estimated.

        :param payment_id: Payment ID.
        :return: Payment estimated.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/payment/{payment_id}/update-merchant-estimate"
        return self._request('GET', url)

    def get_payment_status(self, payment_id: str) -> dict:
        """
        Get payment status.

        :param payment_id: Payment ID.
        :return: Payment status.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/payment/{payment_id}"
        return self._request('GET', url)

    def get_minimum_payment_amount(self, from_currency: str, to_currency: str) -> dict:
        """
        Get minimum payment amount.

        :param from_currency: Currency of money.
        :param to_currency: Currency of money.
        :return: Minimum payment amount.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/min-amount?" \
              f"currency_from={from_currency}&" \
              f"currency_to={to_currency}"
        return self._request('GET', url)

    @jwt_required
    def get_payment_list(
            self,
            limit: int = 10,
            page: int = 0,
            sort_by: str = 'created_at',
            order_by: str = 'desc',
            date_from: str = None,
            date_to: str = None,
    ) -> dict:
        """
        Get payment list.

        :param limit: Limit.
        :param page: Page.
        :param sort_by: Sort by.
        :param order_by: Order by.
        :param date_from: Date from. e.g. "2019-01-01"
        :param date_to: Date to. e.g. "2019-01-01"

        :return: Payment list.
        :rtype: dict
        """
        url = f"https://api.nowpayments.io/v1/payment?" \
              f"limit={limit}&" \
              f"page={page}&" \
              f"sortBy={sort_by}&" \
              f"orderBy={order_by}&" \
              f"dateFrom={date_from}&" \
              f"dateTo={date_to}"
        return self._request('GET', url)

    def create_invoice(self, price_amount: Union[int, float], price_currency: str, **kwargs) -> dict:
        """
        Create invoice.

        :param price_amount: the fiat equivalent of the price to be paid in crypto.
            If the pay_amount parameter is left empty, our system will automatically convert this fiat price
             into its crypto equivalent. Please note that this does not enable fiat payments, only provides a fiat price
             for yours and the customer’s convenience and information.
        :param price_currency: the fiat currency in which the price_amount is specified (usd, eur, etc).
        :param kwargs: Keyword arguments. See: https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest#3e3ce25e-f43f-4636-bbd9-11560e46048b
        :return: Invoice.
        :rtype: dict
        """
        url = "https://api.nowpayments.io/v1/invoice"
        data = {
            "price_amount": price_amount,
            "price_currency": price_currency,
            **kwargs
        }
        return self._request('POST', url, json=data)