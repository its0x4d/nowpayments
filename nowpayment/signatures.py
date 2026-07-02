import hashlib
import hmac
import json
from typing import Optional, Union


def compute_payment_signature(data: dict, ipn_secret: str) -> str:
    """
    Compute the HMAC-SHA512 signature for an IPN callback payload.
    """
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    if not isinstance(ipn_secret, str):
        raise ValueError("IPN secret must be a string")

    request_data = dict(sorted(data.items()))
    sorted_request_json = json.dumps(request_data, separators=(",", ":"))
    return hmac.new(
        ipn_secret.encode("utf-8"),
        sorted_request_json.encode("utf-8"),
        hashlib.sha512,
    ).hexdigest()


def verify_payment_signature(
    data: dict,
    ipn_secret: str,
    signature: Optional[str] = None,
) -> Union[str, bool]:
    """
    Compute or verify an IPN callback signature.
    """
    computed = compute_payment_signature(data, ipn_secret)
    if signature is None:
        return computed
    return hmac.compare_digest(computed, signature)
