import sys
from pathlib import Path

import challenge_openspace_classifier.utils.openspace_encoder
from challenge_openspace_classifier.utils.file_utils import FileUtils
from challenge_openspace_classifier.utils.openspace import OpenSpace


def _clean_names(names: list[str]) -> list[str]:
    return [n.strip() for n in names if isinstance(n, str) and n.strip()]


def get_source_path() -> Path | None:
    """Get path from argv or prompt the user."""
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    if not path_arg:
        try:
            path_arg = input(
                "Enter path to CSV file (with a 'Names' column or a single-column list): "
            ).strip()
        except EOFError:
            print("No input provided. Exiting.")
            return None

    source_path = Path(path_arg)
    if not source_path.exists():
        print(f"Error: File not found at {source_path}")
        return None
    return source_path


def load_and_clean_names(source_path: Path) -> list[str]:
    """Load names from a CSV file, cleaning it if necessary."""
    try:
        names = FileUtils.from_csv(source_path, "Names")
    except KeyError:
        clean_path = FileUtils.add_header_and_write_clean(
            source_path.parent, source_path.name, ["Names"]
        )
        names = FileUtils.from_csv(clean_path, "Names")
    return _clean_names(names)


def print_summary(names: list[str], unseated: list[str], space: OpenSpace):
    """Prints a summary of the seating arrangement."""
    seated_count = len(names) - len(unseated)
    print(
        f"Total names: {len(names)} | Seated: {seated_count} | Unseated: {len(unseated)}"
    )
    if unseated:
        people_v_pers = "people" if (len(unseated) > 1) else "person"
        reason = (
            "could only seat this person alone on a table"
            if space.left_capacity > 0
            else "not enough capacity"
        )
        print(f"Unseated {people_v_pers} ({reason}):")
        print("\n".join(f"- {name}" for name in unseated))
    # Display all tables and their occupants
    print("\nRoom layout:")
    print(space.formatted_layout())


def main() -> None:
    source_path = get_source_path()
    if not source_path:
        return

    names = load_and_clean_names(source_path)
    if not names:
        print("No names found to seat.")
        return

    # Create an OpenSpace and distribute randomly
    space = OpenSpace()
    unseated = space.seat_people_randomly(names)

    print_summary(names, unseated, space)

    # Save the state of the openspace to a JSON file
    output_path = source_path.parent / "openspace.json"
    FileUtils.save_to_json(output_path, space)
    print(f"\nOpenSpace state saved to {output_path}")

