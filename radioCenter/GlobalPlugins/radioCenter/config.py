from dataclasses import dataclass, field

from .stations import Station

from .types import SortType


@dataclass
class Config:
    stations: list[Station] = field(default_factory=list)

    volume: int = 50
    is_muted: bool = False

    record_path: str = ""

    repeat_count: int = 10
    repeat_count_collection: int = 3
    verify_part_count_limit: int = 50

    sort_type: SortType = SortType.Nothing
