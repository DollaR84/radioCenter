import os
import pickle
from typing import Dict, Union

import globalVars
from logHandler import log

from .collections import CollectionDataExt

from .config import Config


class Saver:

    def __init__(self):
        base_dir = globalVars.appArgs.configPath
        self.file_name = os.path.join(base_dir, 'radio_center.dat')
        self.collections_file_name = os.path.join(base_dir, 'radio_collections.dat')

    def save(self, config: Config):
        with open(self.file_name, 'wb') as data_file:
            pickle.dump(config, data_file)

    def load(self) -> Config:
        config = Config()
        try:
            data_file = open(self.file_name, 'rb')
            config = pickle.load(data_file)

            config = self.fixed_stations(config)
        except Exception:
            pass

        return config

    def fixed_stations(self, config: Config) -> Config:
        if not hasattr(config.stations[0], 'id'):
            config.stations = [
                Station(id=index, manual_id=index, name=old_station.name, url=old_station.url)
                for index, old_station in enumerate(config.stations, start=1)
            ]
            self.save(config)

        if not hasattr(config.stations[0], 'manual_id'):
            config.stations = [
                Station(id=old_station.id, manual_id=old_station.id, name=old_station.name, url=old_station.url)
                for old_station in config.stations
            ]
            self.save(config)

        return config

    def save_collections(self, collections_data: Dict[str, Union[CollectionDataExt, None]]):
        if not collections_data:
            return

        with open(self.collections_file_name, 'wb') as data_file:
            pickle.dump(collections_data, data_file)

    def load_collections(self) -> Dict[str, Union[CollectionDataExt, None]]:
        collections_data = {}

        if not os.path.exists(self.collections_file_name) or not os.path.isfile(self.collections_file_name):
            return collections_data

        try:
            with open(self.collections_file_name, 'rb') as data_file:
                collections_data = pickle.load(data_file)

        except Exception as error:
            os.remove(self.collections_file_name)
            log.error(error, exc_info=True)

        return collections_data
