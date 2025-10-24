import pytest

from challenge_openspace_classifier.utils.table import Table, TableIsFullError


@pytest.fixture
def table_of_three() -> Table:
    return Table(3)


@pytest.fixture
def full_table(table_of_three) -> Table:
    table_of_three.assign_seat("Asta")
    table_of_three.assign_seat("Victor")
    table_of_three.assign_seat("Itan")
    return table_of_three


def test_table_initialization(table_of_three):
    assert table_of_three.capacity == 3
    assert table_of_three.left_capacity == 3
    assert table_of_three.has_free_spot()


def test_assign_seat_success(table_of_three):
    table_of_three.assign_seat("Hamideh")
    assert table_of_three.left_capacity == 2
    assert table_of_three.has_free_spot()


def test_assign_seat_untill_full(table_of_three):
    table_of_three.assign_seat("Fred")
    table_of_three.assign_seat("Amine")
    table_of_three.assign_seat("Vanessa")
    assert table_of_three.left_capacity == 0
    assert not table_of_three.has_free_spot()


def test_assign_seat_table_is_full_error(full_table):
    with pytest.raises(TableIsFullError) as excinfo:
        full_table.assign_seat("Bryan")
    assert "The table is currently full (capacity: 0/3)" in str(excinfo.value)
    assert full_table.left_capacity == 0
    assert not full_table.has_free_spot()


def test_table_with_capacity_zero():
    table_zero = Table(0)
    assert table_zero.capacity == 0
    assert table_zero.left_capacity == 0
    assert not table_zero.has_free_spot()
    with pytest.raises(TableIsFullError):
        table_zero.assign_seat("Bryan")
