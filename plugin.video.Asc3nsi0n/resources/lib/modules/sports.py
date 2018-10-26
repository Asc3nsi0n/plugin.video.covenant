# -*- coding: utf-8 -*-
"""
    Asc3nsi0n Video Add-on
    Copyright (C) 2016

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#credit to demons_are_real for base code
from __future__ import print_function
import xbmc,xbmcplugin,xbmcaddon
import sys,os,urllib,json
import calendar,datetime,time
import ConfigParser
import socket
from datetime import datetime
from resources.lib.modules import control
from resources.lib.modules import sports_utils
from resources.lib.modules import game
from resources.lib.modules.game import Game,GameBuilder
from urlparse import parse_qsl
from PIL import Image

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
sanityChecked = False
iniFilePath = os.path.join(control.addonPath, 'resources', 'sports.ini')
config = ConfigParser.ConfigParser()
config.read(iniFilePath)

#artPath = control.artPath()
artPath = os.path.join(xbmcaddon.Addon('script.Asc3nsi0n.artwork').getAddonInfo('path'), 'resources', 'media')
thumb2 = control.addonThumb()
poster = control.addonPoster()
banner = control.addonBanner()
fanart = control.addonFanart()

NHLicon = os.path.join(artPath, 'sports', 'nhl.png')
MLBicon = os.path.join(artPath, 'sports', 'mlb.png')

#tway = os.path.join(artPath, 'sports', 'nhlteams','3way.jpg')
tway = os.path.join(artPath, 'sports',  'networks','3wayblur.jpg')
alt = os.path.join(artPath, 'sports',  'networks','alt.png')
att = os.path.join(artPath, 'sports',  'networks','att.png')
cbc = os.path.join(artPath, 'sports',  'networks','cbc.png')
fox = os.path.join(artPath, 'sports',  'networks','fox.png')
msg = os.path.join(artPath, 'sports',  'networks','msg.png')
nbcs = os.path.join(artPath, 'sports',  'networks','nbcs.png')
nesn = os.path.join(artPath, 'sports',  'networks','nesn.png')
nhl = os.path.join(artPath, 'sports',  'networks','nhl.png')
prime = os.path.join(artPath, 'sports',  'networks','prime.png')
rds = os.path.join(artPath, 'sports',  'networks','rds.png')
ref = os.path.join(artPath, 'sports',  'networks','ref.jpg')
sn = os.path.join(artPath, 'sports',  'networks','sn.png')
sun = os.path.join(artPath, 'sports',  'networks','sun.png')
tsn = os.path.join(artPath, 'sports',  'networks','tsn.png')
tvas = os.path.join(artPath, 'sports',  'networks','tvas.png')


def games(date,provider): 
  remaining = game.GameBuilder.nhlTvRemaining if provider == "NHL.tv" else game.GameBuilder.mlbTvRemaining
  return GameBuilder.fromDate(config,date,remaining,provider)

def listyears(provider,yesterday = False):
  icon = NHLicon if provider == "NHL.tv" else MLBicon
  items = []
  if yesterday == False:
	listItem = control.item(label = 'Yesterday - ' + sports_utils.yesterday().strftime("%B, %d - %Y"))
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": "Previous" } )
	url = '{0}?action=listgamesyest&provider={1}'.format(sysaddon,provider)
	items.append((url, listItem, True))								 
  for y in sports_utils.years(provider):
	listItem = control.item(label = str(y))
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": str(y) } )
	url = '{0}?action=listmonths&year={1}&provider={2}'.format(sysaddon,y,provider)
	items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(syshandle, items, len(items)) 
  control.directory(syshandle, cacheToDisc=True)
  control.content(syshandle, 'files')

def listmonths(year,provider):
  icon = NHLicon if provider == "NHL.tv" else MLBicon
  items = []
  for (mn,m) in sports_utils.months(year):
	listItem = control.item(label = mn)
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": mn } )
	url = '{0}?action=listdays&year={1}&month={2}&provider={3}'.format(sysaddon,year,m,provider)
	items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(syshandle, items, len(items)) 
  control.directory(syshandle, cacheToDisc=True)
  control.content(syshandle, 'files')

def listdays(year,month,provider):
  icon = NHLicon if provider == "NHL.tv" else MLBicon
  items = []
  for d in sports_utils.days(year,month):
	listItem = control.item(label = str(d))
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": str(d) } )
	url = '{0}?action=listgames&year={1}&month={2}&day={3}&provider={4}'.format(sysaddon,year,month,d,provider)
	items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(syshandle, items, len(items)) 
  control.directory(syshandle, cacheToDisc=True)
  control.content(syshandle, 'files')

def listproviders():
  items = []
  providers = config.get("Sports","Providers").split(",")
  for provider in providers:
	listItem = control.item(label = provider)
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": provider } )
	url = '{0}?action=listtodaysgames&provider={1}'.format(sysaddon,provider)
	items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(syshandle, items, len(items)) 
  control.directory(syshandle, cacheToDisc=True)

def MergeImgBAK(provider,away,home):
	dirname = 'nhlteams' if provider == 'NHL.tv' else 'mlbteams'
	awayicon = os.path.join(artPath, 'sports', dirname, away+'.jpg')
	homeicon = os.path.join(artPath, 'sports', dirname, home+'.jpg')
	
	try:
		control.create_folder(os.path.join(control.dataPath, 'gameicons', 'TEST'))
	except:
		pass

	files = [
	  awayicon,
	  homeicon]

	icon = away + 'vs' + home + '.jpg'

	result = Image.new("RGB", (512, 512))

	for index, file in enumerate(files):
	  path = os.path.expanduser(file)
	  img = Image.open(path)
	  img.thumbnail((512, 400), Image.ANTIALIAS)
	  x = index // 2 * 400
	  y = index % 2 * 394
	  w, h = img.size
	  print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
	  result.paste(img, (x, y, x + w, y + h))

	result.save(os.path.expanduser(os.path.join(artPath, 'sports', dirname, icon)))
	return os.path.join(artPath, 'sports', dirname, icon)

def GameIcon(provider,away,home):
	dirname = 'nhlteams' if provider == 'NHL.tv' else 'mlbteams'
	awayicon = os.path.join(artPath, 'sports', dirname, away+'.jpg')
	homeicon = os.path.join(artPath, 'sports', dirname, home+'.jpg')
	versusicon = os.path.join(artPath, 'sports', 'versus.jpg')
	iconpath = os.path.join(control.dataPath, 'Gameicons', dirname)
	icon = away + 'vs' + home + '.jpg'
	try:
		control.create_folder(iconpath)
	except:
		pass

	files = [
	  awayicon,
	  versusicon,
	  homeicon]

	result = Image.new("RGB", (512, 512))

	for index, file in enumerate(files):
	  path = os.path.expanduser(file)
	  img = Image.open(path)
	  img.thumbnail((512, 400), Image.ANTIALIAS)
	  x = index // 3 * 171
	  y = index % 3 * 196
	  w, h = img.size
	  print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
	  result.paste(img, (x, y, x + w, y + h))

	result.save(os.path.expanduser(os.path.join(iconpath, icon)))
	return os.path.join(iconpath, icon)

def teams(provider,dest):
	if provider == "NHL.tv":
		return (
		'ANA' if 'Ducks' in dest
		else 'ARI' if 'Coyotes' in dest
		else 'BOS' if 'Bruins' in dest
		else 'BUF' if 'Sabres' in dest
		else 'CAL' if 'Flames' in dest
		else 'CAR' if 'Hurricanes' in dest
		else 'CBJ' if 'Jackets' in dest
		else 'CHI' if 'Blackhawks' in dest
		else 'COL' if 'Avalanche' in dest
		else 'DAL' if 'Stars' in dest
		else 'DET' if 'Wings' in dest
		else 'EDM' if 'Oilers' in dest
		else 'FLA' if 'Panthers' in dest
		else 'LAK' if 'Kings' in dest
		else 'MIN' if 'Wild' in dest
		else 'MTL' if 'Canadiens' in dest
		else 'NSH' if 'Predators' in dest
		else 'NHL' if 'Nhl' in dest
		else 'NJD' if 'Devils' in dest
		else 'NYI' if 'Islanders' in dest
		else 'NYR' if 'Rangers' in dest
		else 'OTT' if 'Senators' in dest
		else 'PHI' if 'Flyers' in dest
		else 'PIT' if 'Penguins' in dest
		else 'SJS' if 'Sharks' in dest
		else 'STL' if 'Blues' in dest
		else 'TBL' if 'Lightning' in dest
		else 'TOR' if 'Leafs' in dest
		else 'VAN' if 'Canucks' in dest
		else 'VGK' if 'Knights' in dest
		else 'WSH' if 'Captials' in dest
		else 'WPG' if 'Jets' in dest
		else 'NHL')
	if provider == "MLB.tv":
		return (
		'ARI' if 'Arizona' in dest
		else 'ATL' if 'Atlanta' in dest
		else 'BAL' if 'Baltimore' in dest
		else 'BOS' if 'Boston' in dest
		else 'CHIC' if 'Cubs' in dest
		else 'CHIWS' if 'White' in dest
		else 'CIN' if 'Cincinnati' in dest
		else 'CLE' if 'Cleveland' in dest
		else 'COL' if 'Colorado' in dest
		else 'DET' if 'Detroit' in dest
		else 'HOU' if 'Houston' in dest
		else 'KAN' if 'Kansas' in dest
		else 'LAD' if 'Dodgers' in dest
		else 'LAA' if 'Angels' in dest
		else 'MIA' if 'Miami' in dest
		else 'MIL' if 'Milwaukee' in dest
		else 'MIN' if 'Minnesota' in dest
		else 'NWM' if 'Mets' in dest
		else 'NYY' if 'Yankees' in dest
		else 'OAK' if 'Oakland' in dest
		else 'PHI' if 'Philadelphia' in dest
		else 'PIT' if 'Pittsburgh' in dest
		else 'SEA' if 'Seattle' in dest
		else 'SAND' if 'Diego' in dest
		else 'SANF' if 'Francisco' in dest
		else 'STL' if 'Louis' in dest
		else 'TAM' if 'Tampa' in dest
		else 'TEX' if 'Texas' in dest
		else 'TOR' if 'Toronto' in dest
		else 'WAS' if 'Washington' in dest
		else 'MLB')
	
def clearicons():
	try:
		iconpath = os.path.join(control.dataPath, 'Gameicons')
		control.removeFolder(iconpath)
	except:
		pass

def listgames(date,provider,previous = False):
  items = []
  dategames = games(date,provider)
  for g in dategames:
	label = "%s vs. %s [%s]" % (g.awayFull,g.homeFull,g.remaining if g.remaining != "N/A" else sports_utils.asCurrentTz(date,g.time))

	###gameicon
	away = teams(provider,g.awayFull)
	home = teams(provider,g.homeFull)
	
	#icon = GameIcon(provider,away,home)#testing
	try: 
		icon = GameIcon(provider,away,home)
	except:
		icon = NHLicon if provider == 'NHL.tv' else MLBicon
	############

	listItem = control.item(label = label)
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": label } )
	url = '{0}?action=feeds&game={1}&date={2}&provider={3}'.format(sysaddon,g.id,date,provider)
	items.append((url, listItem, True))
  if len(items) == 0:
	control.dialog.ok(control.addonName(), "No games scheduled today")
  if previous:
	icon = NHLicon if provider == 'NHL.tv' else MLBicon 
	listItem = control.item(label = "[COLOR red][ Games Archive ][/COLOR]")
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": "Previous" } )
	url = '{0}?action=listyears&provider={1}&'.format(sysaddon,provider)
	items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(syshandle, items, len(items)) 
  control.directory(syshandle, cacheToDisc=True)
  control.content(syshandle, 'files')
  xbmc.log("Added %d games" % len(items))

def listfeeds(game,date,provider):
  items = []
  for f in filter(lambda f: f.viewable(), game.feeds):
	label = str(f)
	#network icon
	icon = (
	tway if '3-Way' in str(f)
	else alt if 'ALT' in str(f)
	else att if 'ATT' in str(f)
	else cbc if 'CBC' in str(f)
	else fox if 'FS' in str(f)
	else msg if 'MSG' in str(f)
	else nbcs if 'NBCS' in str(f)
	else nesn if 'NESN' in str(f)
	else nhl if 'NHL' in str(f)
	else prime if 'PRIME' in str(f)
	else rds if 'RDS' in str(f)
	else ref if 'REF' in str(f)
	else sn if 'SN' in str(f)
	else sun if 'SUN' in str(f)
	else tsn if 'TSN' in str(f)
	else tvas if 'TVAS' in str(f)
	else NHLicon if provider == "NHL.tv" else MLBicon)
	listItem = control.item(label = label)
	listItem.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': banner, 'fanart': fanart})#art
	listItem.setInfo( type="Video", infoLabels={ "Title": label } )
	url = '{0}?action=playsports&date={1}&feedId={2}&provider={3}&state={4}'.format(sysaddon,date,f.mediaId,provider,game.gameState)
	
	items.append((url, listItem, False))

  ok = xbmcplugin.addDirectoryItems(syshandle, items, len(items)) 
  control.directory(syshandle, cacheToDisc=True)
  control.content(syshandle, 'addons')

def playgame(date,feedId,provider,state):
  def adjustQuality(masterUrl):
	bestQuality = "720p 60fps"
	qualityUrlDict = {
	  "360p": "1200K/1200_{0}.m3u8",
	  "540p": "2500K/2500_{0}.m3u8",
	  "720p": "3500K/3500_{0}.m3u8"
	}
	if control.setting("sport.quality") == bestQuality: 
	  return masterUrl
	else:
	  #m3u8Path = qualityUrlDict.get(control.setting("sport.quality"))

	  m3u8Path = qualityUrlDict.get(control.setting("sport.quality")).format('slide' if state == 'In Progress' else 'complete-trimmed')
	  
	  #m3u8Path = qualityUrlDict.get(current, "3500K/3500_{0}.m3u8").format('slide' if state == 'In Progress' else 'complete-trimmed')

	  return masterUrl.rsplit('/',1)[0] + "/" + m3u8Path

  def xbmcPlayer(url,mediaAuth):
	xbmc.log("XBMC trying to play URL [%s]" % (url), xbmc.LOGNOTICE)
	completeUrl = url + ("|Cookie=mediaAuth%%3D%%22%s%%22" % (mediaAuth))
	xbmc.Player().play(adjustQuality(url) + ("|Cookie=mediaAuth%%3D%%22%s%%22" % (mediaAuth)))

  cdn = 'akc' if control.setting("sport.cdn") == "Akamai" else 'l3c'

  def getContentUrl(withCdn = True):
	actualCdn = cdn if withCdn else ""
	if provider == "NHL.tv":
	  return "http://freegamez.ga/m3u8/%s/%s%s" % (date,feedId,actualCdn)
	else:
	  return "http://freegamez.ga/mlb/m3u8/%s/%s%s" % (date,feedId,actualCdn)

  contentUrl = getContentUrl()
  xbmc.log("Trying to resolve from content-url: '" + contentUrl  + "'", xbmc.LOGNOTICE)
  if not sports_utils.head(contentUrl):
	contentUrl = getContentUrl(False)
	if not sports_utils.head(contentUrl):
	  xbmc.log("Cannot resolve content-url '" + contentUrl + "'", xbmc.LOGERROR)
	  raise ValueError("Invalid content-url '" + contentUrl + "'") 
  response = urllib.urlopen(contentUrl)
  playUrl = response.read().replace('l3c',cdn)
  xbmc.log("Play URL resolved to : '" + playUrl  + "'", xbmc.LOGNOTICE)
  mediaAuthSalt = sports_utils.salt()
  if sports_utils.head(playUrl,dict(mediaAuth=mediaAuthSalt)):
	xbmcPlayer(playUrl,mediaAuthSalt)
  else:
	otherCdn = 'akc' if cdn == 'l3c' else 'l3c' 
	xbmc.log("URL [%s] failed on HEAD, switching CDN from %s to %s" % (playUrl,cdn,otherCdn), xbmc.LOGNOTICE)
	xbmcPlayer(playUrl.replace(cdn,otherCdn), mediaAuthSalt)

def hostsModify(provider):
	try:
		#ipaddress = config.get("Sports","HostIP")#old-method
		ipaddress = socket.gethostbyname("powersports.ml")#new-method

		if 'darwin' in sys.platform:
			filename = '/private/etc/hosts'
		elif 'linux' in sys.platform:
			filename = '/etc/hosts'
		elif 'win' in sys.platform:
			filename = 'c:\windows\system32\drivers\etc\hosts'

		if control.setting('notify.hosts') == 'true':
			control.execute("Notification('Ascension',Modifying Hosts file)")

		if provider == 'NHL.tv':
			NHLhostname = config.get(provider,"Host")
			NHLhostname2 = config.get(provider,"Host2")
			NHLhost = ipaddress + "\t" + NHLhostname
			NHLhost2 = ipaddress + "\t" + NHLhostname2
			#NHL
			with open(filename, "r+") as hosts:
				for line in hosts:
					if NHLhost in line:
					   break
				else: # not found, we are at the eof
					hosts.write("\n" + NHLhost + "\n") # append missing data
			#NHL2
			with open(filename, "r+") as hosts:
				for line in hosts:
					if NHLhost2 in line:
					   break
				else:
					hosts.write("\n" + NHLhost2 + "\n")

		if provider == 'MLB.tv':
			MLBhostname = config.get(provider,"Host")
			MLBhostname2 = config.get(provider,"Host2")
			MLBhost = ipaddress + "\t" + MLBhostname
			MLBhost2 = ipaddress + "\t" + MLBhostname2
			#MLB
			with open(filename, "r+") as hosts:
				for line in hosts:
					if MLBhost in line:
					   break
				else:
					hosts.write("\n" + MLBhost + "\n")
			#MLB2
			with open(filename, "r+") as hosts:
				for line in hosts:
					if MLBhost2 in line:
					   break
				else:
					hosts.write("\n" + MLBhost2 + "\n")
	except:
		gcERROR = 'Gamecenter Error'
		errorMSG = "Your Hosts file Can't be Accessed!"
		modifyMSG = 'You May Need to Modify your Hosts file Manually'
		modWinMSG = 'Please Run Kodi as Administrator'
		if 'darwin' in sys.platform:
			control.dialog.ok(gcERROR, errorMSG, '', modifyMSG)
		elif 'android' in sys.platform:
			control.dialog.ok(gcERROR, errorMSG, '', modifyMSG)
		elif 'linux' in sys.platform:
			#control.dialog.ok(gcERROR, errorMSG, '', modifyMSG)
			pass
		elif 'win' in sys.platform:
			control.dialog.ok(gcERROR, errorMSG, '', modWinMSG)

def nhlgames():
  provider = "NHL.tv"
  if control.setting('modify.hosts') == 'true': hostsModify(provider)
  listgames(sports_utils.today().strftime("%Y-%m-%d"),provider,True)

def mlbgames(): 
  provider = "MLB.tv" 
  if control.setting('modify.hosts') == 'true': hostsModify(provider)
  listgames(sports_utils.today().strftime("%Y-%m-%d"),provider,True)

def MergeImg_Initial_WORKING():
	Merged = os.path.join(artPath, 'sports', 'nhlteams', 'COMBINED.jpg')
	files = [
	  VAN,
	  MIN]
	result = Image.new("RGB", (512, 512))
	for index, file in enumerate(files):
	  path = os.path.expanduser(file)
	  img = Image.open(path)
	  img.thumbnail((512, 400), Image.ANTIALIAS)
	  x = index // 2 * 400
	  y = index % 2 * 394
	  w, h = img.size
	  print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
	  result.paste(img, (x, y, x + w, y + h))
	result.save(os.path.expanduser(Merged))  
