from __future__ import annotations

from abc import ABC, abstractmethod
import re
import requests

from logHandler import log


class BaseCollection(ABC):
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
    def get_collection(cls, name: str) -> BaseCollection:
        return cls._collections.get(name)(name)

    @classmethod
    def get_collections_names(cls) -> list[str]:
        data = dict(sorted(cls._collections.items(), key=lambda item: item[1].order_id))
        return list(data.keys())

    def __init__(self, name: str):
        self.name = name

    def get_request(self, url: str):
        content = ""

        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.content.decode("utf-8")
        except Exception as error:
            log.error(error, exc_info=True)

        return content

    def parse(self) -> list[CollectionData]:
        return self.process_data(self.make_url())

    @abstractmethod
    def make_url(self, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def process_data(self, url: str) -> list[CollectionData]:
        raise NotImplementedError

    @abstractmethod
    def load(self, url: str) -> list:
        raise NotImplementedError

    @abstractmethod
    def read(self, item) -> CollectionData:
        raise NotImplementedError
