import random
from typing import List, Optional

from .table import Table


class OpenSpace:
    def __init__(
        self, tables_per_room: Optional[int] = 6, seats_per_table: Optional[int] = 4
    ) -> None:
        if tables_per_room is None or seats_per_table is None:
            raise ValueError("tables_per_room and seats_per_table must be provided")
        self.__tables: List[Table] = [
            Table(seats_per_table) for _ in range(tables_per_room)
        ]

    def __str__(self) -> str:
        header = f"OpenSpace(tables={len(self.tables)}, capacity={self.capacity}, left={self.left_capacity})"
        tables_block = "\n".join(str(table) for table in self.__tables)
        return header + ("\n" + tables_block if tables_block else "")

    @property
    def tables(self) -> List[Table]:
        return self.__tables

    @property
    def capacity(self) -> int:
        # total number of seats in the room
        return sum(t.capacity for t in self.__tables)

    @property
    def left_capacity(self) -> int:
        return sum(t.left_capacity for t in self.__tables)

    def seat_people_randomly(self, names: List[str]) -> List[str]:
        """Randomly distribute people across tables.

        - Shuffles the provided list to ensure random assignment.
        - Fills tables sequentially (any free table) with the shuffled names.
        - Returns a list of names that could not be seated if capacity is exceeded.
        """
        names_shuffled = list(filter(None, (n.strip() for n in names)))
        random.shuffle(names_shuffled)

        unseated: List[str] = []
        for name in names_shuffled:
            available_table = next(
                (table for table in self.__tables if table.has_free_spot()), None
            )
            if available_table:
                available_table.assign_seat(name)
            else:
                unseated.append(name)

        return unseated

    def formatted_layout(self) -> str:
        """Return a multi-line string showing all tables and seat occupants."""
        lines: List[str] = []
        for idx, table in enumerate(self.__tables, start=1):
            occ = [o if o is not None else "-" for o in table.occupants]
            lines.append(f"Table {idx}: [" + ", ".join(occ) + "]")
        return "\n".join(lines)
