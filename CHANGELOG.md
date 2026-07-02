# Changelog

All notable changes to this project are documented in this file.

## [1.9.0] - 2026-07-02

### Added
- Full **Subscriptions API** (`client.subscription`): plans, subscriptions, update, delete.
- Payout endpoints: `validate_address`, `get_payout_fee`, `cancel_payout`.
- **Webhook helpers**: `verify_ipn_payload`, `extract_ipn_signature`, `IPNVerificationError`.
- Response models: `SubscriptionPlan`, `Subscription`, `AddressValidation`, `PayoutFee`.
- Sandbox integration tests (`pytest -m integration`) and `examples/sandbox_smoke_test.py`.
- Testing guide: [docs/TESTING.md](docs/TESTING.md).
- `.env.example` for local sandbox credentials.

## [1.8.0] - 2026-07-02

### Added
- Typed response models: `Payment`, `Invoice`, `PaymentList`, `Currency`, `CurrencyList`, `Estimate`, `MinAmount`, `Payout`, `Balance`, `AuthToken`, and more.
- `as_model=True` on payment, currency, and payout API methods to return parsed models.
- Sandbox support via `NowPayments(api_key, sandbox=True)`.
- Shared `requests.Session` with context-manager support (`with NowPayments(...) as client:`).
- `Payment.from_dict()` and model `to_dict()` helpers for manual parsing.

### Changed
- HTTP requests now reuse a single session per `NowPayments` client.

## [1.7.0] - 2026-07-02

### Added
- MIT `LICENSE` file and `pyproject.toml` for modern packaging.
- `NowPaymentsAPIError` and `NowPaymentsError` exception types.
- `compute_payment_signature()` helper for IPN callbacks.
- GitHub Actions CI (lint + tests).
- Pytest suite with mocked HTTP requests.

### Fixed
- `get_user_payments()` always sending `payment_id` due to `if id:` builtin bug.
- `create_recurring_payments()` posting to wrong endpoint (`subscriptions` instead of `sub-partner/balance`).
- `BaseAPI._request()` replacing headers instead of merging them.
- HTTP error responses now raise `NowPaymentsAPIError` instead of returning raw JSON decode errors.
- `get_user_payments()` and list helpers now use query `params` instead of GET bodies.
- `verify_payout()` accepts `payout_id` as an alias for `withdrawals_id`.

### Changed
- Unified package version to `1.7.0`.
- Relaxed `requests` pin to `>=2.28.1,<3`.
- Minimum supported Python version is now 3.8.
