import addonHandler
import gui
import ui

import wx

from .filter import Filters

from .vlc import VirtualListCtrl

from ..collections import RadioCollections, CollectionData, CollectionDataExt
from ..collections.types import StationStatusType

from ..config import Config

from ..player import Player

from ..saver import Saver

from ..tester import RadioTestData

from ..types import PriorityType, SoundType


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
        return (item.name, item.status.value, item.info, item.url,)

    def UpdateCache(self, start, end):
        pass


class TabCollection(wx.Panel):

    def __init__(self, notebook, parent, collection, data: CollectionDataExt | None = None):
        super().__init__(notebook, wx.ID_ANY)

        self.notebook = notebook
        self.parent = parent
        self.collection = collection

        self.collection_data_ext: CollectionDataExt | None = data
        self.collection_data: list[CollectionData] = data.stations if data else []
        self.is_collection_data_updating: bool = False
        self.is_collection_data_updated: bool = False

        self.build_ui()
        self._bindEvents()

        self.verify_part_count: int = 0
        if self.collection_data_ext:
            self.station_generator = self._station_generator()
            self.verify()

    def build_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        box_data = wx.StaticBox(self, wx.ID_ANY, _("List stations:"))
        self.data = VirtualListCtrl(box_data, DataSource(self))
        sizer.Add(self.data, 1, wx.EXPAND | wx.ALL, 5)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)
        self.test_button = buttons_helper.addItem(wx.Button(self, label=_("Test")))
        self.action_button = buttons_helper.addItem(wx.Button(self, label=self.action_label))
        self.add_button = buttons_helper.addItem(wx.Button(self, label=_("Add station")))
        buttons_sizer.Add(buttons_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        sizer.Add(buttons_sizer, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(sizer)

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
            self.play_button.Disable()
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
                Player.play(SoundType.Move)
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

    def update_finish(self, collection_name: str, data: list[CollectionData]):
        if self.collection.name != collection_name:
            return

        self.collection_data = data
        self.collection_data_ext = CollectionDataExt(stations=self.collection_data)

        self.is_collection_data_updating = False
        self.is_collection_data_updated = True
        self.parent.save_collections_data()

        ui.message(_("Collection data successfully updated"))
        self.show_items()

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
        wx.CallLater(1000, self.parent.parent.stop_button.Enable, self.parent.parent.radio.is_playing)

    def test_run(self, event):
        index = self.data.GetIndex()
        item = self.collection_data[index]

        self.parent.collections.verify(
            item, index,
            self.parent.config.repeat_count_collection,
            self.callback_after_verify,
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
        station = self.collection_data[data.station_index]
        station.status = StationStatusType.Works if data.is_success else StationStatusType.NotWork

        index = self.data.GetIndex()
        if index == data.station_index:
            self.action_button.SetLabel(self.action_label)
            ui.message(_("Station link verified"))

        self.collection_data_ext.verified()
        if self.parent and data.station_index == self.collection_data_ext.current_check_index:
            self.verify()

        if self.verify_part_count == self.parent.config.verify_part_count_limit:
            self.parent.save_collections_data()
            self.verify_part_count = 0

        if data.station_index == len(self.collection_data) - 1:
            self.parent.save_collections_data()

    def filtering(self, filters: Filters):
        if not self.collection_data_ext:
            return

        self.collection_data = self.collection_data_ext.stations
        if filters.status != StationStatusType.All:
            self.collection_data = [item for item in self.collection_data if item.status == filters.status]
        if filters.name:
            self.collection_data = [item for item in self.collection_data if filters.name in item.name]
        if filters.info:
            self.collection_data = [item for item in self.collection_data if filters.info in item.info]

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

        dialog_title = _("Radio Collections")
        super().__init__(parent, title=dialog_title)

        self.build_ui()
        self._bindEvents()

        self.filters: Filters = Filters()

    def build_ui(self):
        collections_data = self.saver.load_collections()

        sizer = wx.BoxSizer(wx.VERTICAL)
        filters_sizer = wx.BoxSizer(wx.HORIZONTAL)
        filters_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)

        self.filter_status_type = filters_helper.addLabeledControl(
            _("Filter by status type:"), wx.Choice,
            choices=StationStatusType.get_list_values(),
        )
        self.filter_status_type.SetStringSelection(StationStatusType.All.value)

        self.filter_name = filters_helper.addLabeledControl(_("Filter by name:"), wx.TextCtrl)
        self.filter_info = filters_helper.addLabeledControl(_("Filter by info:"), wx.TextCtrl)

        filters_sizer.Add(filters_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        sizer.Add(filters_sizer, 1, wx.EXPAND | wx.ALL, 3)

        self.notebook = wx.Notebook(self, wx.ID_ANY)
        for collection_name in self.collections.collections_names:
            tab = TabCollection(
                self.notebook, self,
                self.collections.get_collection(collection_name),
                data = collections_data.get(collection_name),
            )
            self.notebook.AddPage(tab, collection_name)
            self.tabs.append(tab)
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)
        self.update_button = buttons_helper.addItem(wx.Button(self, label=_("Update")))
        self.close_button = buttons_helper.addItem(wx.Button(self, wx.ID_ANY, label=_("Close")))

        buttons_sizer.Add(buttons_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        sizer.Add(buttons_sizer, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(sizer)

    def _bindEvents(self):
        self.Bind(wx.EVT_CLOSE, self.close_window)
        self.Bind(wx.EVT_CHAR_HOOK, self.process_char_hooks)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.notebook_page_changed, self.notebook)

        self.Bind(wx.EVT_CHOICE, self.filter_status_type_handler, self.filter_status_type)
        self.Bind(wx.EVT_TEXT, self.filter_name_handler, self.filter_name)
        self.Bind(wx.EVT_TEXT, self.filter_info_handler, self.filter_info)

        self.Bind(wx.EVT_BUTTON, self.update, self.update_button)
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

    def notebook_page_changed(self, event):
        page = self.get_select_page()
        self.filters.status = StationStatusType.get_type_by_value(self.filter_status_type.GetStringSelection())
        self.filters.name = self.filter_name.GetValue()
        self.filters.info = self.filter_info.GetValue()
        page.filtering(self.filters)

    def filter_status_type_handler(self, event):
        page = self.get_select_page()
        self.filters.status = StationStatusType.get_type_by_value(self.filter_status_type.GetStringSelection())
        page.filtering(self.filters)

    def filter_name_handler(self, event):
        page = self.get_select_page()
        self.filters.name = self.filter_name.GetValue()
        page.filtering(self.filters)

    def filter_info_handler(self, event):
        page = self.get_select_page()
        self.filters.info = self.filter_info.GetValue()
        page.filtering(self.filters)

    def update(self, event):
        if any([tab.is_collection_data_updating for tab in self.tabs]):
            ui.message(_("Collection data updating now"))
            return

        page = self.get_select_page()
        page.update()

    def save_collections_data(self):
        collections_data: dict[str, CollectionDataExt | None] = {}
        for tab in self.tabs:
            collections_data[tab.collection.name] = tab.collection_data_ext
        self.saver.save_collections(collections_data)

    def get_select_page(self):
        page = None
        index = self.notebook.GetSelection()
        page = self.tabs[index]
        return page

    def close(self, event):
        self.Close(True)

    def close_window(self, event):
        self.save_collections_data()
        self.Destroy()
        self._instance = None
