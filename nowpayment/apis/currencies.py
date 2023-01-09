from nowpayment.apis import BaseAPI


class CurrencyAPI(BaseAPI):

    def get_available_currencies(self, **kwargs) -> dict:
        """
        This is a method for obtaining information about all cryptocurrencies available for payments.

        fixed_rate(optional) - boolean, can be true or false.
            Returns available currencies with minimum and maximum amount of the exchange.

        :return: Available currencies.
        :rtype: dict
        """
        url = "https://api.nowpayments.io/v1/currencies"
        if 'fixed_rate' in kwargs:
            url += f'?fixed_rate={kwargs["fixed_rate"]}'
        return self._request('GET', url)

    def get_available_currencies_v2(self) -> dict:
        """
        This is a method to obtain detailed information about all cryptocurrencies available for payments.

        :return: All currencies.
        :rtype: dict
        """
        url = "https://api.nowpayments.io/v1/full-currencies"
        return self._request('GET', url)

    def get_available_checked_currencies(self, **kwargs) -> dict:
        """
        This is a method for obtaining information about the cryptocurrencies available for payments.
        Shows the coins you set as available for payments in the "coins settings" tab on your personal account.

        fixed_rate(optional) - boolean, can be true or false.
            Returns available currencies with minimum and maximum amount of the exchange.

        :return: All currencies.
        :rtype: dict
        """
        url = "https://api.nowpayments.io/v1/merchant/coins"
        if 'fixed_rate' in kwargs:
            url += f'?fixed_rate={kwargs["fixed_rate"]}'

        return self._request('GET', url)
