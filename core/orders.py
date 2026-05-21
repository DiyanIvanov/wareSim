from abc import ABC
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class BaseOrder(ABC):
    id: int
    locations: List[str]
    created_at: float
    status: str
    estimated_compleation_time: float


@dataclass(order=True)
class DistributeProductByCustomer(BaseOrder):
    priority: int
    product: str
    initial_product_location: str
    total_qty: int


@dataclass(order=True)
class IntakeOrder(BaseOrder):
    due_time: float
    products: Dict[str: int]


    def __lt__(self, other):
        return self.due_time < other.due_time