from dataclasses import dataclass

from .stations import Station

from .types import SortType


@dataclass
class Config:
    stations: list[Station]

    volume: int = 50
    is_muted: bool = False

    record_path: str = ""

    repeat_count: int = 10
    sort_type: SortType = SortType.Nothing
