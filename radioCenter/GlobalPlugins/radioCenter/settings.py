import addonHandler
import gui
from gui.settingsDialogs import SettingsPanel

import wx

from .client import RadioClient


addonHandler.initTranslation()


class RadioSettings(SettingsPanel):
    title = "RadioCenter"
    radio: RadioClient = None

    def makeSettings(self, settingsSizer):
        settings_sizer_helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        browse_text = _("Browse...")
        dir_dialog_title = _("Select a directory")

        group_sizer = wx.StaticBoxSizer(
            wx.VERTICAL, self,
            label=_("Path to record folder"),
        )
        group_box = group_sizer.GetStaticBox()
        group_helper = settings_sizer_helper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=group_sizer))

        directory_path_helper = gui.guiHelper.PathSelectionHelper(group_box, browse_text, dir_dialog_title)
        directory_entry_control = group_helper.addItem(directory_path_helper)

        self.record_path = directory_entry_control.pathControl
        self.record_path.Value = self.radio.config.record_path

    def onSave(self):
        self.radio.config.record_path = self.record_path.GetValue()
        self.radio.save()
