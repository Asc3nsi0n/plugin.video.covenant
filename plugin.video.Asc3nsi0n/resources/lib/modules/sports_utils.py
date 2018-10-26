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

import os,sys,xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
import urllib,urllib2,urlparse,json
from datetime import datetime, timedelta
import calendar
import time
import random
import requests
import re
import base64

from resources.lib.modules import control
from resources.lib.modules import pytz
from resources.lib.modules.pytz import timezone
from resources.lib.modules.pytz import reference

class FeedBuilder:

  @staticmethod
  def fromContent(content,streamProvider):
    if streamProvider == "MLBTV":
      idProvider = lambda item: item["id"]
    else:
      idProvider = lambda item: item["mediaPlaybackId"]

    def fromItem(item):
      mediaFeedType = item["mediaFeedType"].upper()
      if mediaFeedType == "HOME":
        return Home(item["callLetters"],idProvider(item))
      elif mediaFeedType == "NATIONAL":
        return National(item["callLetters"],idProvider(item))
      elif mediaFeedType == "AWAY":
        return Away(item["callLetters"],idProvider(item))
      elif mediaFeedType == "FRENCH":
        return French(item["callLetters"],idProvider(item))
      elif mediaFeedType == "COMPOSITE":
        return Composite(item["callLetters"],idProvider(item))
      elif mediaFeedType == "ISO":
        return Other(item["feedName"],item["callLetters"],idProvider(item))
      else:
        return NonViewable(item["callLetters"],idProvider(item))
    if "media" in content:
      return [fromItem(item) 
        for stream in content["media"]["epg"] if stream["title"] == streamProvider
        for item in stream["items"]]
    else:
      return []

class Feed(object):
    _tvStation = None
    _mediaId = None

    def __init__(self,tvStation,mediaId):
        self._tvStation = tvStation
        self._mediaId = mediaId

    def viewable(self): return True

    #@property
    def tvStation(self):
        return self._tvStation
    #@property
    def mediaId(self):
        return self._mediaId

class Home(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self):
        return "%s [COLOR blue](Home)[/COLOR]" % (self.tvStation)

class NonViewable(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)

    def __repr__(self): return "NonViewable"

    def viewable(self): 
        return False

class Away(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "%s [COLOR red](Away)[/COLOR]" % (self.tvStation)

class National(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "%s [COLOR blue](National)[/COLOR]" % (self.tvStation)

class French(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "%s [COLOR teal](French)[/COLOR]" % (self.tvStation)

class Composite(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "3-Way Camera [COLOR yellow](Composite)[/COLOR]"

class Other(Feed):
    _feedName = None
    def __init__(self,feedName,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
        self._feedName = feedName
    def __repr__(self): return self._feedName


class Game:
  _home = None
  _homeFull = None
  _away = None
  _awayFull = None 
  _gameState = None
  _time = None
  _id = None
  _remaining = None 
  _feeds = []

  def __init__(self,id,away,home,time,gameState,awayFull,homeFull,remaining,feeds = []):
    self._id = id
    self._away = away
    self._home = home
    self._time = time
    self._gameState = gameState
    self._awayFull = awayFull
    self._homeFull = homeFull
    self._remaining = remaining
    if feeds is None:
      self._feeds = []
    else:
      self._feeds = feeds
  #@property
  def id(self):
    return self._id
  #@property
  def away(self):
    return self._away
  #@property
  def home(self):
    return self._home
  #@property
  def time(self):
    return self._time
  #@property
  def gameState(self):
    return self._gameState
  #@property
  def awayFull(self):
    return self._awayFull
  #@property
  def homeFull(self):
    return self._homeFull
  #@property
  def remaining(self):
    return self._remaining
  #@property
  def feeds(self):
    return self._feeds

  def __repr__(self):
    return "Game(%s vs. %s, %s, feeds: %s)" % (self.away,self.home,self.remaining,", ".join(map(lambda f: f.tvStation, self.feeds)))
 
class GameBuilder:

  @staticmethod
  def mlbTvRemaining(state,game):
      if "In Progress" in state:
        return game["linescore"]["currentInningOrdinal"] + " " + game["linescore"]["inningHalf"] 
      elif state == "Final":
        return "Final"
      elif state == "Postponed":
        return "PPD"
      else:
        return "N/A"

  @staticmethod
  def nhlTvRemaining(state,game):
    if "In Progress" in state:
      return game["linescore"]["currentPeriodOrdinal"] + " " + game["linescore"]["currentPeriodTimeRemaining"]
    elif state == "Final":
      return "Final"
    else:
      return "N/A"
    
  @staticmethod
  def fromDate(config,date,remaining,provider):
    xbmc.log("Fetching games from: '" + config.get(provider,"GameScheduleUrl") % (date,date) + "'", level=xbmc.LOGNOTICE)
    response = urllib.urlopen(config.get(provider,"GameScheduleUrl") % (date,date))
    data = json.loads(response.read())
    if data["totalItems"] <= 0 or len(data["dates"]) == 0:
      return []
    games = data["dates"][0]["games"]
    def asGame(g):
      away = g["teams"]["away"]["team"]
      home = g["teams"]["home"]["team"]
      time = g["gameDate"][11:].replace("Z", "") 
      state = g["status"]["detailedState"]
      return Game(g["gamePk"], away["abbreviation"], home["abbreviation"], "TBD" if time == "04:00:00" else time, state,away["name"],home["name"],remaining(state,g),FeedBuilder.fromContent(g["content"],config.get(provider,"Provider")))
    return map(asGame, games)

##########################################################
#utils.py

losangeles = timezone('America/Los_Angeles')
localtz = reference.LocalTimezone()

def today(tz = losangeles):
  date = datetime.now()
  return tz.localize(date)
  
def yesterday(tz = losangeles):
  date = datetime.now() - timedelta(days=1)
  return tz.localize(date) 							

def asCurrentTz(d,t): 
  parsed = None
  try:
    parsed = datetime.strptime(d + " " + t,'%Y-%m-%d %H:%M:%S')
  except TypeError:
    parsed = datetime(*(time.strptime(d + " " + t, '%Y-%m-%d %H:%M:%S')[0:6]))
  replaced = parsed.replace(tzinfo=timezone('UTC'))
  local = replaced.astimezone(localtz)
  return "%02d:%02d" % (local.hour, local.minute)


def years(provider): 
  start = 2017 if provider == "MLB.tv" else 2015
  return xrange(start,today().year + 1)
  
#def years(): return xrange(2017,today().year - 2, -1)												
#def years(): return xrange(2015,today().year + 1)  

def months(year): 
  if int(year) == today().year:
    return map(lambda m: (calendar.month_name[m],m), xrange(1,today().month + 1))
  else:
    return map(lambda m: (calendar.month_name[m],m), xrange(1,13))

def days(year,month): 
  if int(year) == today().year and int(month) == today().month:
    return xrange(1,today().day)
  else:
    r = calendar.monthrange(int(year),int(month))
    return xrange(1,max(r)+1)

def garble(salt = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"): return ''.join(random.sample(salt,len(salt)))

def salt():
  garbled = garble()
  return ''.join([garbled[int(i * random.random()) % len(garbled)]  for i in range(0,241)])

def head(url,cookies = dict()):
  print "Checking url %s" % (url)
  return requests.request('HEAD',url,cookies = cookies).status_code < 400
  
################################################################################################

urlx = ''.join([chr(int(''.join(c), 16)) for c in zip('61485230'[0::2],'61485230'[1::2])])
I11Ii1iI = 'WTBSdmRrd3lUbWxOU0docldWaFNhRXh1VFhwTWJVWjBXVmh3ZG1KdFJqTmplVFZxWWpJd2RtTnRWbmRpZVRCNFRuazVkMkpJVm01aFZ6UjFaRzFzYTFwWE9IVlJXRTVxVFRJMWVtRlVRblZNTTA1M1lqTktNR041TVhwa1IwWXdaRmhOZFdSSWFEQT0='.decode('base64').decode('base64')
I1IIi1iI = urlx+I11Ii1iI
statustxt = I1IIi1iI.decode('base64')
#statusurl = 'PRIVATE/plugin.video.Asc3nsi0n/sports-status.txt'

def openURL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def checkstatus(name, ret):
	link = openURL(statustxt).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?tatus="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for status in match:
			if ret == 'status': 
				return status
			else: 
				pass
	else: 
		return False

try:
	status = checkstatus('SPORTS', 'status')
	statuslabel = status
	#if status == 'WORKING': statuslabel = '[COLOR ff006400]WORKING[/COLOR]'
	#if status == 'DOWN':    statuslabel = '[COLOR red]DOWN[/COLOR]'
	#if status == 'DEAD':    statuslabel = '[COLOR red]DEAD ![/COLOR]'
	statusicon = os.path.join(control.artPath(), 'working.png') if 'WORKING' in status else os.path.join(control.artPath(), 'down.png')
except:
	pass
