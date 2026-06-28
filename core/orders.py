from abc import ABC
import pandas as pd
import salabim as sim



class BaseOrder(sim.Component, ABC):
    VALID_STATUSES = {"Pending", "Completed", "Assigned", "In Progress"}

    def __init__(self, id, locations, created_at, status, estimated_completion_time, **kwargs):
        super().__init__(**kwargs)

        self._validate(locations, status, estimated_completion_time, created_at)

        self.id = id
        self.locations = locations
        self.created_at = created_at
        self.status = status
        self.estimated_completion_time = estimated_completion_time

    def _validate(self, locations, status, estimated_completion_time, created_at):
        if not locations:
            raise ValueError("locations must not be empty")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"status must be one of {self.VALID_STATUSES}")
        if estimated_completion_time <= 0:
            raise ValueError("estimated completion time must be positive")
        if created_at < 0:
            raise ValueError("created_at must not be negative")


class IntakeOrder(BaseOrder):

    def __init__(self,
                      id,
                      locations,
                      created_at,
                      status,
                      estimated_completion_time,
                      arrival_time,
                      pallets,
                      **kwargs
                      ):
        super().__init__(id, locations, created_at, status, estimated_completion_time, **kwargs)

        self._validate_intake(arrival_time, pallets)
        self.arrival_time = arrival_time
        self.pallets = pallets

    def _validate_intake(self, arrival_time, pallets):
        if arrival_time < 0:
            raise ValueError("arrival time must not be negative")
        if not pallets:
            raise ValueError("pallets must not be empty")

class Pallet(sim.Component):

    def __init__(self, product, qty, order_id, **kwargs):
        super().__init__(**kwargs)
        self.product = product
        self.qty = qty
        self.order_id = order_id


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

            # wake a passive worker
            for worker in self.warehouse.intake_workers:
                if worker.ispassive():
                    worker.activate()
                    break
