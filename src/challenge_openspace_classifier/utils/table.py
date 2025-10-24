from challenge_openspace_classifier.utils.seat import Seat


class TableIsFullError(Exception):
    pass


class Table:
    def __init__(self, capacity: int) -> None:
        self.__capacity = capacity
        self.__seats: list[Seat] = [Seat() for _ in range(capacity)]

    @property
    def capacity(self) -> int:
        return self.__capacity

    @property
    def left_capacity(self) -> int:
        return sum(1 for seat in self.__seats if seat.free)

    def has_free_spot(self) -> bool:
        return any(seat.free for seat in self.__seats)

    def assign_seat(self, name) -> None:
        empty_seat = next((seat for seat in self.__seats if seat.free), None)
        if empty_seat:
            empty_seat.set_occupant(name)
        else:
            raise TableIsFullError(
                f"Cannot assign seat: The table is currently full (capacity: {self.left_capacity}/{self.__capacity})"
            )
