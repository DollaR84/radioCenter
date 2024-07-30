from dataclasses import dataclass
from operator import attrgetter
from typing import List, Set, Union

import wx

from .types import SortType, PriorityType


@dataclass
class Station:
    id: int
    manual_id: int
    name: str
    url: str

    priority: PriorityType = PriorityType.Middle
    is_selected: bool = False

    @property
    def name_url(self) -> str:
        return f"{self.name}: {self.url}"

    @property
    def priority_status(self) -> int:
        return list(PriorityType).index(self.priority)


class StationsControl:

    def __init__(self, stations: List[Station]):
        self.stations = stations

    def check_and_fix_ids(self) -> bool:
        need_fix_id = len(self.stations) != len(list(set([station.id for station in self.stations])))
        need_fix_manual_id = len(self.stations) != len(list(set([station.manual_id for station in self.stations])))
        if not need_fix_id and not need_fix_manual_id:
            return False

        ids: set[int] = set()
        manual_ids: set[int] = set()

        for station in self.stations:
            if need_fix_id:
                station.id = self.fix_id(station.id, ids)
            if need_fix_manual_id:
                station.manual_id = self.fix_id(station.manual_id, manual_ids)

        return True

    def fix_id(self, id_: int, fix_set: Set[int]):
        new_id = id_
        while new_id in fix_set:
            new_id += 1
        fix_set.add(new_id)
        return new_id

    @property
    def selected_index(self) -> int:
        index = 0
        for i, station in enumerate(self.stations):
            if station.is_selected:
                index = i
                break
        return index

    @property
    def selected(self) -> Station:
        for station in self.stations:
            if station.is_selected:
                result = station
                break
        else:
            if not self.stations:
                raise ValueError("error in requesting an installed station when the list is empty")

            result = self.stations[0]
            result.is_selected = True
        return result

    def select(self, station: Station) -> int:
        return self.select_name(station.name_url)

    def select_name(self, name_url: str) -> int:
        index = 0
        for i, station in enumerate(self.stations):
            station.is_selected = station.name_url == name_url
            if station.is_selected:
                index = i
        return index

    def change_station(self, index: int) -> Station:
        try:
            station = self.stations[index]
        except Exception:
            station = self.stations[0]

        self.select(station)
        return station

    def next(self) -> Station:
        index = self.selected_index + 1
        if index >= len(self.stations):
            index = 0

        return self.change_station(index)

    def previous(self) -> Station:
        index = self.selected_index - 1
        if index < 0:
            index = len(self.stations) - 1

        return self.change_station(index)

    def sort(self, sort_by: SortType) -> List[Station]:
        if sort_by == SortType.Nothing:
            self.stations.sort(key=attrgetter('id'))

        elif sort_by == SortType.Manual:
            self.stations.sort(key=attrgetter('manual_id'))

        elif sort_by in (SortType.NameDirect, SortType.NameReverse,):
            is_reverse = sort_by == SortType.NameReverse
            self.stations.sort(
                key=lambda station: attrgetter('name')(station).lower(),
                reverse=is_reverse,
            )

        elif sort_by in (SortType.PriorityDirect, SortType.PriorityReverse,):
            is_reverse = sort_by == SortType.PriorityReverse
            self.stations.sort(
                key=lambda station: (
                    attrgetter('priority_status')(station),
                    attrgetter('name')(station).lower(),
                ),
                reverse=is_reverse,
            )

        return self.stations

    def check_unique_url(self, url: str) -> bool:
        unique_urls = list(set([station.url for station in self.stations]))
        return url not in unique_urls

    def create(self, name: str, url: str, priority: PriorityType) -> Union[Station, None]:
        index = len(self.stations)
        if self.check_unique_url(url):
            station = Station(id=index, manual_id=index, name=name, url=url, priority=priority)
            self.stations.append(station)
            return station
        return None

    def add(self, name: str, url: str, priority: PriorityType, sort_by: SortType) -> Union[int, None]:
        new_position = None
        station = self.create(name, url, priority)
        self.check_and_fix_ids()
        if station:
            self.sort(sort_by)
            new_position = self.select(station)
        return new_position

    def remove(self, index: int) -> int:
        if index >= len(self.stations):
            return index

        self.stations.pop(index)
        if len(self.stations) > 0:
            index = index - 1
            if index < 0:
                index = 0        

            station = self.stations[index]
            self.select(station)
        return index

    def manual_sort(self, index: int, order_type) -> Union[int, None]:
        station1 = self.stations[index]
        if order_type == wx.WXK_UP and index > 0:
            station2 = self.stations[index - 1]
        elif order_type == wx.WXK_DOWN and index < len(self.stations) - 1:
            station2 = self.stations[index + 1]
        else:
            return None

        station1.manual_id, station2.manual_id = station2.manual_id, station1.manual_id
        self.sort(SortType.Manual)
        return station1.manual_id - 1
