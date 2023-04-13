"""Module for utility functions"""
from pathlib import Path
from types import NoneType
from typing import Union, Any


BASE_DATA_DIR = Path("./data/")


def open_file(rel_path: Union[Path, str]) -> Any:
    with open(BASE_DATA_DIR / rel_path) as file:
        return file.read().strip()


def save_file(data: str, rel_path: Union[Path, str]) -> NoneType:
    with open(BASE_DATA_DIR / rel_path, "w") as file:
        file.write(data)
