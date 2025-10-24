import csv
from pathlib import Path

import pytest

from challenge_openspace_classifier.utils.file_utils import FileUtils

STANDARD_HEADER = ["First Name", "Last Name", "Nationality"]
STANDARD_ROWS = [
    ["Pat", "Senna", "american"],
    ["John", "Doe", "belgian"],
    ["Dave", "Paladin", ""],
]


@pytest.fixture
def standard_csv_path(tmp_path: Path) -> Path:
    filepath = tmp_path / "standard_data.csv"
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(STANDARD_HEADER)
        writer.writerows(STANDARD_ROWS)
    return filepath


@pytest.fixture
def empty_csv_file_path(tmp_path: Path) -> Path:
    filepath = tmp_path / "empty_data.csv"
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(STANDARD_HEADER)
    return filepath


def test_from_csv_successful_read(standard_csv_path: Path):
    result = FileUtils.from_csv(standard_csv_path, "Last Name")
    assert result == ["Senna", "Doe", "Paladin"]


def test_from_csv_read_with_empty_strings(standard_csv_path: Path):
    result = FileUtils.from_csv(standard_csv_path, "Nationality")
    assert result == ["american", "belgian", ""]


def test_from_csv_file_not_found(capfd: pytest.CaptureFixture[str], tmp_path: Path):
    non_existent_path = tmp_path / "non_existent_file.csv"
    result = FileUtils.from_csv(non_existent_path, "Nationality")
    out, err = capfd.readouterr()

    assert result == []
    assert f"Error: File not found at {non_existent_path}" in out


def test_from_csv_missing_header_raise_key_error(standard_csv_path):
    with pytest.raises(KeyError) as excinfo:
        FileUtils.from_csv(standard_csv_path, "T")
    assert "does not contain a header named 'T'" in str(excinfo.value)
    assert "Found headers: ['First Name', 'Last Name', 'Nationality']" in str(
        excinfo.value
    )


def test_from_csv_empty_csv_file(empty_csv_file_path: Path):
    result = FileUtils.from_csv(empty_csv_file_path, "First Name")
    assert result == []

