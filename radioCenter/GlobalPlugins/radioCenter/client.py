import os

import addonHandler
from logHandler import log
import ui

import wx

from . import vlc\

from .config import Config, Station

from .saver import Saver


addonHandler.initTranslation()


class RadioClient:

    def __init__(self):
        self.saver: Saver = Saver()
        self.config: Config = self.saver.load()
        if len(self.config.stations) <= self.config.current:
            self.config.current = 0

        self.instance = vlc.Instance('--no-video', '--input-repeat=-1')
        self.player = None
        self.media = None

        self._need_paused: bool = False
        self._is_recording: bool = False

        self.track_process = None

        self.data = dict.fromkeys([
            vlc.Meta.Title,
            vlc.Meta.Artist,
            vlc.Meta.Genre,
            vlc.Meta.Copyright,
            vlc.Meta.Album,
            vlc.Meta.TrackNumber,
            vlc.Meta.Description,
            vlc.Meta.Rating,
            vlc.Meta.Date,
            vlc.Meta.Setting,
            vlc.Meta.URL,
            vlc.Meta.Language,
            vlc.Meta.NowPlaying,
            vlc.Meta.Publisher,
            vlc.Meta.EncodedBy,
            vlc.Meta.ArtworkURL,
            vlc.Meta.TrackID,
            vlc.Meta.TrackTotal,
            vlc.Meta.Director,
            vlc.Meta.Season,
            vlc.Meta.Episode,
            vlc.Meta.ShowName,
            vlc.Meta.Actors,
            vlc.Meta.AlbumArtist,
            vlc.Meta.DiscNumber,
            vlc.Meta.DiscTotal,
        ], None)

    def play(self, count: int = 1):
        if self.is_playing:
            if count > 1:
                self.release()
            else:
                self.player.pause()
                self._need_paused = False

        else:
            if count > 1:
                self.release()
            else:
                if not self._need_paused:
                    self.set_media()
                self.player.play()
                self._need_paused = True
                if self.track_process:
                    self.track_process.Stop()
                self.track_process = wx.CallLater(5 * 1000, self.track_data)

    def stop(self):
        self._need_paused = False
        if self.player:
            self.player.stop()

        if self.media:
            self.media.release()
            self.media = None

        if self.track_process:
            self.track_process.Stop()
            self.track_process = None

    def release(self, need_speak_phrase: bool = True):
        if self.player:
            self.stop()
            self.player.release()
            self.player = None

            if need_speak_phrase:
                ui.message(_("radio turned off"))

    def set_media(self, commands: list[str] = []):
        station = self.config.stations[self.config.current]
        self.media = self.instance.media_new(station.url, *commands)
        self.media.get_mrl()

        if not self.player:
            self.player = self.instance.media_player_new()
            self.player.audio_set_volume(self.config.volume)
        self.player.set_media(self.media)

    def change_station(self, index: int):
        need_playing = self.is_playing
        self.stop()
        self.config.current = index
        self.set_media()
        self.save()

        if need_playing:
            self.play()

    def station_up(self):
        index = self.config.current + 1
        if len(self.config.stations) == index:
            index = 0
        self.change_station(index)

    def station_down(self):
        index = self.config.current - 1
        if index < 0:
            index = len(self.config.stations) - 1
        self.change_station(index)

    def change_volume(self, volume: int):
        self.config.volume = volume
        volume = 0 if self.config.is_muted else volume
        self.player.audio_set_volume(volume)
        self.save()

    def volume_up(self):
        volume = self.config.volume + 5
        if volume > 100:
            volume = 100
        else:
            self.change_volume(volume)

    def volume_down(self):
        volume = self.config.volume - 5
        if volume < 0:
            volume = 0
        else:
            self.change_volume(volume)

    def mute(self):
        self.config.is_muted = not self.config.is_muted
        self.save()

        volume = 0 if self.config.is_muted else self.config.volume
        self.player.audio_set_volume(volume)

    def add_station(self, station: Station) -> int:
        new_position = self.config.current
        unique_urls = list(set([station.url for station in self.config.stations]))
        if station.url not in unique_urls:
            self.config.stations.append(station)
            self.save()
            new_position = len(self.config.stations) - 1
            self.config.current = new_position
        return new_position

    def remove_station(self, index: int) -> int:
        self.config.stations.pop(index)

        if len(self.config.stations) > 0:
            index = index - 1
            if index < 0:
                index = 0
            self.config.current = index

        self.save()
        return index

    def save(self):
        self.saver.save(self.config)

    def speech(self, text: str):
        if text and self.is_playing and not self.config.is_muted:
            ui.message(text)

    def track_data(self):
        if not self.check_media():
            return

        self.media.parse_with_options(vlc.MediaParseFlag.network, 0)
        wx.CallLater(5 * 1000, self.parse_data)

    def parse_data(self):
        if not self.check_media():
            return

        for key in self.data.keys():
            value = self.media.get_meta(key)
            if value != self.data[key]:
                self.data[key] = value
                self.speech(value)

        self.track_process = wx.CallLater(30 * 1000, self.track_data)

    def check_media(self) -> bool:
        result = True
        if not self.media:
            if self.track_process:
                self.track_process.Stop()
                self.track_process = None
            result = False
        return result

    def get_info(self):
        for key, value in self.data.items():
            if value is not None:
                log.info(f"{key}: {value}")
                ui.message(value)

    @property
    def is_stations_available(self):
        return bool(self.config.stations)

    @property
    def is_playing(self) -> bool:
        return self.player and self.player.is_playing()

    @property
    def need_paused(self) -> bool:
        return self._need_paused

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    @property
    def is_recording_allowed(self) -> bool:
        record_path = self.config.record_path
        if record_path and os.path.exists(record_path):
            return True
        return False

    def record(self):
        if not self.is_recording_allowed:
            return

        self._is_recording = not self._is_recording

        if self._is_recording:
            pass
        else:
            audiofile = self.get_name_file_for_record(self.config.record_path)

    def get_name_file_for_record(self, record_path: str, ext: str = ".mp3") -> str:
        names = set(x[:8] for x in os.listdir(record_path) if x.endswith(ext) and len(x) == 12)
        for i in range(10**8):
            filename = "%08i" % i
            if filename not in names:
                return os.path.join(record_path, "".join([filename, ext]))
