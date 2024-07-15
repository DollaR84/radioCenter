from dataclasses import dataclass
from typing import Callable

import addonHandler
import ui

import wx

from .player import Player

from . import vlc\

from .types import PriorityType, SoundType


addonHandler.initTranslation()


@dataclass
class RadioTestData:
    callback_after: Callable
    url: str

    name: str | None = None
    priority: PriorityType | None = None
    station_index: int | None = None

    is_success: bool = False


class RadioTester:

    def __init__(self, data: RadioTestData, repeat_count: int, is_speech_mode: bool = True):
        self.data = data
        self.repeat_count = repeat_count
        self.is_speech_mode = is_speech_mode

        self.instance = vlc.Instance('--no-video', '--input-repeat=-1')
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(self.data.url)
        self.player.set_media(self.media)
        self.player.audio_set_mute(True)
        self.player.play()

        self.repeats = 0
        if self.is_speech_mode:
            ui.message(_("link checking started"))
        wx.CallLater(1000, self.check)

    def check(self):
        state = self.player.get_state()
        self.data.is_success = state == vlc.State.Playing

        if not self.data.is_success and self.repeats < self.repeat_count:
            self.repeats += 1
            if self.is_speech_mode:
                Player.play(SoundType.Move)
            wx.CallLater(1000, self.check)

        else:
            self.finish()

    def finish(self):
        self.player.stop()
        self.media.release()
        self.player.release()

        if self.data.is_success:
            if self.is_speech_mode:
                Player.play(SoundType.Success)
                ui.message(_("The link to the radio station audio stream has been successfully verified"))
        else:
            if self.is_speech_mode:
                Player.play(SoundType.Failure)
                ui.message(_("The link to the radio station audio stream is not working"))

        self.data.callback_after(self.data)
