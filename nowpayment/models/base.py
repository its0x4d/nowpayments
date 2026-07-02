from dataclasses import dataclass, field, fields
from typing import Any, Dict, Type, TypeVar, Union

T = TypeVar("T", bound="BaseResponse")


@dataclass
class BaseResponse:
    """Base type for parsed NOWPayments API responses."""

    raw: Dict[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        if not isinstance(data, dict):
            raise TypeError(f"{cls.__name__}.from_dict() expects a dict, got {type(data).__name__}")
        names = {item.name for item in fields(cls) if item.name != "raw"}
        values = {name: data.get(name) for name in names}
        return cls(**values, raw=data)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.raw)


def parse_response(
    data: Dict[str, Any],
    model: Type[T],
    as_model: bool,
) -> Union[Dict[str, Any], T]:
    if as_model:
        return model.from_dict(data)
    return data
