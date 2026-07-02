from typing import Any, Dict, Mapping, Optional

from nowpayment.exceptions import NowPaymentsError
from nowpayment.signatures import verify_payment_signature

IPN_SIGNATURE_HEADER = "x-nowpayments-sig"


class IPNVerificationError(NowPaymentsError):
    """Raised when an IPN callback signature does not match."""


def extract_ipn_signature(headers: Mapping[str, str]) -> Optional[str]:
    """
    Read the NOWPayments IPN signature header from request headers.

    Header name is matched case-insensitively.

    :param headers: Request headers mapping.
    :return: Signature value or ``None`` if missing.
    """
    for key, value in headers.items():
        if key.lower() == IPN_SIGNATURE_HEADER:
            return value
    return None


def verify_ipn_payload(
    data: Dict[str, Any],
    ipn_secret: str,
    signature: str,
) -> Dict[str, Any]:
    """
    Verify an IPN callback payload and return it when valid.

    :param data: Parsed JSON body from the IPN request.
    :param ipn_secret: IPN secret from the NOWPayments dashboard.
    :param signature: Value of the ``x-nowpayments-sig`` header.
    :return: The verified payload.
    :raises IPNVerificationError: If the signature is invalid.
    :raises ValueError: If inputs are invalid.
    """
    if not signature:
        raise IPNVerificationError("Missing IPN signature header")
    is_valid = verify_payment_signature(data, ipn_secret, signature)
    if not is_valid:
        raise IPNVerificationError("Invalid IPN signature")
    return data
