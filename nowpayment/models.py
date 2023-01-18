from dataclasses import dataclass, asdict


@dataclass
class WithdrawalModel:
    address: str
    currency: str
    amount: float
    ipn_callback_url: str
    extra_id: str = None
    fiat_amount: float = None
    fiat_currency: str = None

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items() if v is not None}
