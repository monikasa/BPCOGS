import wx


class QueryKiezen(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
      	self.declareren()
	box = self.boxen_maken()
        self.SetSizer(box)

    def declareren(self):
	self.bevestig_query_knop = wx.Button(self, -1, "Gebruik deze query")
	self.maak_query_knop = wx.Button(self, -1, "Maak zelf een query")
	self.exit_knop = wx.Button(self, -1, "Sluiten")
	self.querylist = ["query1", "query2", "query3", "query4", "query5"]
	self.queryknopjes = wx.RadioBox(self, -1, "Query Lijst", (-1, -1), (-1, -1), self.querylist, 1, wx.RA_SPECIFY_COLS)
	
    def boxen_maken(self):
	query_box = wx.BoxSizer(wx.VERTICAL)
	query_box.Add(self.queryknopjes, 1, wx.EXPAND)	
	knoppen_box = wx.BoxSizer(wx.VERTICAL)
	knoppen_box.Add(self.bevestig_query_knop, 1, wx.EXPAND)
	knoppen_box.Add(self.maak_query_knop, 1, wx.EXPAND)
	knoppen_box.Add(self.exit_knop, 1, wx.EXPAND)
	totaal_box = wx.BoxSizer()
	totaal_box.Add(query_box, 3, wx.EXPAND)
	totaal_box.Add(knoppen_box, 1, wx.EXPAND)
	return totaal_box
	
	

		



        
if __name__ == "__main__":
    class Schermpje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(800, 500))
            self.paneeltje = QueryKiezen(self, -1)
            self.Show(True)
    app = wx.App()
    Schermpje(None, -1, "Query Maker")
    app.MainLoop()
