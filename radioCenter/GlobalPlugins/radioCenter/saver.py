from enum import Enum
import os
import pickle

import globalVars

from .config import Config, Station


class Saver:

    def __init__(self):
        base_dir = globalVars.appArgs.configPath
        self.file_name = os.path.join(base_dir, 'radio_center.dat')

    @property
    def default(self) -> Config:
        station = Station(
            id=1,
            manual_id=1,
            name="Homer",
            url='https://homer.in.ua/listen/radio_homer/radio128.aac',
        )
        return Config(stations=[station])

    def save(self, config: Config):
        with open(self.file_name, 'wb') as data_file:
            pickle.dump(config, data_file)

    def load(self) -> Config:
        config = self.default
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
