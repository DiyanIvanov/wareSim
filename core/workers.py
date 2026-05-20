from abc import ABC, abstractmethod
import simpy


class Worker(ABC):

    def __init__(self, env, short_brake = 15, lunch_break = 30):
        self.env = env
        self.action = env.process(self.run())
        self.short_break = short_brake
        self.lunch_break = lunch_break

    @abstractmethod
    def run(self):
        """Must be implemented as a generator that yields SimPy events."""
        raise NotImplementedError

    def get_short_break(self):
        yield self.env.timeout(self.short_break)

    def get_lunch_break(self):
        yield self.env.timeout(self.lunch_break)

