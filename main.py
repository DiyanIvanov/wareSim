import salabim as sim
from warehouse import Warehouse


env = sim.Environment(trace=True)
# picker = Picker(warehouse_layout=None)
#
# env.run(till=10)

warehouse = Warehouse(env, './data/demo_data.csv')
warehouse.run()