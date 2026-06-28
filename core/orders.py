from abc import ABC
from dataclasses import dataclass
from typing import List, Dict
import pandas as pd
import salabim as sim


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
        if not self.product:
            raise ValueError("product must be provided")
        if not self.initial_product_location:
            raise ValueError("Initial location must be provided")


@dataclass(order=True)
class IntakeOrder(BaseOrder):
    arrival_time: float
    pallets: Dict[str, int]

    def __post_init__(self):
        super().__post_init__()
        if self.arrival_time <= 0:
            raise ValueError("arrival time must be positive")
        if not self.pallets:
            raise ValueError("Pallets must not be empty")


@dataclass(order=True)
class PalletToLocation(BaseOrder):
    priority: int
    product: str
    initial_location: str
    destination_location: str

    def __post_init__(self):
        super().__post_init__()
        if self.priority <= 0:
            raise ValueError("priority must be positive")
        if not self.product:
            raise ValueError("product must be provided")
        if not self.initial_location:
            raise ValueError("initial location must be provided")
        if not self.destination_location:
            raise ValueError("destination location must be provided")

@dataclass
class Pallet:
    product: str
    qty: int
    order_id: str


class IntakeOrderGenerator(sim.Component):

    def __init__(self, warehouse, orders_file, **kwargs):
        super().__init__(**kwargs)
        self.warehouse = warehouse
        self.orders = self._load_orders_from_csv(orders_file)

    def _load_orders_from_csv(self, file_path):
        data = pd.read_csv(file_path)
        orders = []

        for order in data['order_id'].unique():
            orders.append(IntakeOrder(
                id=order,
                locations=['Salabim'],
                created_at=1,
                status="Pending",
                arrival_time=data[data['order_id'] == order]['arrival_time'].values[0],
                pallets=self._load_pallets(data, order),
                estimated_completion_time=0.1
            ))

        return sorted(orders, key=lambda o: o.arrival_time)

    def _load_pallets(self, data, order_id):
        pallets_data = data[data['order_id'] == order_id]
        pallets = []
        for _, row in pallets_data.iterrows():
            pallets.append(Pallet(
                product=row['product'],
                qty=int(row['qty']),
                order_id=order_id,
            ))
        return pallets

    def process(self):
        for order in self.orders:
            self.hold(order.arrival_time - self.env.now())
            order.enter(self.warehouse.intake_queue)
