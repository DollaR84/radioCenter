import os
from typing import Callable

import addonHandler
from logHandler import log
import ui

import wx

from . import vlc\

from .config import Config

from .recorder import RadioRecorder

from .saver import Saver

from .stations import Station, StationsControl

from .types import SortType, PriorityType


addonHandler.initTranslation()


class RadioClient:

    def __init__(self):
        self.saver: Saver = Saver()
        self.config: Config = self.saver.load()
        self.stations_control = StationsControl(self.config.stations)
        need_fix = self.stations_control.check_and_fix_ids()
        if need_fix:
            self.save()
        self.stations_control.sort(self.config.sort_type)
        self.recorder = None

        self.gui = None

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

    @property
    def stations(self) -> list[Station]:
        return self.stations_control.stations

    def play(self, count: int = 1, url: str | None = None):
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
                    self.set_media(url)
                self.player.play()
                self._need_paused = True

                if self.track_process:
                    self.track_process.Stop()
                self.track_process = wx.CallLater(5 * 1000, self.track_data)

        if self.gui:
            wx.CallLater(1000, self.gui.play_button.SetLabel, self.gui.play_label)

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

    def set_media(self, url: str | None = None, commands: list[str] = []):
        if not url:
            station = self.stations_control.selected
            url = station.url

        self.media = self.instance.media_new(url, *commands)
        self.media.get_mrl()

        if not self.player:
            self.player = self.instance.media_player_new()
            self.player.audio_set_volume(self.config.volume)
        self.player.set_media(self.media)

    def station_up(self):
        need_playing = self.is_playing
        self.release(need_speak_phrase=False)

        self.stations_control.next()
        self.set_media()
        self.save()

        if need_playing:
            self.play()

    def station_down(self):
        need_playing = self.is_playing
        self.release(need_speak_phrase=False)

        self.stations_control.previous()
        self.set_media()
        self.save()

        if need_playing:
            self.play()

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
        if not self.player:
            return

        self.config.is_muted = not self.player.audio_get_mute()
        self.player.audio_set_mute(self.config.is_muted)
        self.save()

    def add_station(self, name: str, url: str, priority: PriorityType) -> int | None:
        new_position = self.stations_control.add(name, url, priority, self.config.sort_type)

        if new_position is not None:
            self.save()
        return new_position

    def remove_station(self, index: int) -> int:
        index = self.stations_control.remove(index)

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
                ui.message(value)

    @property
    def is_stations_available(self):
        return bool(self.config.stations)

    @property
    def is_playing(self) -> bool:
        return bool(self.player) and self.player.is_playing()

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

        if self._is_recording and self.recorder:
            self.recorder.stop()
            self.recorder = None

        else:
            station = self.stations_control.selected
            self.recorder = RadioRecorder(self.gui, self.config.record_path, station.url)

        self._is_recording = not self._is_recording
