import wx


class QueryKiezen(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
      	self.declareren()
	box = self.boxen_maken()
        self.SetSizer(box)

    def declareren(self):
	self.bevestig_query_knop = wx.Button(self, -1, "Gebruik deze query")
	self.kiez_query_knop = wx.Button(self, -1, "Kies kant en klare query")
	self.exit_knop = wx.Button(self, -1, "Sluiten")
	self.tabellenknop = wx.Button(self, -1, "Weergeef alle tabellen")
	self.textje = wx.StaticText(self, -1, "Combenneer uw query. Gebruik a.u.b alle velden met sterretje.")

    def boxen_maken(self):
	werking_box = wx.BoxSizer(wx.VERTICAL)
	knoppen_box = wx.BoxSizer(wx.VERTICAL)
	totaal_box = wx.BoxSizer()
	werking_box.Add(self.textje, 1, wx.EXPAND)
	werking_box.Add(self.tabellenknop, 1, wx.EXPAND)
	knoppen_box.Add(self.bevestig_query_knop, 1, wx.EXPAND)
	knoppen_box.Add(self.kiez_query_knop, 1, wx.EXPAND)
	knoppen_box.Add(self.exit_knop, 1, wx.EXPAND)
	totaal_box.Add(werking_box, 2, wx.EXPAND)
	totaal_box.Add(knoppen_box, 1, wx.EXPAND)
	return totaal_box
	


if __name__ == "__main__":
    class Schermpje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(800, 500))
            self.paneeltje = QueryKiezen(self, -1)
            self.Show(True)
    app = wx.App()
    Schermpje(None, -1, "Simpel CheckBox")
    app.MainLoop()
