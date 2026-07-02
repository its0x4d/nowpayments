from dataclasses import dataclass
from typing import List, Optional, Union

from nowpayment.models.base import BaseResponse


@dataclass
class Currency(BaseResponse):
    id: Optional[Union[int, str]] = None
    code: Optional[str] = None
    name: Optional[str] = None
    enable: Optional[bool] = None
    wallet_regex: Optional[str] = None
    priority: Optional[int] = None
    extra_id_exists: Optional[bool] = None
    extra_id_regex: Optional[str] = None
    logo_url: Optional[str] = None
    track: Optional[bool] = None
    cg_id: Optional[str] = None
    is_maxlimit: Optional[bool] = None
    network: Optional[str] = None
    smart_contract: Optional[str] = None
    network_precision: Optional[Union[int, str]] = None


@dataclass
class CurrencyList(BaseResponse):
    currencies: Optional[List[Union[str, Currency]]] = None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("CurrencyList.from_dict() expects a dict")
        currencies = data.get("currencies", [])
        parsed: List[Union[str, Currency]] = []
        for item in currencies:
            if isinstance(item, dict):
                parsed.append(Currency.from_dict(item))
            else:
                parsed.append(item)
        return cls(currencies=parsed, raw=data)
