from dataclasses import dataclass

from .stations import Station

from .types import SortType


@dataclass
class Config:
    stations: list[Station]

    volume: int = 50
    is_muted: bool = False

    record_path: str = ""

    sort_type: SortType = SortType.Nothing
