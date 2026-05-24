from abc import ABC
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class BaseOrder(ABC):
    id: int
    locations: List[str]
    created_at: float
    status: str
    estimated_completion_time: float

    def __post_init__(self):
        if len(self.locations) <= 0:
            raise ValueError("locations must not be empty")
        if self.status not in ["Pending", "Completed", "Assigned", "In Progress"]:
            raise ValueError("status must be Pending or Completed")
        if self.estimated_completion_time <= 0:
            raise ValueError("estimated completion time must be positive")
        if self.created_at <= 0:
            raise ValueError("created_at must be positive")


@dataclass(order=True)
class DistributeProductByCustomer(BaseOrder):
    priority: int
    product: str
    initial_product_location: str
    total_qty: int

    def __post_init__(self):
        super().__post_init__()
        if self.total_qty <= 0:
            raise ValueError("total_qty must be positive")
        if self.priority <= 0:
            raise ValueError("priority must be positive")
        if self.product is None:
            raise ValueError("product must be provided")
        if self.initial_product_location is None:
            raise ValueError("Initial location must be provided")


@dataclass(order=True)
class IntakeOrder(BaseOrder):
    due_time: float
    products: Dict[str, int]

    def __post_init__(self):
        super().__post_init__()
        if self.due_time <= 0:
            raise ValueError("due time must be positive")
        if self.products is None:
            raise ValueError("products must not be empty")


@dataclass(order=True)
class PalLetToLocation(BaseOrder):
    priority: int
    product: str
    initial_location: str
    destination_location: str

    def __post_init__(self):
        super().__post_init__()
        if self.priority <= 0:
            raise ValueError("priority must be positive")
        if self.product is None:
            raise ValueError("product must be provided")
        if self.initial_location is None:
            raise ValueError("initial location must be provided")
        if self.destination_location is None:
            raise ValueError("destination location must be provided")
