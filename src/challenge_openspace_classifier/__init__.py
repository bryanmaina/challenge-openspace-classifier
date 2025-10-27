import sys
from pathlib import Path
from typing import List

from challenge_openspace_classifier.utils.file_utils import FileUtils
from challenge_openspace_classifier.utils.openspace import OpenSpace


def _clean_names(names: List[str]) -> List[str]:
    return [n.strip() for n in names if isinstance(n, str) and n.strip()]


def main() -> None:
    # Get path from argv or prompt the user
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    if not path_arg:
        try:
            path_arg = input(
                "Enter path to CSV file (with a 'Names' column or a single-column list): "
            ).strip()
        except EOFError:
            print("No input provided. Exiting.")
            return

    source_path = Path(path_arg)

    if not source_path.exists():
        print(f"Error: File not found at {source_path}")
        return

    # Try reading 'Names' column; if missing, create a clean_ file with a header and try again
    try:
        names = FileUtils.from_csv(source_path, "Names")
    except KeyError:
        clean_path = FileUtils.add_header_and_write_clean(
            source_path.parent, source_path.name, ["Names"]
        )
        names = FileUtils.from_csv(clean_path, "Names")

    names = _clean_names(names)
    if not names:
        print("No names found to seat.")
        return

    # Create an OpenSpace and distribute randomly
    space = OpenSpace()
    unseated = space.seat_people_randomly(names)

    seated_count = len(names) - len(unseated)
    print(
        f"Total names: {len(names)} | Seated: {seated_count} | Unseated: {len(unseated)}"
    )
    if unseated:
        print("Unseated people (not enough capacity):")
        print("\n".join(f"- {name}" for name in unseated))

    # Display all tables and their occupants using __str__ representations
    print("\nRoom layout:")
    print(space.formatted_layout())
