import sys
from typing import List, Union

import addonHandler
import gui
from logHandler import log
import ui

import wx

if sys.version_info >= (3, 10):
    from .collections import RadioCollectionsGUI
else:
    class RadioCollectionsGUI:

        @staticmethod
        def create_collections_gui(parent):
            pass

from ..client import RadioClient

from ..stations import Station

from ..types import SortType, PriorityType

from ..utils import RadioTestData, RadioTester
from ..utils.player import Player, SoundType

from ..utils.parsers import PLSParser
from ..utils.parsers.data import ItemData


addonHandler.initTranslation()


class RadioGUI(wx.Dialog):

    _instance = None

    @staticmethod
    def create_radio_gui(client: RadioClient):
        if RadioGUI._instance:
            return

        gui.mainFrame.prePopup()
        window = RadioGUI(gui.mainFrame, client)
        client.gui = window

        window.Show()
        gui.mainFrame.postPopup()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            return super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, parent, client: RadioClient):
        if self._instance is not None:
            return self._instance

        self.radio: RadioClient = client
        RadioGUI._instance = self

        dialog_title = _("Radio Center Control")
        super().__init__(parent, title=dialog_title)

        self.build_ui()
        self._bindEvents()

    @property
    def stations_names(self) -> List[str]:
        return [
            station.name_url
            for station in self.radio.stations
        ]

    def build_ui(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

        left_helper.addItem(wx.StaticText(self, wx.ID_ANY, label=_("List stations:")))
        self.stations = left_helper.addItem(wx.ListBox(
            self, wx.ID_ANY, choices=self.stations_names,
            style=wx.LB_HSCROLL | wx.LB_NEEDED_SB | wx.LB_SINGLE,
        ))
        left_sizer.Add(left_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)

        sort_types = [item.value for item in SortType]
        self.sort_type = left_helper.addLabeledControl(_("Sort by:"), wx.Choice, choices=sort_types)
        self.sort_type.SetStringSelection(self.radio.config.sort_type.value)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

        self.play_button = right_helper.addItem(wx.Button(self, label=self.play_label))
        self.stop_button = right_helper.addItem(wx.Button(self, label=_("Stop")))
        self.mute_button = right_helper.addItem(wx.Button(self, label=self.mute_label))
        self.record_button = right_helper.addItem(wx.Button(self, label=self.record_label))
        self.collections_button = right_helper.addItem(wx.Button(self, wx.ID_ANY, label=_("Collections")))
        self.close_button = right_helper.addItem(wx.Button(self, wx.ID_ANY, label=_("Close")))
        right_sizer.Add(right_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)

        station_text_sizer = wx.BoxSizer(wx.VERTICAL)
        station_text_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
        self.station_name = station_text_helper.addLabeledControl(_("station name:"), wx.TextCtrl)
        self.station_url = station_text_helper.addLabeledControl(_("station url:"), wx.TextCtrl)

        station_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
        station_ctrl_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)

        priorities = [item.value for item in PriorityType]
        self.priority_type = station_ctrl_helper.addLabeledControl(_("Priority:"), wx.Choice, choices=priorities)
        self.priority_type.SetStringSelection(PriorityType.Middle.value)

        self.add_station_button = station_ctrl_helper.addItem(wx.Button(self, label=_("Add")))
        self.change_station_button = station_ctrl_helper.addItem(wx.Button(self, label=_("Change")))
        self.remove_station_button = station_ctrl_helper.addItem(wx.Button(self, label=_("Remove")))

        station_text_sizer.Add(station_text_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        station_ctrl_sizer.Add(station_ctrl_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        right_sizer.Add(station_text_sizer, border=2, flag=wx.EXPAND | wx.ALL)
        right_sizer.Add(station_ctrl_sizer, border=2, flag=wx.EXPAND | wx.ALL)

        self.add_station_button.Disable()
        self.change_station_button.Disable()
        self.remove_station_button.Disable()

        if not self.radio.is_stations_available:
            self.play_button.Disable()
            self.stop_button.Disable()
            self.record_button.Disable()

        elif not self.radio.is_playing:
            self.stop_button.Disable()
            self.record_button.Disable()

        if not self.radio.is_recording_allowed:
            self.record_button.Disable()

        if sys.version_info < (3, 10):
            self.collections_button.Disable()

        self.close_button.SetDefault()

        main_sizer.Add(left_sizer, border=5, flag=wx.EXPAND | wx.ALL)
        main_sizer.Add(right_sizer, border=5, flag=wx.EXPAND | wx.ALL)
        main_sizer.Fit(self)
        self.SetSizer(main_sizer)
        self.CentreOnScreen()

    def _bindEvents(self):
        self.Bind(wx.EVT_CLOSE, self.close_window)
        self.Bind(wx.EVT_CHAR_HOOK, self.process_char_hooks)

        self.Bind(wx.EVT_LISTBOX, self.selection_station, self.stations)
        self.stations.Bind(wx.EVT_KEY_UP, self.process_hot_keys)

        self.Bind(wx.EVT_CHOICE, self.selection_sort_type, self.sort_type)
        self.Bind(wx.EVT_CHOICE, self.selection_priority_type, self.priority_type)
        self.Bind(wx.EVT_TEXT, self.changed_text_station, self.station_name)
        self.Bind(wx.EVT_TEXT, self.changed_text_station, self.station_url)

        self.Bind(wx.EVT_BUTTON, self.play, self.play_button)
        self.Bind(wx.EVT_BUTTON, self.stop, self.stop_button)
        self.Bind(wx.EVT_BUTTON, self.mute, self.mute_button)
        self.Bind(wx.EVT_BUTTON, self.record, self.record_button)
        self.Bind(wx.EVT_BUTTON, self.collections, self.collections_button)
        self.Bind(wx.EVT_BUTTON, self.close, self.close_button)

        self.Bind(wx.EVT_BUTTON, self.add_station, self.add_station_button)
        self.Bind(wx.EVT_BUTTON, self.change_station, self.change_station_button)
        self.Bind(wx.EVT_BUTTON, self.remove_station, self.remove_station_button)

    def process_char_hooks(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Close(True)

        elif event.GetId() == self.stations.GetId() and chr(keycode) == 'C' and event.ControlDown():
            index = self.stations.GetSelection()
            station = self.radio.stations[index]
            self.copy_to_clipboard(station.url)

        event.Skip()

    def process_hot_keys(self, event):
        sort_type_status = self.radio.config.sort_type == SortType.Manual
        if event.GetId() == self.stations.GetId() and event.AltDown() and sort_type_status:
            index = self.stations.GetSelection()
            keycode = event.GetKeyCode()
            new_position = self.radio.stations_control.manual_sort(index, keycode)
            if new_position is not None:
                self.radio.save()
                self.stations.Set(self.stations_names)
                self.stations.SetSelection(new_position)
                Player.play(SoundType.Action)
            else:
                Player.play(SoundType.Failure)
        event.Skip()

    def selection_station(self, event):
        index = self.stations.GetSelection()
        self.radio.stations_control.change_station(index)
        self.play_button.Enable()
        self.change_station_button.Enable()
        self.remove_station_button.Enable()
        self.play_button.SetLabel(self.play_label)
        if self.radio.is_playing and self.radio.is_recording_allowed:
            self.record_button.Enable()
        self.priority_type.SetStringSelection(self.radio.stations_control.selected.priority.value)
        self.Layout()

    def selection_sort_type(self, event):
        index = self.sort_type.GetSelection()
        for i, sort_type in enumerate(SortType):
            if index == i:
                self.radio.config.sort_type = sort_type
                self.radio.save()
                break

        self.radio.stations_control.sort(self.radio.config.sort_type)
        self.stations.Set(self.stations_names)

    def selection_priority_type(self, event):
        self.change_station_button.Enable()

    def changed_text_station(self, event):
        if event.GetId() == self.station_url.GetId():
            self.add_station_button.Enable()
        if self.stations.GetSelection():
            self.change_station_button.Enable()

    def add_station(self, event):
        name = self.get_station_name()
        url = self.station_url.GetValue()

        index = self.priority_type.GetSelection()
        for i, priority in enumerate(PriorityType):
            if index == i:
                break
        else:
            priority = PriorityType.Middle

        if url.endswith(".pls"):
            parser = PLSParser(url)
            items = parser.get_data()
        else:
            items = [ItemData(name=name, url=url)]

        for item in items:
            data = RadioTestData(
                callback_after=self.add_station_after, url=item.url,
                name=item.name, priority=priority,
            )
            RadioTester(data, self.radio.config.repeat_count)

    def change_station(self, event):
        index = self.stations.GetSelection()
        station = self.radio.stations[index]

        name = self.station_name.GetValue()
        url = self.station_url.GetValue()
        priority_index = self.priority_type.GetSelection()
        for i, priority in enumerate(PriorityType):
            if priority_index == i:
                break
        else:
            priority = None

        if name and name != station.name and not url:
            station.name = name
        if url and url != station.url:
            data = RadioTestData(
                callback_after=self.change_station_after, url=url,
                name=name, station_index=index,
            )
            RadioTester(data, self.radio.config.repeat_count)
        if priority and priority != station.priority:
            station.priority = priority

        if not url:
            self.radio.save()
            self.stations.SetString(index, station.name_url)
            self.radio.stations_control.sort(self.radio.config.sort_type)
            self.stations.Set(self.stations_names)

        self.station_name.SetValue('')
        self.station_url.SetValue('')
        self.change_station_button.Disable()
        self.Layout()

    def remove_station(self, event):
        index = self.stations.GetSelection()
        self.stations.Delete(index)
        new_index = self.radio.remove_station(index)

        if len(self.radio.config.stations) == 0:
            self.play_button.Disable()
        else:
            self.stations.SetSelection(new_index)
        self.remove_station_button.Disable()
        self.Layout()

    def play(self, event):
        self.radio.play()
        self.play_button.SetLabel(self.play_label)

        self.stop_button.Enable()
        if self.radio.is_recording_allowed:
            self.record_button.Enable()

    def stop(self, event):
        self.radio.release()
        self.play_button.SetLabel(self.play_label)
        self.stop_button.Disable()
        if not self.radio.is_recording:
            self.record_button.Disable()

    def mute(self, event):
        self.radio.mute()
        self.mute_button.SetLabel(self.mute_label)

    def record(self, event):
        self.radio.record()
        self.record_button.SetLabel(self.record_label)

    def close(self, event):
        self.Close(True)

    def close_window(self, event):
        self.radio.save()
        self.radio.gui = None
        self.Destroy()
        self._instance = None

    def collections(self, event):
        RadioCollectionsGUI.create_collections_gui(self)

    @property
    def play_label(self) -> str:
        return _("Pause") if self.radio.need_paused else _("Play")

    @property
    def record_label(self) -> str:
        return _("Stop record") if self.radio.is_recording else _("Record")

    @property
    def mute_label(self) -> str:
        return _("Unmute") if self.radio.config.is_muted else _("Mute")

    def get_station_name(self) -> str:
        name = self.station_name.GetValue()
        if not name:
            name = " ".join([_("Station"), str(len(self.radio.config.stations) + 1)])
        return name

    def add_station_after(self, data: RadioTestData):
        if data.is_success:
            new_position = self.radio.add_station(data.name, data.url, data.priority)
            station = self.radio.stations_control.selected
            self.add_station_to_listbox(station, new_position)

        self.station_name.SetValue('')
        self.station_url.SetValue('')
        self.add_station_button.Disable()
        self.Layout()

    def add_station_to_listbox(self, station: Station, new_position: Union[int, None]):
        if new_position is not None:
            self.stations.Insert(station.name_url, new_position)
            self.stations.SetSelection(new_position)

    def change_station_after(self, data:RadioTestData):
        if data.is_success:
            station = self.radio.stations[data.station_index]
            if self.radio.stations_control.check_unique_url(data.url):
                station.url = data.url

            if data.name and data.name != station.name:
                station.name = data.name

            self.radio.save()
            self.stations.SetString(data.station_index, station.name_url)
            self.radio.stations_control.sort(self.radio.config.sort_type)
            self.stations.Set(self.stations_names)

    def copy_to_clipboard(self, text: str, need_speak_phrase: bool = True):
        data = wx.TextDataObject()
        data.SetText(text)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()

            if need_speak_phrase:
                ui.message(_("Link copied to clipboard"))

        else:
            log.error("error opening clipboard")
