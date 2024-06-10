from dataclasses import dataclass


@dataclass
class Station:
    name: str
    url: str


@dataclass
class Config:
    stations: list[Station]
    current: int = 0

    volume: int = 50
    is_muted: bool = False

    record_path: str = ""
