import wx


class VirtualListCtrl(wx.ListCtrl):

    def __init__(self, parent, dataSource):
        wx.ListCtrl.__init__(
            self, parent, wx.ID_ANY,
            style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL |wx.LC_VIRTUAL,
        )
        self.data = dataSource
        self.index = -1

        self.Bind(wx.EVT_LIST_CACHE_HINT, self.DoCacheItems)

        self.SetItemCount(self.data.GetCount())
        columns = self.data.GetColumnHeaders()
        for col, text in enumerate(columns):
            self.InsertColumn(col, text)

    def DoCacheItems(self, evt):
        self.data.UpdateCache(evt.GetCacheFrom(), evt.GetCacheTo())

    def OnGetItemText(self, item, col):
        row = self.data.GetItem(item)
        self.index = item
        return row[col]

    def GetIndex(self):
        return self.index

    def OnGetItemAttr(self, item):
        return None

    def OnGetItemImage(self, item):
        return -1
