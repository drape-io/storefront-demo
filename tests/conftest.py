from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from storefront.cart import coupons
from storefront.cart.models import Cart, Coupon, Customer, LineItem


@pytest.fixture(autouse=True)
def coupon_table():
    coupons.COUPONS.clear()
    coupons.COUPONS.update({
        "SPRING10": Coupon("SPRING10", percent_off=Decimal("10"), stackable=True),
        "FIVEOFF": Coupon("FIVEOFF", amount_off=Decimal("5"), stackable=True),
        "WELCOME20": Coupon("WELCOME20", percent_off=Decimal("20"), first_order_only=True),
        "BIG50": Coupon("BIG50", amount_off=Decimal("50"), min_spend=Decimal("200")),
        "OLD": Coupon("OLD", percent_off=Decimal("10"), expires_at=datetime.now(UTC) - timedelta(days=1)),
    })
    yield coupons.COUPONS


@pytest.fixture
def new_customer():
    return Customer(id=1, email="new@example.com", order_count=0)


@pytest.fixture
def returning_customer():
    return Customer(id=2, email="back@example.com", order_count=3)


@pytest.fixture
def cart(new_customer):
    return Cart(new_customer, [LineItem("MUG", Decimal("12.50"), 2), LineItem("TEE", Decimal("25.00"))])
