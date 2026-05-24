import pytest
from core.orders import (
    BaseOrder,
    DistributeProductByCustomer,
    IntakeOrder,
    PalletToLocation
)

@pytest.fixture
def base_fields():
    return {
        "id": 1,
        "locations": ["test_location"],
        "created_at": 1.0,
        "status": "Pending",
        "estimated_completion_time": 2.0
    }


@pytest.fixture
def distribute_product_by_customer(base_fields):
    return {
        **base_fields,
        "priority": 1,
        "product": "test_product",
        "initial_product_location": "test_location",
        "total_qty": 24
    }


@pytest.fixture
def intake_order(base_fields):
    return {
        **base_fields,
        "due_time": 1.0,
        "products": {"test_product": 1}
    }


@pytest.fixture
def pallet_to_location(base_fields):
    return {
        **base_fields,
        "priority": 1,
        "product": "test_product",
        "initial_location": "test_location_1",
        "destination_location": "test_location_2",
    }

class TestBaseOrderValidation:

    def test_empty_locations_raises(self, base_fields):
        base_fields["locations"] = []
        with pytest.raises(ValueError, match="locations must not be empty"):
            DistributeProductByCustomer(
                **base_fields,
                priority=1,
                product="SKU-001",
                initial_product_location="shelf_A1",
                total_qty=10,
            )

    def test_invalid_status_raises(self, base_fields):
        base_fields["status"] = "Unknown"
        with pytest.raises(ValueError, match="status must be"):
            DistributeProductByCustomer(
                **base_fields,
                priority=1,
                product="SKU-001",
                initial_product_location="shelf_A1",
                total_qty=10,
            )

    def test_negative_estimated_completion_time_raises(self, base_fields):
        base_fields["estimated_completion_time"] = -1.0
        with pytest.raises(ValueError, match="estimated completion time"):
            DistributeProductByCustomer(
                **base_fields,
                priority=1,
                product="SKU-001",
                initial_product_location="shelf_A1",
                total_qty=10,
            )

    def test_negative_created_at_raises(self, base_fields):
        base_fields["created_at"] = -1.0
        with pytest.raises(ValueError, match="created_at must be positive"):
            DistributeProductByCustomer(
                **base_fields,
                priority=1,
                product="SKU-001",
                initial_product_location="shelf_A1",
                total_qty=10,
            )

    @pytest.mark.parametrize("status", ["Pending", "Completed", "Assigned", "In Progress"])
    def test_valid_statuses(self, base_fields, status):
        base_fields["status"] = status
        order = DistributeProductByCustomer(
            **base_fields,
            priority=1,
            product="SKU-001",
            initial_product_location="shelf_A1",
            total_qty=10,
        )
        assert order.status == status


class TestDistributeProductByCustomer:

    def test_valid_order_creates(self, distribute_product_by_customer):
        assert distribute_product_by_customer["total_qty"] == 24
        assert distribute_product_by_customer["product"] == "test_product"

    def test_zero_total_qty_raises(self, base_fields):
        with pytest.raises(ValueError, match="total_qty must be positive"):
            DistributeProductByCustomer(
                **base_fields,
                priority=1,
                product="SKU-001",
                initial_product_location="shelf_A1",
                total_qty=0,
            )

    def test_empty_product_raises(self, base_fields):
        with pytest.raises(ValueError, match="product must be provided"):
            DistributeProductByCustomer(
                **base_fields,
                priority=1,
                product="",
                initial_product_location="shelf_A1",
                total_qty=10,
            )

    def test_zero_priority_raises(self, base_fields):
        with pytest.raises(ValueError, match="priority must be positive"):
            DistributeProductByCustomer(
                **base_fields,
                priority=0,
                product="SKU-001",
                initial_product_location="shelf_A1",
                total_qty=10,
            )

class TestIntakeOrder:

    def test_valid_order_creates(self, intake_order):
        assert intake_order["due_time"] == 1.0
        assert intake_order["products"] == {"test_product": 1}

    def test_zero_due_time_raises(self, base_fields):
        with pytest.raises(ValueError, match="due time must be positive"):
            IntakeOrder(**base_fields, due_time=0, products={"test_product": 10})

    def test_empty_products_raises(self, base_fields):
        with pytest.raises(ValueError, match="products must not be empty"):
            IntakeOrder(**base_fields, due_time=5.0, products={})


class TestPalletToLocation:

    def test_valid_order_creates(self, pallet_to_location):
        assert pallet_to_location["priority"] == 1
        assert pallet_to_location["product"] == "test_product"
        assert pallet_to_location["initial_location"] == "test_location_1"
        assert pallet_to_location["destination_location"] == "test_location_2"

    def test_empty_product_raises(self, base_fields):
        with pytest.raises(ValueError, match="product must be provided"):
            PalletToLocation(
                **base_fields,
                priority=1,
                product="",
                initial_location="shelf_A1",
                destination_location="staging",
            )

    def test_empty_destination_raises(self, base_fields):
        with pytest.raises(ValueError, match="destination location"):
            PalletToLocation(
                **base_fields,
                priority=1,
                product="SKU-001",
                initial_location="shelf_A1",
                destination_location="",
            )


class TestOrderComparison:

    def test_higher_priority_is_greater(self, base_fields):
        low  = DistributeProductByCustomer(**base_fields, priority=1,
                    product="A", initial_product_location="shelf_A1", total_qty=5)
        high = DistributeProductByCustomer(**base_fields, priority=2,
                    product="A", initial_product_location="shelf_A1", total_qty=5)
        assert high > low

    def test_equal_priority_is_equal(self, base_fields):
        a = DistributeProductByCustomer(**base_fields, priority=1,
                product="A", initial_product_location="shelf_A1", total_qty=5)
        b = DistributeProductByCustomer(**base_fields, priority=1,
                product="A", initial_product_location="shelf_A1", total_qty=5)
        assert a == b