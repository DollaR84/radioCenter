import addonHandler

import wx

from ..client import RadioClient


addonHandler.initTranslation()


class BaseGUI:

    def __init__(self, client: RadioClient):
        self.radio: RadioClient = client


class LabelsGUI(BaseGUI):

    @property
    def play_label(self) -> str:
        return _("Pause") if self.radio.need_paused else _("Play")

    @property
    def record_label(self) -> str:
        return _("Stop record") if self.radio.is_recording else _("Record")

    @property
    def mute_label(self) -> str:
        return _("Unmute") if self.radio.config.is_muted else _("Mute")
