from abc import ABC, abstractmethod
import simpy


class Worker(ABC):

    def __init__(self, env, warehouse_lauout, short_brake = 15, lunch_break = 30):
        self.env = env
        self.action = env.process(self.run())
        self.short_break = short_brake
        self.lunch_break = lunch_break
        self.warehouse_lauout = warehouse_lauout

    @abstractmethod
    def run(self):
        """Must be implemented as a generator that yields SimPy events."""
        raise NotImplementedError

    def get_short_break(self):
        yield self.env.timeout(self.short_break)

    def get_lunch_break(self):
        yield self.env.timeout(self.lunch_break)

    def travel_to(self, location):
        pass


class Picker(Worker):

    TAKE_EQUPMENT_RATE = 5
    PICK_RATE = 1   

    def __init__(self, env, warehouse_lauout, short_brake = 15, lunch_break = 30):
        super().__init__(env, warehouse_lauout, short_brake, lunch_break)
        self.order = None

    def run(self):
        while True:
            print(f"Start at {self.env.now}")
            yield self.env.timeout(5)

    def pick_item(self):
        pass

    def get_product(self):
        pass

    def add_empty_container(self, location):
        pass

