import wx
import sys
import psycopg2
import re


class QueryResults(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        # Declareer variabelen, creeren boxen, toon selecties, plaats boxen
	cursor, conn = self.connect()
	self.query(cursor, conn)
	self.kopje_maken()
	self.resBox()
	self.declaratie()
	self.resultaten_box()
	self.knoppen_box()
        final = self.mainBox()
        self.SetSizer(final)
	self.Layout()
	self.Refresh()
	
    def connect(self):
        conn_string = "host='localhost' dbname='postgres' user='monika'" \
                  " password='elzelek'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
	return cursor, conn
	
    def query(self, cursor, conn):
	cursor.execute(" SELECT * FROM pathway" ) #DIT MOET GEAUTOMATISEERD WORDEN
	self.rows = cursor.fetchall()
	self.field_names = [i[0] for i in cursor.description]

    def declaratie(self):
	self.kopje_text = wx.StaticText(self, 1, self.kopje_word)
	fontje =wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
	fontje2 =wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
	self.kopje_text.SetFont(fontje)
	self.leeg_text = wx.StaticText(self, 1, " ")
	self.beschrijving = wx.StaticText(self, 1, "RESULTATEN", style=wx.CENTRE)
	self.beschrijving.SetFont(fontje2)
	self.exit_knop = wx.Button(self, -1, "Exit")
        self.new_query_kiezen_knop = wx.Button(self, -1, "Kiez een nieuwe query")
	self.new_query_maken_knop = wx.Button(self, -1, "Maak een nieuwe query")
        self.save_knop = wx.Button(self, -1, "Save to file")
    

    def mainBox(self):
	box = wx.BoxSizer(wx.VERTICAL)
	box.Add(self.resultaten_box, 10, wx.EXPAND)
	box.Add(self.knoppen_box, 1, wx.EXPAND)
	return box
    
    def knoppen_box(self):
	self.knoppen_box = wx.BoxSizer(wx.HORIZONTAL)
	self.knoppen_box.Add(self.new_query_kiezen_knop, 1, wx.EXPAND)
	self.knoppen_box.Add(self.new_query_maken_knop, 1, wx.EXPAND)
	self.knoppen_box.Add(self.save_knop, 1, wx.EXPAND)
	self.knoppen_box.Add(self.exit_knop, 1, wx.EXPAND)

    def resultaten_box(self):
	self.resultaten_box = wx.BoxSizer(wx.VERTICAL)
	self.resultaten_box.Add(self.leeg_text,0, wx.ALL|wx.EXPAND)
	self.resultaten_box.Add(self.beschrijving,1, wx.ALL|wx.EXPAND)
	self.resultaten_box.Add(self.kopje_text, 1, wx.ALL|wx.EXPAND)
	self.resultaten_box.Add(self.res_box, 10, wx.ALL|wx.EXPAND)

    def resBox(self):
	self.res_box = wx.BoxSizer(wx.VERTICAL)
	for rij in self.rows:
		self.results_word = ''
		for word in rij:
		    if len(word) > 200:
			new_word = re.sub("(.{200})", "\\1\n", word, 0, re.DOTALL)
		    	self.results_word += new_word
		    elif len(word) < 42:
			new_word = word + ((42 - len(word)) * " ")
			self.results_word += new_word 
		self.results_text = wx.StaticText(self,0,self.results_word)
		font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
		self.results_text.SetFont(font)
		self.res_box.Add(self.results_text, 0, wx.ALL|wx.EXPAND)
		
    def kopje_maken(self):
	for word in self.field_names:
    		if len(word) > 200:
			place = self.field_names.index(word)
			wordje = re.sub("(.{200})", "\\1\n", word, 0, re.DOTALL)
			self.field_names[place] = wordje
		elif len(word) < 30:
			place = self.field_names.index(word)
			new_word = word + ((30 - len(word)) * " ")
			self.field_names[place] = new_word
	self.kopje_word = ''
	for word in self.field_names:
		self.kopje_word += word



if __name__ == "__main__":
    class Schermpje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(800,1000))
            self.paneeltje = QueryResults(self, -1)
            self.Show(True)
    app = wx.App()
    Schermpje(None, -1, "Query Maker WizardOfCogs")
    app.MainLoop()
