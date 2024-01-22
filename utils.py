import datetime
import csv
from dataclasses import dataclass


def write_csv(filename: str, field_names: list[str], data: str) -> None:
    with open(filename, 'w') as f:
        f.write(f"{','.join(field_names)}\n")
        f.write(data)


def read_csv(filename: str, ) -> list[dict]:
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def get_formatted_time() -> str:
    return datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")


@dataclass
class PACTest:
    result: str
    elapsed_time: int
