from typing import Any, Dict, Optional


class NowPaymentsError(Exception):
    """Base exception for the nowpayment SDK."""


class NowPaymentsAPIError(NowPaymentsError):
    """Raised when the NOWPayments API returns an error response."""

    def __init__(
        self,
        status_code: int,
        message: str,
        response: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"{status_code}: {message}")
