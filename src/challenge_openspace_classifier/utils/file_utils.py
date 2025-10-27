import csv
from pathlib import Path
from collections.abc import Iterable


class FileUtils:
    @staticmethod
    def from_csv(filepath: Path, header_name: str) -> list[str]:
        path = Path(filepath)
        data_list: list[str] = []
        try:
            with open(path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if not reader.fieldnames or header_name not in reader.fieldnames:
                    raise KeyError(
                        f"The CSV file at '{path}' does not contain a header named '{header_name}'.\nFound headers: {reader.fieldnames}"
                    )
                data_list = [row[header_name] for row in reader]
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
            return []

        return data_list

    @staticmethod
    def add_header_and_write_clean(
        dirpath: Path, filename: str, headers: Iterable[str]
    ) -> Path:
        src_path = Path(dirpath) / filename
        dst_path = Path(dirpath) / f"clean_{filename}"

        header_line = ",".join(headers) + "\n"
        try:
            with open(dst_path, mode="w", encoding="utf-8") as out_file:
                out_file.write(header_line)
                with open(src_path, mode="r", encoding="utf-8") as in_file:
                    out_file.write(in_file.read())
        except FileNotFoundError:
            # If the source does not exist, still create the destination with just the header
            with open(dst_path, mode="w", encoding="utf-8") as out_file:
                out_file.write(header_line)
        return dst_path
