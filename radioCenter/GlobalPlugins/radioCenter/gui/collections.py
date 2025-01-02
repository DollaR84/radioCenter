from typing import List, Optional, Union

import addonHandler
import gui
from gui.message import displayDialogAsModal
import ui

import wx

from .filter import Filters, FiltersGUI

from .vlc import VirtualListCtrl

from ..collections import RadioCollections, CollectionData, CollectionDataExt
from ..collections.types import StationStatusType

from ..config import Config

from ..database import CollectionsDB

from ..saver import Saver

from ..types import PriorityType

from ..utils import RadioTestData
from ..utils.player import Player, SoundType


addonHandler.initTranslation()


class DataSource:

    def __init__(self, parent):
        self.parent = parent

        self.columns = [_("Name"), _("Status"), _("Info"), _("Url")]

    def GetColumnHeaders(self):
        return self.columns

    def GetCount(self):
        return len(self.parent.collection_data)

    def GetItem(self, index):
        item = self.parent.collection_data[index]
        url = item.url if self.parent.parent.config.need_show_station_link else ""
        return (item.name, item.status.value, item.info, url,)

    def UpdateCache(self, start, end):
        pass


class TabCollection(wx.Panel):

    def __init__(self, notebook, parent, collection, db):
        super().__init__(notebook, wx.ID_ANY)

        self.notebook = notebook
        self.parent = parent
        self.collection = collection
        self.db = db

        data = self.db.load_data(self.collection.name)
        self.collection_data_ext: Optional[CollectionDataExt] = data
        self.collection_data: List[CollectionData] = data.stations if data else []

        self.is_collection_data_updating: bool = False
        self.is_collection_data_updated: bool = False

        self.build_ui()
        self._bindEvents()

        self.verify_part_count: int = 0
        if self.collection_data_ext:
            self.station_generator = self._station_generator()
            self.verify()

    def build_ui(self):
        image_list = wx.ImageList(1, 1)
        self.SetBackgroundColour(wx.Colour(220, 220, 220))
        sizer = wx.BoxSizer(wx.VERTICAL)

        box_data = wx.StaticBox(self, wx.ID_ANY, _("List stations:"))
        self.data = VirtualListCtrl(box_data, DataSource(self))
        self.data.AssignImageList(image_list, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.data, 1, wx.EXPAND | wx.ALL, 5)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)
        self.test_button = buttons_helper.addItem(wx.Button(self, label=_("Test")))
        self.action_button = buttons_helper.addItem(wx.Button(self, label=self.action_label))
        self.add_button = buttons_helper.addItem(wx.Button(self, label=_("Add station")))
        buttons_sizer.Add(buttons_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        sizer.Add(buttons_sizer, 1, wx.EXPAND | wx.ALL, 3)

        self.SetSizer(sizer)
        self.Layout()
        self.parent.Layout()
        self.Fit()
        self.parent.Fit()

        self.test_button.Disable()
        self.action_button.Disable()
        self.add_button.Disable()

    def _bindEvents(self):
        self.data.Bind(wx.EVT_KEY_UP, self.process_hot_keys)

        self.Bind(wx.EVT_BUTTON, self.test_run, self.test_button)
        self.Bind(wx.EVT_BUTTON, self.action, self.action_button)
        self.Bind(wx.EVT_BUTTON, self.add, self.add_button)

    def process_hot_keys(self, event):
        index = self.data.GetIndex()
        if not index or index == -1 or index >= len(self.collection_data):
            event.Skip()
            return

        if not self.collection_data:
            self.test_button.Disable()
            self.action_button.Disable()
            self.add_button.Disable()
            event.Skip()
            return

        item = self.collection_data[index]

        self.test_button.Enable()
        self.add_button.Enable()
        if item.status == StationStatusType.Works:
            self.action_button.Enable()
            self.action_button.SetLabel(self.action_label)
        else:
            self.action_button.Disable()

        if event.GetId() == self.data.GetId() and event.AltDown() and item.many_urls_status:
            keycode = event.GetKeyCode()
            is_changed = item.change_url(keycode)

            if is_changed:
                Player.play(SoundType.Action)
                self.parent.collections.verify(
                    item, index,
                    self.parent.config.repeat_count_collection,
                    self.callback_after_verify,
                )

        event.Skip()

    def update(self):
        if self.collection_data and self.is_collection_data_updated:
            ui.message(_("Collection data already updated"))
            return

        self.is_collection_data_updating = True
        self.parent.collections.update(self.collection, self.update_finish)

    def update_finish(self, collection_name: str, data: List[CollectionData]):
        if self.collection.name != collection_name:
            return

        self.collection_data = data
        self.collection_data_ext = CollectionDataExt(stations=self.collection_data)

        self.is_collection_data_updating = False
        self.is_collection_data_updated = True
        self.parent.save_collections_data()

        ui.message(_("Collection data successfully updated"))
        self.show_items()

        self.Fit()
        self.parent.Fit()

        self.station_generator = self._station_generator()
        self.verify()

    @property
    def action_label(self) -> str:
        index = self.data.GetIndex()
        if not index or index == -1:
            return ""

        item = self.collection_data[index]
        return _("Stop") if self.parent.parent.radio.is_playing else _("Play")

    def action(self, event):
        index = self.data.GetIndex()
        item = self.collection_data[index]

        if self.parent.parent.radio.is_playing:
            self.parent.parent.radio.release()
        else:
            self.parent.parent.radio.play(url=item.url)

        wx.CallLater(2000, self.action_button.SetLabel, self.action_label)
        wx.CallLater(2000, self.parent.parent.play_button.SetLabel, self.parent.parent.play_label)
        wx.CallLater(2000, self.parent.parent.stop_button.Enable, self.parent.parent.radio.is_playing)

    def test_run(self, event):
        index = self.data.GetIndex()
        item = self.collection_data[index]
        station_index = self.collection_data_ext.stations.index(item)

        self.parent.collections.verify(
            item, station_index,
            self.parent.config.repeat_count_collection,
            self.callback_after_verify,
            is_speech_mode=True,
        )

    def add(self, event):
        index = self.data.GetIndex()
        item = self.collection_data[index]

        new_position = self.parent.parent.radio.add_station(item.name, item.url, PriorityType.Middle)
        if new_position is not None:
            station = self.parent.parent.radio.stations[new_position]
            self.parent.parent.add_station_to_listbox(station, new_position)

        ui.message(_("The station has been added to the general list"))

    def show_items(self):
        self.data.DeleteAllItems()
        self.data.SetItemCount(len(self.collection_data))

        for i in range(self.data.GetColumnCount()):
            self.data.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

        self.data.Refresh()
        self.data.Update()

    def _station_generator(self):
        for station in self.collection_data_ext:
            yield station

    def verify(self):
        try:
            station = next(self.station_generator)
        except StopIteration:
            return

        self.parent.collections.verify(
            station, self.collection_data_ext.current_check_index,
            self.parent.config.repeat_count_collection,
            self.callback_after_verify,
        )
        self.verify_part_count += 1

    def callback_after_verify(self, data: RadioTestData):
        station = self.collection_data_ext.stations[data.station_index]
        station.status = StationStatusType.Works if data.is_success else StationStatusType.NotWork

        if self.collection_data and len(self.collection_data) > 0:
            index = self.data.GetIndex()
            item = self.collection_data[index]

        if self.parent and data.station_index == self.collection_data_ext.current_check_index:
            self.collection_data_ext.verified()
            if self.verify_part_count != self.parent.config.verify_part_count_limit:
                self.verify()

        if data.station_index == len(self.collection_data) - 1:
            self.parent.save_collections_data()

        if self.verify_part_count == self.parent.config.verify_part_count_limit:
            self.parent.save_collections_data()
            self.verify_part_count = 0
            self.verify()

    def filtering(self, filters: Filters):
        if not self.collection_data_ext:
            return

        self.collection_data = self.collection_data_ext.stations
        if filters.status != StationStatusType.All:
            self.collection_data = [item for item in self.collection_data if item.status == filters.status]

        if filters.name:
            self.collection_data = [item for item in self.collection_data if filters.name in item.name.lower()]

        if filters.info:
            self.collection_data = [item for item in self.collection_data if filters.info in item.info.lower()]

        self.show_items()


class RadioCollectionsGUI(wx.Dialog):

    _instance = None

    @staticmethod
    def create_collections_gui(parent):
        if RadioCollectionsGUI._instance:
            return

        window = RadioCollectionsGUI(parent)
        window.Show()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            return super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, parent):
        if self._instance is not None:
            return self._instance

        self.tabs = []
        self.config: Config = parent.radio.config
        self.saver: Saver = parent.radio.saver
        self.parent = parent

        self.collections: RadioCollections = RadioCollections()
        RadioCollectionsGUI._instance = self
        self.db = CollectionsDB(self.saver.collections_db_filename)

        dialog_title = _("Radio Collections")
        super().__init__(parent, title=dialog_title)

        self.build_ui()
        self._bindEvents()

    def build_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self, wx.ID_ANY)
        for collection_name in self.collections.collections_names:
            collection = self.collections.get_collection(collection_name, config=self.config)
            if not collection.is_available:
                continue

            tab = TabCollection(
                self.notebook, self,
                collection,
                self.db,
            )
            self.notebook.AddPage(tab, collection_name)
            tab.show_items()
            self.tabs.append(tab)
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)
        self.update_button = buttons_helper.addItem(wx.Button(self, label=_("Update")))
        self.filters_button = buttons_helper.addItem(wx.Button(self, label=_("Filters")))
        self.close_button = buttons_helper.addItem(wx.Button(self, wx.ID_ANY, label=_("Close")))

        buttons_sizer.Add(buttons_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        sizer.Add(buttons_sizer, 1, wx.EXPAND | wx.ALL, 3)

        self.SetSizer(sizer)
        self.Layout()
        self.Fit()

    def _bindEvents(self):
        self.Bind(wx.EVT_CLOSE, self.close_window)
        self.Bind(wx.EVT_CHAR_HOOK, self.process_char_hooks)

        self.Bind(wx.EVT_BUTTON, self.update, self.update_button)
        self.Bind(wx.EVT_BUTTON, self.filters, self.filters_button)
        self.Bind(wx.EVT_BUTTON, self.close, self.close_button)

    def process_char_hooks(self, event):
        keycode = event.GetKeyCode()
        page = self.get_select_page()

        if keycode == wx.WXK_ESCAPE:
            self.Close(True)

        elif (
            event.GetId() == page.data.GetId() and page.collection_data and
            chr(keycode) == 'C' and event.ControlDown()
        ):
            index = page.data.GetIndex()
            station = page.collection_data[index]
            self.parent.copy_to_clipboard(station.url)

        event.Skip()

    def filters(self, event):
        filters = self.get_filters()
        if filters:
            page = self.get_select_page()
            page.filtering(filters)

    def update(self, event):
        if any([tab.is_collection_data_updating for tab in self.tabs]):
            ui.message(_("Collection data updating now"))
            return

        page = self.get_select_page()
        page.update()

    def close(self, event):
        self.Close(True)

    def close_window(self, event):
        self.save_collections_data()
        self.Destroy()
        self._instance = None

    def get_select_page(self):
        page = None
        index = self.notebook.GetSelection()
        page = self.tabs[index]
        return page

    def get_filters(self) -> Filters:
        result = None

        filters_dialog = FiltersGUI(self)
        if displayDialogAsModal(filters_dialog) == wx.ID_OK:
            result = filters_dialog.get_values()
        filters_dialog.Destroy()

        return result
