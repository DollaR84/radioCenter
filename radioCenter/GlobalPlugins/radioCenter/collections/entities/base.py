from __future__ import annotations

from abc import ABC, abstractmethod
import re
from typing import List

from ...utils.parsers.base import BaseParser


class BaseCollection(BaseParser, ABC):
    _collections: dict[str, BaseCollection] = {}

    def __init_subclass__(cls, **kwargs):
        name = cls.get_name()
        if name not in cls._collections:
            cls._collections[name] = cls

    @classmethod
    def get_name(cls):
        _name = cls.__name__.replace("Collection", "")
        return " ".join([word for word in re.findall(r"[A-Z][a-z0-9]+", _name)])

    @classmethod
    def get_collection(cls, name: str, **kwargs) -> BaseCollection:
        return cls._collections.get(name)(name, **kwargs)

    @classmethod
    def get_collections_names(cls) -> List[str]:
        data = dict(sorted(cls._collections.items(), key=lambda item: item[1].order_id))
        return list(data.keys())

    @property
    def is_available(self) -> bool:
        return True

    def __init__(self, name: str):
        self.name = name

    def parse(self) -> List[CollectionData]:
        return self.process_data(self.make_url())

    @abstractmethod
    def make_url(self, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def process_data(self, url: str) -> List[CollectionData]:
        raise NotImplementedError

    @abstractmethod
    def load(self, url: str) -> list:
        raise NotImplementedError

    @abstractmethod
    def read(self, item) -> CollectionData:
        raise NotImplementedError
