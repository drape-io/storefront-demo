from decimal import Decimal

import pytest

from storefront.cart.coupons import CouponError
from storefront.cart.models import Cart, LineItem
from storefront.cart.pricing import cart_total


def test_no_coupons(cart):
    assert cart_total(cart, []) == Decimal("50.00")


def test_percent_coupon(cart):
    assert cart_total(cart, ["SPRING10"]) == Decimal("45.00")


def test_stacked_coupons_apply_in_order(cart):
    assert cart_total(cart, ["SPRING10", "FIVEOFF"]) == Decimal("40.00")


def test_non_stackable_coupon_cannot_combine(cart):
    with pytest.raises(CouponError):
        cart_total(cart, ["WELCOME20", "SPRING10"])


def test_minimum_spend(cart):
    with pytest.raises(CouponError):
        cart_total(cart, ["BIG50"])


def test_expired_coupon(cart):
    with pytest.raises(CouponError):
        cart_total(cart, ["OLD"])


def test_first_order_coupon_for_new_customer(cart):
    assert cart_total(cart, ["WELCOME20"]) == Decimal("40.00")


def test_first_order_coupon_rejected_for_returning_customer(returning_customer):
    cart = Cart(returning_customer, [LineItem("TEE", Decimal("25.00"))])
    with pytest.raises(CouponError):
        cart_total(cart, ["WELCOME20"])
