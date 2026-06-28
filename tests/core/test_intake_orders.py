import pytest
import pandas as pd
from io import StringIO
from core.orders import IntakeOrder, Pallet, IntakeOrderGenerator


SAMPLE_CSV = """order_id,product,qty,due_time,arrival_time
ORD001,SKU_01,40,3600,300
ORD001,SKU_02,20,3600,300
ORD002,SKU_05,60,7200,900
"""

@pytest.fixture
def sample_df():
    return pd.read_csv(StringIO(SAMPLE_CSV))

class TestIntakeOrderGenerator:
    def test_loads_correct_number_of_orders(self, sample_df, tmp_path):
        csv_file = tmp_path / "intake_orders.csv"
        csv_file.write_text(SAMPLE_CSV)

        generator = IntakeOrderGenerator.__new__(IntakeOrderGenerator)
        generator.orders = generator._load_orders_from_csv(str(csv_file))

        assert len(generator.orders) == len(sample_df["order_id"].unique())

    def test_pallets_are_grouped_correctly(self, sample_df, tmp_path):
        csv_file = tmp_path / "intake_orders.csv"
        csv_file.write_text(SAMPLE_CSV)
        df = pd.read_csv(str(csv_file))

        generator = IntakeOrderGenerator.__new__(IntakeOrderGenerator)
        generator.orders = generator._load_orders_from_csv(str(csv_file))

        for order in generator.orders:
            assert len(order.products) == df[df['order_id'] == order.id]['product'].count()


    def test_orders_are_sorted_by_arrival_time(self, sample_df, tmp_path):
        csv_file = tmp_path / "intake_orders.csv"
        csv_file.write_text(SAMPLE_CSV)

        generator = IntakeOrderGenerator.__new__(IntakeOrderGenerator)
        generator.orders = generator._load_orders_from_csv(str(csv_file))

        arrival_times = [o.arrival_time for o in generator.orders]
        assert arrival_times == sorted(arrival_times)

    def test_pallets_fields(self, sample_df, tmp_path):
        csv_file = tmp_path / "intake_orders.csv"
        csv_file.write_text(SAMPLE_CSV)

        generator = IntakeOrderGenerator.__new__(IntakeOrderGenerator)
        generator.orders = generator._load_orders_from_csv(str(csv_file))

        order = generator.orders[0]
        print(order)
        pallet = order.products[0]
        assert pallet.order_id == order.id
        assert isinstance(pallet.qty, int)
        assert isinstance(pallet.product, str)

