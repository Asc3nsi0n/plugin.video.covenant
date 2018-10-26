# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Provider: Asc3nsi0n
# Addon id: plugin.video.Asc3nsi0n
# Addon Provider: Asc3nsi0n

import re,sys,json,time,xbmc
import hashlib,urllib,os,base64,codecs,xmlrpclib
import gzip, StringIO

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

from resources.lib.modules import control

def UniScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
	try:
		control.busy()
		from resources.lib.modules2 import sources
		sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	except:
		control.idle()
		#pass

def IntScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
	try:
		control.busy()
		from resources.lib.modules import sources
		sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	except:
		control.idle()
		#pass

def LambScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
	try:
		control.busy()
		from resources.lib.modules import sourceslambda
		sourceslambda.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	except:
		control.idle()
		#pass

def ScrDialog0(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
	scraper = control.yesnoDialog(control.lang(33718).encode('utf-8'), ' ', control.lang(33719).encode('utf-8'), control.addonInfo('name'), '[B]Universal[/B]', '[B]Internal[/B]')
	if scraper:
		select = control.setting('hosts.mode')
		UniScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	if not scraper:
		IntScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	else:
		#pass
		control.execute('Dialog.Close(yesnoDialog)')

def ScrDialog1(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
	list = [control.lang(33718).encode('utf-8'), control.lang(33714), control.lang(33748), control.lang(33713).encode('utf-8')]
	choice = control.selectDialog(list, control.addonInfo('name'))
	#if choice == -1: control.execute('Dialog.Close(All)')
	if choice == 0: control.execute('Dialog.Close(All)')
	if choice == 1:
		select = control.setting('hosts.mode')
		IntScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	if choice == 2:
		select = control.setting('hosts.mode')
		LambScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	if choice == 3:
		select = control.setting('hosts.mode')
		UniScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	else: control.execute('Dialog.Close(All)')

def ScrDialog2(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
	try: import pyxbmct.addonwindow as pyxbmct
	except: pass
	class SelectScraper(pyxbmct.AddonDialogWindow):
		def __init__(self, title='Ascension'):
			super(SelectScraper, self).__init__(title)###
			self.setGeometry(670, 284, 16, 32, 0, 5, 5)

			self.textbox = pyxbmct.TextBox()###
			## Place The Text             (Y, X, W, H)
			self.placeControl(self.textbox, 1, 11, 9, 20)
			self.textbox.setText(control.lang(33718).encode('utf-8'))
			#self.textbox.autoScroll(1000, 2000, 1000)

			self.textbox2 = pyxbmct.TextBox()###
			## Place The Text               (Y, X, W, H)
			self.placeControl(self.textbox2, 5, 12, 10, 20)
			self.textbox2.setText(control.lang(33720).encode('utf-8'))
			#self.textbox2.autoScroll(1000, 2000, 1000)

			#self.textbox3 = pyxbmct.TextBox()###
			#self.placeControl(self.textbox3, 4, 11, 10, 20)
			#self.textbox3.setText(control.lang(33720).encode('utf-8'))
			##self.textbox3.autoScroll(1000, 2000, 1000)

			self.button = pyxbmct.Button(control.lang(33714).encode('utf-8'))
			## Place Button               (Y, X, W, H)
			self.placeControl(self.button, 9, 12, 3, 9)
			self.connect(self.button, lambda: self.Int())

			self.button2 = pyxbmct.Button(control.lang(33739).encode('utf-8'))
			## Place Button                 (Y, X, W, H)
			self.placeControl(self.button2, 12, 12, 3, 9)
			self.connect(self.button2, lambda: self.AutoInt())

			self.button3 = pyxbmct.Button(control.lang(33713).encode('utf-8'))
			## Place Button                (Y, X, W, H)
			self.placeControl(self.button3, 9, 2, 3, 9)
			self.connect(self.button3, lambda: self.Uni())

			self.button4 = pyxbmct.Button(control.lang(33740).encode('utf-8'))
			## Place Button                 (Y, X, W, H)
			self.placeControl(self.button4, 12, 2, 3, 9)
			self.connect(self.button4, lambda: self.AutoUni())

			self.button5 = pyxbmct.Button(control.lang(33748).encode('utf-8'))
			## Place Button               (Y, X, W, H)
			self.placeControl(self.button5, 9, 22, 3, 9)
			self.connect(self.button5, lambda: self.Lamb())

			self.button6 = pyxbmct.Button(control.lang(33750).encode('utf-8'))
			## Place Button                 (Y, X, W, H)
			self.placeControl(self.button6, 12, 22, 3, 9)
			self.connect(self.button6, lambda: self.AutoLamb())			

			self.button.controlUp(self.button2)#Int
			self.button.controlDown(self.button2)
			self.button.controlLeft(self.button3)
			self.button.controlRight(self.button5)

			self.button2.controlUp(self.button)#AutoInt
			self.button2.controlDown(self.button)
			self.button2.controlLeft(self.button4)
			self.button2.controlRight(self.button6)

			self.button3.controlUp(self.button4)#Uni
			self.button3.controlDown(self.button4)
			self.button3.controlLeft(self.button5)
			self.button3.controlRight(self.button)

			self.button4.controlUp(self.button3)#AutoUni
			self.button4.controlDown(self.button3)
			self.button4.controlLeft(self.button6)
			self.button4.controlRight(self.button2)

			self.button5.controlUp(self.button6)#Lamb
			self.button5.controlDown(self.button6)
			self.button5.controlLeft(self.button)
			self.button5.controlRight(self.button3)

			self.button6.controlUp(self.button5)#AutoLamb
			self.button6.controlDown(self.button5)
			self.button6.controlLeft(self.button2)
			self.button6.controlRight(self.button4)

			self.setFocus(self.button)
			self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

		def Int(self):
			self.close()
			IntScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		def AutoInt(self):
			self.close()
			#control.infoDialog('It might NOT work properly!', 'Autoplay is still in testing...', control.addonIcon())
			select = '2'
			IntScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		def Uni(self):
			self.close()
			select = control.setting('hosts.mode')
			UniScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		def AutoUni(self):
			self.close()
			#control.infoDialog('It might NOT work properly!', 'Autoplay is still in testing...', control.addonIcon())
			select = '2'
			UniScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		def Lamb(self):
			self.close()
			LambScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		def AutoLamb(self):
			self.close()
			#control.infoDialog('It might NOT work properly!', 'Autoplay is still in testing...', control.addonIcon())
			select = '2'
			LambScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		def Apex(self):
		#PlayMedia(&quot;plugin://plugin.video.Apex/tv/play/281714/4/5/default&quot;)
			self.close()
			import apex
			from apex import sources
			sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

	window = SelectScraper(control.addonInfo('name'))
	window.doModal()
	del window