import wx
import sys
import textwrap

from QueryResults import QueryResults
from DBscherm import DBscherm
from QueryKiezen import QueryKiezen
from QueryMaken import QueryMaken

class Aanroep(wx.Frame):
#ALLE FUNCTIE SPRINGEN ALLLEEN TUSSEN SCHERMEN NIKS WERKT NOG
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (800,400))
        self.results_scherm = QueryResults(self, id)
        self.db_scherm = DBscherm(self, id)
	self.query_kiezen = QueryKiezen(self, id)
	self.query_maken = QueryMaken(self, id)
        self.knoppenBinden()
        totaalbox = self.BoxMaken()
        self.SetSizer(totaalbox)
        self.Show(True) 

    def BoxMaken(self):
        box = wx.BoxSizer()
        box.Add(self.results_scherm, 1, wx.EXPAND | wx.ALL, 1)
        box.Add(self.db_scherm, 1, wx.EXPAND | wx.ALL, 1)
	box.Add(self.query_maken, 1, wx.EXPAND | wx.ALL, 1)
	box.Add(self.query_kiezen, 1, wx.EXPAND | wx.ALL, 1)
        self.results_scherm.Hide()
	self.query_maken.Hide()
	self.query_kiezen.Hide()
        self.db_scherm.Show()
        return box
        

    def knoppenBinden(self):
        self.results_scherm.new_query_kiezen_knop.Bind(wx.EVT_BUTTON, self.sluiten)
        self.results_scherm.new_query_maken_knop.Bind(wx.EVT_BUTTON, self.sluiten)
	self.results_scherm.save_knop.Bind(wx.EVT_BUTTON, self.bestand_maken)
	self.results_scherm.exit_knop.Bind(wx.EVT_BUTTON, self.sluiten)
	self.db_scherm.mqknop.Bind(wx.EVT_BUTTON, self.nieuwe_query)
	self.db_scherm.kqknop.Bind(wx.EVT_BUTTON, self.gebruik_query)
	self.query_kiezen.bevestig_query_knop.Bind(wx.EVT_BUTTON, self.gebruik_query)
	self.query_kiezen.maak_query_knop.Bind(wx.EVT_BUTTON, self.sluiten)
	self.query_kiezen.exit_knop.Bind(wx.EVT_BUTTON, self.sluiten)
	self.query_kiezen.queryknopjes.Bind(wx.EVT_RADIOBOX, self.bestand_maken)
	self.query_maken.exit_knop.Bind(wx.EVT_BUTTON, self.sluiten)
	self.query_maken.bevestig_query_knop.Bind(wx.EVT_BUTTON, self.gebruik_query)
	self.query_maken.kiez_query_knop.Bind(wx.EVT_BUTTON, self.sluiten)
	self.query_maken.tabellenknop.Bind(wx.EVT_BUTTON, self.bestand_maken)

    def query_kiezen(self, event):
	self.db_scherm.Hide()
	self.query_maken.Hide()
	self.query_kiezen.Show()
	self.results_scherm.Hide()
	self.Refresh()
        self.Layout()

    def nieuwe_query(self, event):
	self.db_scherm.Hide()
	self.query_maken.Hide()
	self.query_kiezen.Show()
	self.results_scherm.Hide()
	self.Refresh()
        self.Layout()
	
    def gebruik_query(self, event):
	self.db_scherm.Hide()
	self.query_maken.Hide()
	self.query_kiezen.Hide()
	self.results_scherm.Show()
	self.Refresh()
        self.Layout()

    def bestand_maken(self, event):#deze functie komt maar terug naar start scherm, voor nu gebruikt voor de knoppen zonder functies
	self.db_scherm.Hide()
	self.query_maken.Hide()
	self.query_kiezen.Hide()
	self.results_scherm.Show()
	self.Refresh()
        self.Layout()
        
    def sluiten(self, event):
	sys.exit()

if __name__ == "__main__": 
    app = wx.App()
    Aanroep(None, -1, "Oefenopdracht 2")
    app.MainLoop()
                
                
