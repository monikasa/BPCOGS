import wx
import sys
import textwrap

from QueryResults import QueryResults
from DBscherm import DBscherm


class Aanroep(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (800,400))
        self.results_scherm = QueryResults(self, id)
        self.db_scherm = DBscherm(self, id)
        self.knoppenBinden()
        totaalbox = self.BoxMaken()
        self.SetSizer(totaalbox)
        self.Show(True) 

    def BoxMaken(self):
        box = wx.BoxSizer()
        box.Add(self.results_scherm, 1, wx.EXPAND | wx.ALL, 1)
        box.Add(self.db_scherm, 1, wx.EXPAND | wx.ALL, 1)
        self.results_scherm.Hide()
        self.db_scherm.Show()
        return box
        

    def knoppenBinden(self):
        self.results_scherm.new_query_kiezen_knop.Bind(wx.EVT_BUTTON, self.gebruik_query)
        self.results_scherm.new_query_maken_knop.Bind(wx.EVT_BUTTON, self.nieuwe_query)
	self.results_scherm.save_knop.Bind(wx.EVT_BUTTON, self.bestand_maken)
	self.results_scherm.exit_knop.Bind(wx.EVT_BUTTON, self.sluiten)
	self.db_scherm.mqknop.Bind(wx.EVT_BUTTON, self.nieuwe_query)
	self.db_scherm.kqknop.Bind(wx.EVT_BUTTON, self.gebruik_query)

    def nieuwe_query(self, event):
	self.db_scherm.Hide()
	self.results_scherm.Show()
	self.Refresh()
        self.Layout()
	
    def gebruik_query(self, event):
	self.db_scherm.Hide()
	self.results_scherm.Show()
	self.Refresh()
        self.Layout()

    def bestand_maken(self, event):
	self.db_scherm.Hide()
	self.results_scherm.Show()
	self.Refresh()
        self.Layout()
        
    def sluiten(self, event):
	sys.exit()

if __name__ == "__main__": 
    app = wx.App()
    Aanroep(None, -1, "Oefenopdracht 2")
    app.MainLoop()
                
                
