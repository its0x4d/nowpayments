from dataclasses import dataclass
from typing import List, Optional, Union

from nowpayment.models.base import BaseResponse


@dataclass
class APIStatus(BaseResponse):
    message: Optional[str] = None


@dataclass
class Estimate(BaseResponse):
    currency_from: Optional[str] = None
    currency_to: Optional[str] = None
    amount_from: Optional[Union[int, float, str]] = None
    amount_to: Optional[Union[int, float, str]] = None
    estimated_amount: Optional[Union[int, float, str]] = None


@dataclass
class MinAmount(BaseResponse):
    min_amount: Optional[Union[int, float, str]] = None
    fiat_equivalent: Optional[Union[int, float, str]] = None
    currency_from: Optional[str] = None
    currency_to: Optional[str] = None


@dataclass
class Payment(BaseResponse):
    payment_id: Optional[Union[str, int]] = None
    payment_status: Optional[str] = None
    pay_address: Optional[str] = None
    price_amount: Optional[Union[int, float, str]] = None
    price_currency: Optional[str] = None
    pay_amount: Optional[Union[int, float, str]] = None
    pay_currency: Optional[str] = None
    order_id: Optional[str] = None
    order_description: Optional[str] = None
    purchase_id: Optional[str] = None
    actually_paid: Optional[Union[int, float, str]] = None
    outcome_amount: Optional[Union[int, float, str]] = None
    outcome_currency: Optional[str] = None
    invoice_id: Optional[Union[str, int]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Invoice(BaseResponse):
    id: Optional[Union[str, int]] = None
    order_id: Optional[str] = None
    order_description: Optional[str] = None
    price_amount: Optional[Union[int, float, str]] = None
    price_currency: Optional[str] = None
    pay_currency: Optional[str] = None
    ipn_callback_url: Optional[str] = None
    invoice_url: Optional[str] = None
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class PaymentList(BaseResponse):
    data: Optional[List[Payment]] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    pages_count: Optional[int] = None
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("PaymentList.from_dict() expects a dict")
        items = [Payment.from_dict(item) for item in data.get("data", []) if isinstance(item, dict)]
        return cls(
            data=items,
            limit=data.get("limit"),
            page=data.get("page"),
            pages_count=data.get("pagesCount") or data.get("pages_count"),
            total=data.get("total"),
            raw=data,
        )
