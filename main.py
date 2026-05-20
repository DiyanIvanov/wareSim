import simpy
from core.workers import Picker


env = simpy.Environment()
picker = Picker(env)
env.run(until=10)