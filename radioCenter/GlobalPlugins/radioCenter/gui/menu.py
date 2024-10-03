import addonHandler
import gui

import wx

from .base import LabelsGUI

from ..client import RadioClient


addonHandler.initTranslation()


class BaseMenu(LabelsGUI):

    def __init__(self, client: RadioClient):
        super().__init__(client)

        self.menu = wx.Menu()

    def build_ui(self):
        self.play_item = self.menu.Append(wx.ID_ANY, self.play_label)
        self.stop_item = self.menu.Append(wx.ID_ANY, _("Stop"))
        self.mute_item = self.menu.Append(wx.ID_ANY, self.mute_label)
        self.record_item = self.menu.Append(wx.ID_ANY, self.record_label)

        if not self.radio.is_stations_available:
            self.play_item.Enable(False)
            self.stop_item.Enable(False)
            self.record_item.Enable(False)

        elif not self.radio.is_playing:
            self.stop_item.Enable(False)
            self.record_item.Enable(False)

        if not self.radio.is_recording_allowed:
            self.record_item.Enable(False)

    def play(self, event):
        self.radio.play()
        self.play_item.SetItemLabel(self.play_label)

        self.stop_item.Enable(True)
        if self.radio.is_recording_allowed:
            self.record_item.Enable(True)

    def stop(self, event):
        self.radio.release()
        self.play_item.SetItemLabel(self.play_label)
        self.stop_item.Enable(False)
        if not self.radio.is_recording:
            self.record_item.Enable(False)

    def mute(self, event):
        self.radio.mute()
        self.mute_item.SetItemLabel(self.mute_label)

    def record(self, event):
        self.radio.record()
        self.record_item.SetItemLabel(self.record_label)


class ToolsMenu(BaseMenu):

    def __init__(self, client: RadioClient):
        super().__init__(client)

        self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu

        self.build_ui()
        self._bindEvents()

    def build_ui(self):
        super().build_ui()

        self.menu.AppendSeparator()
        self.station_up_item = self.menu.Append(wx.ID_ANY, _("station next"))
        self.station_down_item = self.menu.Append(wx.ID_ANY, _("station previous"))

        self.menu.AppendSeparator()
        self.volume_up_item = self.menu.Append(wx.ID_ANY, _("volume up"))
        self.volume_down_item = self.menu.Append(wx.ID_ANY, _("volume down"))

        if not self.radio.is_stations_available:
            self.station_up_item.Enable(False)
            self.station_down_item.Enable(False)

        self.radio_menu = self.tools_menu.AppendSubMenu(self.menu, _("RadioCenter"))

    def _bindEvents(self):
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.play, self.play_item)
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.stop, self.stop_item)
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.mute, self.mute_item)
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.record, self.record_item)

        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.station_up, self.station_up_item)
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.station_down, self.station_down_item)

        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.volume_up, self.volume_up_item)
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.volume_down, self.volume_down_item)

    def terminate(self):
        try:
            self.tools_menu.Remove(self.radio_menu)
        except Exception:
            pass

    def station_up(self, event):
        self.radio.station_up()

    def station_down(self, event):
        self.radio.station_down()

    def volume_up(self, event):
        self.radio.volume_up()

    def volume_down(self, event):
        self.radio.volume_down()


class ContextMenu(BaseMenu):

    def __init__(self, client: RadioClient, index: int):
        super().__init__(client)

        self.radio_index = index

        self.build_ui()
        self._bindEvents()

    def _bindEvents(self):
        self.menu.Bind(wx.EVT_MENU, self.play, self.play_item)
        self.menu.Bind(wx.EVT_MENU, self.stop, self.stop_item)
        self.menu.Bind(wx.EVT_MENU, self.mute, self.mute_item)
        self.menu.Bind(wx.EVT_MENU, self.record, self.record_item)

    def play(self, event):
        self.radio.stations_control.change_station(self.radio_index)
        super().play(event)

    def record(self, event):
        self.radio.stations_control.change_station(self.radio_index)
        super().record(event)
