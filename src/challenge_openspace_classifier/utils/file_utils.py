import csv
from pathlib import Path
from typing import List


class FileUtils:
    @staticmethod
    def from_csv(filepath: Path, header_name: str) -> List[str]:
        data_list: List[str] = []
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if not reader.fieldnames or header_name not in reader.fieldnames:
                    raise KeyError(
                        f"The CSV file at '{filepath}' does not contain a header named '{header_name}'.\nFound headers: {reader.fieldnames}"
                    )
                data_list = [row[header_name] for row in reader]
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return []

        return data_list
