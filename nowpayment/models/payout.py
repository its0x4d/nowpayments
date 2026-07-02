from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from nowpayment.models.base import BaseResponse


@dataclass
class AuthToken(BaseResponse):
    token: Optional[str] = None


@dataclass
class BalanceEntry:
    amount: Union[int, float] = 0
    pending_amount: Union[int, float] = 0
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Balance(BaseResponse):
    balances: Dict[str, BalanceEntry] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("Balance.from_dict() expects a dict")
        balances: Dict[str, BalanceEntry] = {}
        for currency, entry in data.items():
            if isinstance(entry, dict):
                balances[currency] = BalanceEntry(
                    amount=entry.get("amount", 0),
                    pending_amount=entry.get("pendingAmount", entry.get("pending_amount", 0)),
                    raw=entry,
                )
        return cls(balances=balances, raw=data)


@dataclass
class PayoutWithdrawal(BaseResponse):
    id: Optional[Union[str, int]] = None
    address: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[Union[str, int, float]] = None
    status: Optional[str] = None
    hash: Optional[str] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Payout(BaseResponse):
    id: Optional[Union[str, int]] = None
    withdrawals: Optional[List[PayoutWithdrawal]] = None
    status: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("Payout.from_dict() expects a dict")
        withdrawals = [
            PayoutWithdrawal.from_dict(item)
            for item in data.get("withdrawals", [])
            if isinstance(item, dict)
        ]
        return cls(
            id=data.get("id"),
            withdrawals=withdrawals,
            status=data.get("status"),
            raw=data,
        )


@dataclass
class PayoutVerification(BaseResponse):
    status: Optional[str] = None
