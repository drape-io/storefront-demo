from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Customer:
    id: int
    email: str
    order_count: int = 0


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price: Decimal
    quantity: int = 1

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Cart:
    customer: Customer
    items: list[LineItem] = field(default_factory=list)

    @property
    def subtotal(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0"))


@dataclass(frozen=True)
class Coupon:
    code: str
    percent_off: Decimal = Decimal("0")
    amount_off: Decimal = Decimal("0")
    min_spend: Decimal = Decimal("0")
    expires_at: datetime | None = None
    first_order_only: bool = False
    stackable: bool = False
