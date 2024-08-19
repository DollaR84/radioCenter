from dataclasses import dataclass
from typing import List

import addonHandler
import gui

import wx

from ..collections.types import StationStatusType


addonHandler.initTranslation()


@dataclass(init=False)
class Filters:
    __slots__ = ("status", "_name", "_info",)

    status: StationStatusType

    _name: str
    _info: str

    def __init__(
            self,
            status: StationStatusType = StationStatusType.All,
            name: str = "",
            info: str = "",
    ):
        self.status = status
        self._name = name
        self._info = info

    @property
    def name(self) -> str:
        return self._name.lower()

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def info(self) -> str:
        return self._info.lower()

    @info.setter
    def info(self, value: str):
        self._info = value


class FiltersGUI(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, _("Filters"))

        self.filters: Filters = Filters()

        self.build_ui()
        self._bindEvents()

    def build_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        filters_helper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

        self.filter_status_type = filters_helper.addLabeledControl(
            _("Filter by status type:"), wx.Choice,
            choices=StationStatusType.get_list_values(),
        )
        self.filter_status_type.SetStringSelection(StationStatusType.All.value)

        self.filter_name = filters_helper.addLabeledControl(_("Filter by name:"), wx.TextCtrl)
        self.filter_info = filters_helper.addLabeledControl(_("Filter by info:"), wx.TextCtrl)

        buttons_sizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)

        ok_button = wx.Button(self, wx.ID_OK, label=_("Apply"))
        cancel_button = wx.Button(self, wx.ID_CANCEL, label=_("Cancel"))

        buttons_sizer.Add(ok_button, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        buttons_sizer.Add(cancel_button, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(filters_helper.sizer, border=2, flag=wx.EXPAND | wx.ALL)
        sizer.Add(buttons_sizer, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)
        self.Fit()

    def _bindEvents(self):
        self.Bind(wx.EVT_CHOICE, self.filter_status_type_handler, self.filter_status_type)
        self.Bind(wx.EVT_TEXT, self.filter_name_handler, self.filter_name)
        self.Bind(wx.EVT_TEXT, self.filter_info_handler, self.filter_info)

    def filter_status_type_handler(self, event):
        self.filters.status = StationStatusType.get_type_by_value(self.filter_status_type.GetStringSelection())

    def filter_name_handler(self, event):
        self.filters.name = self.filter_name.GetValue()

    def filter_info_handler(self, event):
        self.filters.info = self.filter_info.GetValue()

    def get_values(self):
        return self.filters
