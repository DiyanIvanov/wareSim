import simpy
from models.workers import Picker


env = simpy.Environment()
picker = Picker(env)
env.run(until=10)