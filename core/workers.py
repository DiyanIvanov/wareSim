from abc import ABC, abstractmethod
import salabim as sim
from core.orders import DistributeProductByCustomer


class Worker(sim.Component, ABC):

    BREAK_WINDOWS = [[7200, 7650], [21600,22500]]
    LUNCH_WINDOW = [14400,15300]
    MAX_ALLOWED_SHORT_BREAKS = 2

    def __init__(self, warehouse, short_break=15, lunch_break=30, **kwargs):
        super().__init__(**kwargs)
        self.short_break = short_break
        self.lunch_break = lunch_break
        self.warehouse_layout = warehouse
        self.breaks_taken = set()
        self.lunch_breaks = 0

    @abstractmethod
    def process(self):
        """Must be implemented"""
        raise NotImplementedError

    def get_short_break(self):
        if self._break_allowed():
            current_breaks = max(self.breaks_taken)
            self.breaks_taken.add(current_breaks + 1)
            self.hold(self.short_break)

    def get_lunch_break(self):
        if self.lunch_breaks < 1 and self.LUNCH_WINDOW[1] >= self.env.now() <= self.LUNCH_WINDOW[1]:
            self.lunch_breaks += 1
            self.hold(self.lunch_break)

    def travel_to(self, location):
        # ToDo after location class is implemented
        pass

    def _break_allowed(self):
        if max(self.breaks_taken) >= self.MAX_ALLOWED_SHORT_BREAKS:
            return False

        for i, window in enumerate(self.BREAK_WINDOWS):
            if window[1] <= self.env.now() <= window[2] and i not in self.breaks_taken:
                return True

        return False

class Picker(Worker):

    TAKE_EQUIPMENT_RATE = 5
    PICK_RATE = 1

    def __init__(self, warehouse, short_break=15, lunch_break=30,order = None,  **kwargs):
        super().__init__(warehouse, short_break, lunch_break, **kwargs)
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


class IntakeWorker(Worker):

    INTAKE_RATE_PER_PALLET = 180 # measured in seconds

    def __init__(self, warehouse, short_break=15, lunch_break=30,**kwargs):
        super().__init__(warehouse, short_break=15, lunch_break=30,**kwargs)
        self.order = None

    def process(self):
        while True:
            self.hold(self.INTAKE_RATE_PER_PALLET)
