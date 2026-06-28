import pytest
import pandas as pd
from io import StringIO
from core.orders import IntakeOrder, Pallet, IntakeOrderGenerator
import salabim as sim


SAMPLE_CSV = """order_id,product,qty,due_time,arrival_time
ORD001,SKU_01,40,3600,300
ORD001,SKU_02,20,3600,300
ORD002,SKU_05,60,7200,900
"""

@pytest.fixture(scope="class")
def sample_df():
    return pd.read_csv(StringIO(SAMPLE_CSV))

@pytest.fixture(scope="class")
def csv_file(tmp_path_factory):
    f = tmp_path_factory.mktemp("data") / "intake_orders.csv"
    f.write_text(SAMPLE_CSV)
    return str(f)

@pytest.fixture(scope="class")
def generator(csv_file):
    sim.Environment(trace=False)
    return IntakeOrderGenerator(warehouse=None, orders_file=csv_file)


class TestIntakeOrderGenerator:

    def test_loads_correct_number_of_orders(self, generator, sample_df):
        assert len(generator.orders) == len(sample_df["order_id"].unique())

    def test_pallets_are_grouped_correctly(self, generator, sample_df):
        for order in generator.orders:
            expected = sample_df[sample_df["order_id"] == order.id]["product"].count()
            assert len(order.pallets) == expected

    def test_orders_are_sorted_by_arrival_time(self, generator):
        arrival_times = [o.arrival_time for o in generator.orders]
        assert arrival_times == sorted(arrival_times)

    def test_pallet_fields(self, generator):
        pallet = generator.orders[0].pallets[0]
        assert pallet.order_id == generator.orders[0].id
        assert isinstance(pallet.qty, int)
        assert isinstance(pallet.product, str)
