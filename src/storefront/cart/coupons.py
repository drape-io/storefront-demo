"""Coupon lookup and eligibility."""

from datetime import UTC, datetime

from storefront.cart.models import Coupon, Customer

# Stands in for the coupons table.
COUPONS: dict[str, Coupon] = {}


class CouponError(Exception):
    pass


def fetch_coupon(code: str) -> Coupon:
    try:
        return COUPONS[code.upper()]
    except KeyError:
        raise CouponError(f"Unknown coupon {code!r}") from None


def check_eligibility(coupon: Coupon, customer: Customer, now: datetime | None = None) -> None:
    now = now or datetime.now(UTC)
    if coupon.expires_at is not None and now >= coupon.expires_at:
        raise CouponError(f"{coupon.code} has expired")
    if coupon.first_order_only and customer.order_count > 0:
        raise CouponError(f"{coupon.code} is only valid on a first order")


def lookup_coupon(code: str, customer: Customer) -> Coupon:
    """The coupon for ``code`` if ``customer`` may use it, else CouponError."""
    coupon = fetch_coupon(code)
    check_eligibility(coupon, customer)
    return coupon
