"""Cart totals with coupons applied."""

from decimal import ROUND_HALF_EVEN, Decimal

from storefront.cart.coupons import CouponError, lookup_coupon
from storefront.cart.models import Cart, Coupon

CENT = Decimal("0.01")


def _discount(coupon: Coupon, amount: Decimal) -> Decimal:
    if coupon.percent_off:
        return amount * coupon.percent_off / 100
    return min(coupon.amount_off, amount)


def cart_total(cart: Cart, codes: list[str]) -> Decimal:
    """The cart's total after applying ``codes`` in order.

    Only stackable coupons combine; a non-stackable coupon must be the only one.
    """
    coupons = [lookup_coupon(code, cart.customer) for code in codes]
    if len(coupons) > 1 and not all(c.stackable for c in coupons):
        raise CouponError("These coupons can't be combined")
    total = cart.subtotal
    for coupon in coupons:
        if cart.subtotal < coupon.min_spend:
            raise CouponError(f"{coupon.code} needs a minimum spend of {coupon.min_spend}")
        total -= _discount(coupon, total)
    return max(total, Decimal("0")).quantize(CENT, rounding=ROUND_HALF_EVEN)
