import addonHandler
import gui
from gui.settingsDialogs import SettingsPanel
from logHandler import log

import wx

from .client import RadioClient

from .types import SortType


addonHandler.initTranslation()


class RadioSettings(SettingsPanel):
    title = _("RadioCenter")
    radio: RadioClient = None

    def makeSettings(self, settingsSizer):
        settings_sizer_helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        browse_text = _("Browse...")
        dir_dialog_title = _("Select a directory")

        sort_types = [item.value for item in SortType]
        self.sort_type = settings_sizer_helper.addLabeledControl(_("Sort by:"), wx.Choice, choices=sort_types)
        self.sort_type.SetStringSelection(self.radio.config.sort_type.value)

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

        group_sizer = wx.StaticBoxSizer(
            wx.VERTICAL, self,
            label=_("Path to File System collection base folder"),
        )
        group_box = group_sizer.GetStaticBox()
        group_helper = settings_sizer_helper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=group_sizer))

        directory_path_helper = gui.guiHelper.PathSelectionHelper(group_box, browse_text, dir_dialog_title)
        directory_entry_control = group_helper.addItem(directory_path_helper)

        self.fs_collection_path = directory_entry_control.pathControl
        self.fs_collection_path.Value = self.radio.config.fs_collection_path

        self.need_show_station_link = settings_sizer_helper.addItem(wx.CheckBox(self, label=_("Show radio station link")))
        self.need_show_station_link.SetValue(self.radio.config.need_show_station_link)

        verify_part_count_limit_label = _("Count of stations in a part for automatic checking")
        self.verify_part_count_limit = settings_sizer_helper.addLabeledControl(
            verify_part_count_limit_label, wx.TextCtrl
        )
        self.verify_part_count_limit.SetValue(str(self.radio.config.verify_part_count_limit))

    def onSave(self):
        sort_by = self.sort_type.GetStringSelection()
        for sort_type in SortType:
            if sort_type.value == sort_by:
                self.radio.config.sort_type = sort_type
                break

        self.radio.config.record_path = self.record_path.GetValue()
        self.radio.config.fs_collection_path = self.fs_collection_path.GetValue()

        self.radio.config.need_show_station_link = self.need_show_station_link.IsChecked()

        try:
            self.radio.config.verify_part_count_limit = int(self.verify_part_count_limit.GetValue())
        except ValueError as error:
            log.error(error, exc_info=True)

        self.radio.save()
