import os

from nowpayment import NowPayments, NowPaymentsAPIError


def main() -> None:
    api_key = os.environ.get("NOWPAYMENTS_SANDBOX_API_KEY")
    if not api_key:
        raise SystemExit(
            "Set NOWPAYMENTS_SANDBOX_API_KEY to your sandbox key.\n"
            "Get one at https://account-sandbox.nowpayments.io/"
        )

    client = NowPayments(api_key, sandbox=True)

    print("1. API status")
    print(client.get_api_status(as_model=True))

    print("\n2. Available currencies")
    currencies = client.currency.get_available_currencies(as_model=True)
    preview = currencies.currencies[:5] if currencies.currencies else []
    print(f"first 5: {preview}")

    print("\n3. Price estimate (10 USD -> BTC)")
    try:
        estimate = client.payment.get_estimated_price(
            amount=10,
            from_currency="usd",
            to_currency="btc",
            as_model=True,
        )
        print(estimate)
    except NowPaymentsAPIError as exc:
        print(f"estimate failed: {exc.status_code} {exc.message}")

    print("\n4. Minimum payment amount (USD -> TRX)")
    try:
        minimum = client.payment.get_minimum_payment_amount(
            from_currency="usd",
            to_currency="trx",
            as_model=True,
        )
        print(minimum)
    except NowPaymentsAPIError as exc:
        print(f"min-amount failed: {exc.status_code} {exc.message}")

    print("\n5. Subscription plans")
    try:
        plans = client.subscription.get_plans(limit=5, as_model=True)
        print(plans)
    except NowPaymentsAPIError as exc:
        print(f"subscriptions failed: {exc.status_code} {exc.message}")

    print("\nDone. Sandbox smoke test completed.")


if __name__ == "__main__":
    main()
