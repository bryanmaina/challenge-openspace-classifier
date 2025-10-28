import pytest

from challenge_openspace_classifier.utils.seat import Seat, SeatNotAvailableError


@pytest.fixture
def empty_seat() -> Seat:
    """Provides a fresh, empty seat instance for testing"""
    return Seat()


@pytest.fixture
def occupied_seat() -> Seat:
    """Provides a fresh, empty seat instance for testing"""
    return Seat(occupant="Astha")


def test_initialization_empty(empty_seat: Seat):
    assert empty_seat.occupant is None
    assert empty_seat.free


def test_initialization_occupied(occupied_seat: Seat):
    assert occupied_seat.occupant == "Astha"
    assert not occupied_seat.free


def test_set_occupant_success(empty_seat: Seat):
    empty_seat.set_occupant("Kristin")
    assert empty_seat.occupant == "Kristin"
    assert not empty_seat.free


def test_set_occupant_invalid(empty_seat: Seat):
    with pytest.raises(ValueError) as excinfo:
        empty_seat.set_occupant("")
    assert "A string is required. (occupant='')" in str(excinfo.value)
    assert empty_seat.occupant is None


def test_set_occupant_failure(occupied_seat: Seat):
    with pytest.raises(SeatNotAvailableError) as excinfo:
        occupied_seat.set_occupant("Bryan")
    assert "already occupied by Astha" in str(excinfo.value)
    assert occupied_seat.occupant == "Astha"


def test_remove_occupant_success(occupied_seat: Seat):
    removed_occupant = occupied_seat.remove_occupant()
    assert removed_occupant == "Astha"
    assert occupied_seat.occupant is None
    assert occupied_seat.free


def test_remove_occupant_empty(empty_seat: Seat):
    removed_occupant = empty_seat.remove_occupant()
    assert removed_occupant is None
    assert empty_seat.occupant is None
    assert empty_seat.free
