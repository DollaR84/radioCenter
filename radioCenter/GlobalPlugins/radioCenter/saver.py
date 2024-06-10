import os
import pickle

import globalVars

from .config import Config, Station


class Saver:

    def __init__(self):
        base_dir = globalVars.appArgs.configPath
        self.file_name = os.path.join(base_dir, 'radio_center.dat')

    def get_default(self) -> Config:
        station = Station(
            name="Gomer",
            url='https://homer.in.ua/listen/radio_homer/radio128.aac',
        )
        return Config(stations=[station])

    def save(self, config: Config):
        with open(self.file_name, 'wb') as data_file:
            pickle.dump(config, data_file)

    def load(self) -> Config:
        config = self.get_default()
        try:
            data_file = open(self.file_name, 'rb')
            config = pickle.load(data_file)
        except Exception:
            pass

        return config
