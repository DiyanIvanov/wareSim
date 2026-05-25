from abc import ABC, abstractmethod
import salabim as sim
from core.orders import DistributeProductByCustomer


class Worker(sim.Component, ABC):

    def __init__(self, warehouse_layout, short_break=15, lunch_break=30, **kwargs):
        super().__init__(**kwargs)
        self.short_break = short_break
        self.lunch_break = lunch_break
        self.warehouse_layout = warehouse_layout

    @abstractmethod
    def process(self):
        """Must be implemented as a generator that yields SimPy events."""
        raise NotImplementedError

    def get_short_break(self):
        self.hold(self.short_break)

    def get_lunch_break(self):
        self.hold(self.lunch_break)

    def travel_to(self, location):
        pass


class Picker(Worker):

    TAKE_EQUIPMENT_RATE = 5
    PICK_RATE = 1

    def __init__(self, warehouse_layout, short_break=15, lunch_break=30,order = None,  **kwargs):
        super().__init__(warehouse_layout, short_break, lunch_break, **kwargs)
        self.order = order
        self.current_location = None

    def process(self):
        while True:
            self.hold(self.PICK_RATE)


    def pick_item(self):
        self.hold(self.PICK_RATE)

    def get_product(self):
        pass

    def add_empty_container(self):
        pass
