import addonHandler
import globalPluginHandler
import gui
import scriptHandler

import      wx

from .client import RadioClient

from .gui import RadioGUI

from .settings import RadioSettings


addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "RadioCenter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.radio: RadioClient = RadioClient()
        RadioSettings.radio = self.radio
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(RadioSettings)

    @scriptHandler.script(
        description=_("play/pause radio"),
        gesture="kb:NVDA+ALT+P"
    )
    def script_play(self, gesture):
        self.radio.play(scriptHandler.getLastScriptRepeatCount() + 1)

    @scriptHandler.script(
        description=_("volume up"),
        gesture="kb:NVDA+ALT+UpArrow"
    )
    def script_volume_up(self, gesture):
        self.radio.volume_up()

    @scriptHandler.script(
        description=_("volume down"),
        gesture="kb:NVDA+ALT+DownArrow"
    )
    def script_volume_down(self, gesture):
        self.radio.volume_down()

    @scriptHandler.script(
        description=_("station next"),
        gesture="kb:NVDA+ALT+RightArrow"
    )
    def script_station_up(self, gesture):
        self.radio.station_up()

    @scriptHandler.script(
        description=_("station previous"),
        gesture="kb:NVDA+ALT+LeftArrow"
    )
    def script_station_down(self, gesture):
        self.radio.station_down()

    @scriptHandler.script(
        description=_("get station info"),
        gesture="kb:NVDA+ALT+O"
    )
    def script_info(self, gesture):
        self.radio.get_info()

    @scriptHandler.script(
        description=_("open radio window"),
        gesture="kb:NVDA+ALT+R"
    )
    def script_open_window(self, gesture):
        wx.CallAfter(RadioGUI.create_radio_gui, self.radio)
        