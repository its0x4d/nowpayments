from dataclasses import dataclass
from typing import List, Optional, Union

from nowpayment.models.base import BaseResponse


@dataclass
class SubscriptionPlan(BaseResponse):
    id: Optional[Union[str, int]] = None
    title: Optional[str] = None
    interval_day: Optional[Union[int, str]] = None
    amount: Optional[Union[int, float, str]] = None
    currency: Optional[str] = None
    ipn_callback_url: Optional[str] = None
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None
    partially_paid_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class SubscriptionPlanList(BaseResponse):
    result: Optional[List[SubscriptionPlan]] = None
    count: Optional[int] = None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("SubscriptionPlanList.from_dict() expects a dict")
        items = data.get("result", data.get("plans", []))
        plans = [
            SubscriptionPlan.from_dict(item)
            for item in items
            if isinstance(item, dict)
        ]
        return cls(
            result=plans,
            count=data.get("count"),
            raw=data,
        )


@dataclass
class Subscription(BaseResponse):
    id: Optional[Union[str, int]] = None
    subscription_plan_id: Optional[Union[str, int]] = None
    status: Optional[str] = None
    email: Optional[str] = None
    sub_partner_id: Optional[Union[str, int]] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class SubscriptionList(BaseResponse):
    result: Optional[List[Subscription]] = None
    count: Optional[int] = None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("SubscriptionList.from_dict() expects a dict")
        items = data.get("result", data.get("subscriptions", []))
        subscriptions = [
            Subscription.from_dict(item)
            for item in items
            if isinstance(item, dict)
        ]
        return cls(
            result=subscriptions,
            count=data.get("count"),
            raw=data,
        )


@dataclass
class AddressValidation(BaseResponse):
    valid: Optional[bool] = None
    message: Optional[str] = None


@dataclass
class PayoutFee(BaseResponse):
    fee: Optional[Union[int, float, str]] = None
    currency: Optional[str] = None
