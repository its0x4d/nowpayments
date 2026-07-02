from typing import Optional, Union

from nowpayment.apis import BaseAPI
from nowpayment.decorators import jwt_required
from nowpayment.models import (
    Subscription,
    SubscriptionList,
    SubscriptionPlan,
    SubscriptionPlanList,
    parse_response,
)


class SubscriptionAPI(BaseAPI):

    @jwt_required
    def create_plan(
        self,
        title: str,
        interval_day: int,
        amount: Union[int, float],
        currency: str,
        as_model: bool = False,
        **kwargs,
    ) -> Union[dict, SubscriptionPlan]:
        """
        Create a recurring payment plan.

        :param title: Plan name shown to customers.
        :param interval_day: Billing interval in days.
        :param amount: Plan price.
        :param currency: Fiat currency ticker (usd, eur, etc).
        :param as_model: When True, return a ``SubscriptionPlan`` model.
        :return: Created plan response.
        """
        data = {
            "title": title,
            "interval_day": interval_day,
            "amount": amount,
            "currency": currency,
            **kwargs,
        }
        response = self._request('POST', "subscriptions/plans", json=data)
        return parse_response(response, SubscriptionPlan, as_model)

    def get_plans(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        as_model: bool = False,
    ) -> Union[dict, SubscriptionPlanList]:
        """
        List subscription plans.

        :param limit: Maximum number of plans to return.
        :param offset: Number of plans to skip.
        :param as_model: When True, return a ``SubscriptionPlanList`` model.
        :return: Plan list response.
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._request('GET', "subscriptions/plans", params=params)
        return parse_response(data, SubscriptionPlanList, as_model)

    def get_plan(
        self,
        plan_id: Union[str, int],
        as_model: bool = False,
    ) -> Union[dict, SubscriptionPlan]:
        """
        Get a single subscription plan.

        :param plan_id: Plan ID.
        :param as_model: When True, return a ``SubscriptionPlan`` model.
        :return: Plan response.
        """
        data = self._request('GET', f"subscriptions/plans/{plan_id}")
        return parse_response(data, SubscriptionPlan, as_model)

    @jwt_required
    def update_plan(
        self,
        plan_id: Union[str, int],
        as_model: bool = False,
        **updates,
    ) -> Union[dict, SubscriptionPlan]:
        """
        Update an existing subscription plan.

        :param plan_id: Plan ID.
        :param as_model: When True, return a ``SubscriptionPlan`` model.
        :param updates: Fields to update (title, amount, interval_day, etc).
        :return: Updated plan response.
        """
        data = self._request('PATCH', f"subscriptions/plans/{plan_id}", json=updates)
        return parse_response(data, SubscriptionPlan, as_model)

    @jwt_required
    def create_subscription(
        self,
        subscription_plan_id: Union[str, int],
        as_model: bool = False,
        email: Optional[str] = None,
        sub_partner_id: Optional[Union[str, int]] = None,
        **kwargs,
    ) -> Union[dict, Subscription]:
        """
        Create a subscription for email billing or custody sub-partners.

        Provide ``email`` for email subscriptions or ``sub_partner_id`` for custody.

        :param subscription_plan_id: Plan ID to subscribe to.
        :param email: Customer email for email-based subscriptions.
        :param sub_partner_id: Sub-partner ID for custody subscriptions.
        :param as_model: When True, return a ``Subscription`` model.
        :return: Subscription response.
        """
        if email is None and sub_partner_id is None:
            raise ValueError("email or sub_partner_id is required")
        data = {
            "subscription_plan_id": subscription_plan_id,
            **kwargs,
        }
        if email is not None:
            data["email"] = email
        if sub_partner_id is not None:
            data["sub_partner_id"] = sub_partner_id
        response = self._request('POST', "subscriptions", json=data)
        return parse_response(response, Subscription, as_model)

    def get_subscriptions(
        self,
        as_model: bool = False,
        status: Optional[str] = None,
        subscription_plan_id: Optional[Union[str, int]] = None,
        is_active: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Union[dict, SubscriptionList]:
        """
        List recurring subscriptions.

        :param status: Filter by status (e.g. PAID, WAITING).
        :param subscription_plan_id: Filter by plan ID.
        :param is_active: Filter by active flag.
        :param limit: Maximum results to return.
        :param offset: Number of results to skip.
        :param as_model: When True, return a ``SubscriptionList`` model.
        :return: Subscription list response.
        """
        params = {}
        if status is not None:
            params["status"] = status
        if subscription_plan_id is not None:
            params["subscription_plan_id"] = subscription_plan_id
        if is_active is not None:
            params["is_active"] = str(is_active).lower()
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._request('GET', "subscriptions", params=params)
        return parse_response(data, SubscriptionList, as_model)

    def get_subscription(
        self,
        subscription_id: Union[str, int],
        as_model: bool = False,
    ) -> Union[dict, Subscription]:
        """
        Get a single subscription.

        :param subscription_id: Subscription ID.
        :param as_model: When True, return a ``Subscription`` model.
        :return: Subscription response.
        """
        data = self._request('GET', f"subscriptions/{subscription_id}")
        return parse_response(data, Subscription, as_model)

    @jwt_required
    def delete_subscription(
        self,
        subscription_id: Union[str, int],
    ) -> dict:
        """
        Delete a subscription.

        :param subscription_id: Subscription ID.
        :return: API response.
        """
        return self._request('DELETE', f"subscriptions/{subscription_id}")
