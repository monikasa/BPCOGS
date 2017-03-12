import wx

class DBscherm(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        # Declareer variabelen, creeren boxen, toon selecties, plaats boxen
        self.declareren()
        #self.boxCreeren1()
        final = self.boxCreeren()
        self.SetSizer(final)

    def declareren(self):
        self.welkomtext = wx.StaticText(self, -1, "WELKOM BIJ DE QUERY MAKER")
        font = wx.Font(20, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
	fontje =wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.welkomtext.SetFont(font)
	self.infotext = wx.StaticText(self, -1, "Hiermee kunt u uw COG bekijken")
	self.keuzetext = wx.StaticText(self, 1, "Kiez een optie", style=wx.ALIGN_CENTER)
	self.mqknop = wx.Button(self, -1, "Maak een query")
        self.kqknop = wx.Button(self, -1, "Gebruik kant en klare query")
	
    
    def boxCreeren(self):
        box = wx.BoxSizer(wx.VERTICAL)
	knoppen_box = wx.BoxSizer()
	t_knoppen_box = wx.BoxSizer(wx.VERTICAL)
	v_box = wx.BoxSizer(wx.VERTICAL)
        v_box.Add(self.welkomtext, 1, wx.CENTRE)
	v_box.Add(self.infotext, 1, wx.CENTRE)
	knoppen_box.Add(self.mqknop, 1, wx.EXPAND)
        knoppen_box.Add(self.kqknop, 1, wx.EXPAND)
	t_knoppen_box.Add(self.keuzetext,1, wx.CENTRE)
	t_knoppen_box.Add(knoppen_box, 1, wx.EXPAND)
	box.Add(v_box, 1, wx.CENTRE)
	box.Add(t_knoppen_box, 1, wx.EXPAND)
        return box	


if __name__ == "__main__":
    class Schermpje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(800,300))
            self.paneeltje = DBscherm(self, -1)
            self.Show(True)
    app = wx.App()
    Schermpje(None, -1, "Query Maker WizardOfCogs")
    app.MainLoop()
