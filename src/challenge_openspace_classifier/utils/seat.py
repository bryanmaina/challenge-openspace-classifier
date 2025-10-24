from typing import Optional


class SeatNotAvailabeError(Exception):
    """Raised why trying to set an occcupant on an already occupied seat"""

    pass


class Seat:
    def __init__(self, occupant: Optional[str] = None) -> None:
        self.__occupant = occupant

    @property
    def free(self) -> bool:
        return self.__occupant is None

    @property
    def occupant(self) -> Optional[str]:
        return self.__occupant

    def set_occupant(self, occupant: str) -> None:
        if not occupant:
            raise ValueError(
                f"The 'occupant' attribute cannot be None. A string is required. ({occupant=})"
            )
        if not self.free:
            raise SeatNotAvailabeError(
                f"Cannot set occupant: container is already occupied by {self.__occupant}."
            )
        self.__occupant = occupant

    def remove_occupant(self) -> Optional[str]:
        if self.__occupant is None:
            return self.__occupant
        prev = self.__occupant
        self.__occupant = None
        return prev
