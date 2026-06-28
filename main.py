import salabim as sim
from core.workers import Picker
from core.orders import DistributeProductByCustomer


env = sim.Environment(trace=True)
picker = Picker(warehouse_layout=None)

env.run(till=10)
