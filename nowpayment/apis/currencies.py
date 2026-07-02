from typing import Union

from nowpayment.apis import BaseAPI
from nowpayment.models import CurrencyList, parse_response


class CurrencyAPI(BaseAPI):

    def get_available_currencies(
        self,
        as_model: bool = False,
        **kwargs,
    ) -> Union[dict, CurrencyList]:
        """
        Get cryptocurrencies available for payments.

        :param as_model: When True, return a ``CurrencyList`` model.
        :return: Available currencies.
        """
        params = {}
        if 'fixed_rate' in kwargs:
            params['fixed_rate'] = kwargs['fixed_rate']
        data = self._request('GET', "currencies", params=params)
        return parse_response(data, CurrencyList, as_model)

    def get_available_currencies_v2(
        self,
        as_model: bool = False,
    ) -> Union[dict, CurrencyList]:
        """
        Get detailed information about all cryptocurrencies available for payments.

        :param as_model: When True, return a ``CurrencyList`` model.
        :return: Detailed currency list.
        """
        data = self._request('GET', "full-currencies")
        return parse_response(data, CurrencyList, as_model)

    def get_available_checked_currencies(
        self,
        as_model: bool = False,
        **kwargs,
    ) -> Union[dict, CurrencyList]:
        """
        Get cryptocurrencies enabled in your merchant coin settings.

        :param as_model: When True, return a ``CurrencyList`` model.
        :return: Merchant-enabled currencies.
        """
        params = {}
        if 'fixed_rate' in kwargs:
            params['fixed_rate'] = kwargs['fixed_rate']
        data = self._request('GET', "merchant/coins", params=params)
        return parse_response(data, CurrencyList, as_model)
