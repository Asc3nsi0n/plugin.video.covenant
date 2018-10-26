import urllib, urllib2, urlparse, os
import xbmc, xbmcgui, xbmcaddon
import sys, subprocess, re, time, zipfile

import pyxbmct.addonwindow as pyxbmct

#############################################################
####################### Popup Image #########################

class PopupImage(xbmcgui.WindowDialog):
    #def __init__(self, image, line1, line2, line3, line4, line5):
    def __init__(self, imgfile):
        self.addControl(xbmcgui.ControlImage(x=0, y=0, width=1280, height=720, filename=imgfile))

def PopupImg(imgfile):
	#xbmc.executebuiltin("Dialog.Close(busydialog)")
    window = PopupImage(imgfile)
    window.show()
	#window.doModal()
    xbmc.sleep(5000)
    window.close()
    del window

def DebridExample():
    #window = PopupImage('http://STORAGE/plugin.video.Asc3nsi0n/nodebridss.jpg')
    window = PopupImage(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Asc3nsi0n', 'resources', 'media', 'nodebridss.jpg')))
    window.show()
    xbmc.sleep(6000)
    #window2 = PopupImage('http://STORAGE/plugin.video.Asc3nsi0n/debridss.jpg')
    window2 = PopupImage(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Asc3nsi0n', 'resources', 'media', 'debridss.jpg')))
    window2.show()
    xbmc.sleep(6000)	
    window.close()
    del window
	#PopupImg('http://STORAGE/plugin.video.Asc3nsi0n/debridss.jpg')
	#time.sleep(1)
	#PopupImg('http://STORAGE/plugin.video.Asc3nsi0n/nodebridss.jpg')

#############################################################
################### VIEW DIALOG MESSAGE #####################		
def request(url):
	file = urllib.urlopen(url)
	txt = file.read()
	return txt

def viewDialog(url, title):
    global msg_text

    if url.startswith('http'): msg_text = request(url)

    else:
        with open(url,mode='r')as f: msg_text = f.read()
    #TextWindow(msg_text)
    #window = TextBox('[B]Ascension[/B]')
    window = TextBox(title)
    window.doModal()
    del window

class TextBox(pyxbmct.AddonDialogWindow):
    def __init__(self, title='Ascension'):
        super(TextBox, self).__init__(title)
        self.setGeometry(950, 600, 10, 30, 0, 5, 5)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self):
        #Background   = pyxbmct.Image(xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Asc3nsi0n', 'fanart.jpg')))
		## Place The BackGround Image (X, Y, W, H)
        #self.placeControl(Background, -1, 0, 10, 30)
        self.textbox = pyxbmct.TextBox()
		## Place The Text             (X, Y, W, H)
        self.placeControl(self.textbox, 0, 1, 9, 28)
        self.textbox.setText(msg_text)
        self.textbox.autoScroll(1000, 2000, 1000)

    def set_active_controls(self):
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 9,26,1,4)
        self.connect(self.button, self.close)

    def set_navigation(self):
        self.button.controlUp(self.button)
        self.button.controlDown(self.button)
        self.button.controlRight(self.button)
        self.button.controlLeft(self.button)
        self.setFocus(self.button)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])

#informationFileURL   = 'http://STORAGE/plugin.video.Asc3nsi0n/information.txt'
#informationFileLocal = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Asc3nsi0n', 'resources', 'msg', 'information.txt'))
#viewDialog(informationFileURL)
#viewDialog(informationFile)
