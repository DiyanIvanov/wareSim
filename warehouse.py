import salabim as sim
from typing import List
from core.workers import IntakeWorker, Picker
from core.orders import IntakeOrderGenerator


class Warehouse:
    def __init__(self, env, orders: str, simulation_duration=28800):
        self.env = env
        self.orders = orders
        self.simulation_duration = simulation_duration

        # Intake Resources
        self.intake_queue = sim.Queue(name="intake_queue")
        self.pick_by_customer_staging_area = sim.Queue(name="pick_by_customer_staging_area")
        self.intake_workers: List[IntakeWorker] = []
        self.pickers: List[Picker] = []


    def setup(self):
        intake_orders = IntakeOrderGenerator(self, self.orders)
        # self.intake_queue.append(intake_orders.orders)

        for i in range(2):
            w = IntakeWorker(warehouse=self, name=f"intake_worker_{i}")
            self.intake_workers.append(w)

    def run(self):
        self.setup()
        self.env.run(till=self.simulation_duration)
        # return self.metrics.summary()
