import random

from challenge_openspace_classifier.utils.table import Table


class OpenSpace:
    def __init__(
        self, tables_per_room: int | None = 6, seats_per_table: int | None = 4
    ) -> None:
        if tables_per_room is None or seats_per_table is None:
            raise ValueError("tables_per_room and seats_per_table must be provided")
        self.__tables: list[Table] = [
            Table(seats_per_table) for _ in range(tables_per_room)
        ]

    def __str__(self) -> str:
        header = f"OpenSpace(tables={len(self.tables)}, capacity={self.capacity}, left={self.left_capacity})"
        tables_block = "\n".join(str(table) for table in self.__tables)
        return header + ("\n" + tables_block if tables_block else "")

    @property
    def tables(self) -> list[Table]:
        return self.__tables

    @property
    def capacity(self) -> int:
        # total number of seats in the room
        return sum(t.capacity for t in self.__tables)

    @property
    def left_capacity(self) -> int:
        return sum(t.left_capacity for t in self.__tables)

    def seat_people_randomly(self, names: list[str]) -> list[str]:
        """Randomly distribute people across tables.

        Rules with a goal to avoid single-person tables when possible:
        - Shuffle the provided list to ensure randomization.
        - Prefer adding to tables that already have someone (especially tables with exactly 1 occupant).
        - Open a new empty table only when at least two people remain to be seated, or no non-empty table has space.
        - Return a list of names that could not be seated if capacity is exceeded.
        """
        names_shuffled = list(filter(None, (n.strip() for n in names)))
        random.shuffle(names_shuffled)

        #  to derive occupancy for a given table
        def occupancy(table: Table) -> int:
            return table.capacity - table.left_capacity

        unseated: list[str] = []
        total = len(names_shuffled)
        for idx, name in enumerate(names_shuffled):
            remaining = total - idx
            free_tables = [t for t in self.__tables if t.left_capacity > 0]
            if not free_tables:
                unseated.append(name)
                continue

            non_empty_with_space = [t for t in free_tables if occupancy(t) > 0]
            if non_empty_with_space:
                # Prefer the table with the smallest positive occupancy (1 first), to pair singles
                selected = min(non_empty_with_space, key=occupancy)
                selected.assign_seat(name)
                continue

            # Only empty tables have space at this point
            empty_tables = [t for t in free_tables if occupancy(t) == 0]
            if empty_tables:
                # Avoid opening a table for a single last person when possible
                if remaining >= 2:
                    empty_tables[0].assign_seat(name)
                else:
                    # Last person and only empty tables left; to avoid someone alone at a table, leave unseated
                    unseated.append(name)
            else:
                unseated.append(name)

        return unseated

    def formatted_layout(self) -> str:
        """Return a multi-line string showing all tables and seat occupants."""
        lines: list[str] = []
        for idx, table in enumerate(self.__tables, start=1):
            occ = [o if o is not None else "-" for o in table.occupants]
            lines.append(f"Table {idx}: [" + ", ".join(occ) + "]")
        return "\n".join(lines)
