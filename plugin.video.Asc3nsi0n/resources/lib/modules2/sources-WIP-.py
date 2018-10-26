# -*- coding: utf-8 -*-

'''
    Asc3nsi0n Video Add-on
    Copyright (C) 2017

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
'''
import xbmc,xbmcaddon,xbmcgui,xbmcvfs
import sys,pkgutil,re,json,urllib,urlparse,random,datetime,time,os

from resources.lib.modules2 import dialogs, dialogs_list
from resources.lib.modules2.executor import execute
from schism_commons import cleantitle_get

from resources.lib.modules2 import control
from resources.lib.modules2 import cleantitle
from resources.lib.modules2 import client
from resources.lib.modules2 import debrid
from resources.lib.modules2 import realdebrid 
from resources.lib.modules2 import workers
from resources.lib.modules2 import unshorten
from threading import Event
import universalscrapers

#debridstatus = control.setting('debrid.show')
#debridcolor = control.setting('debrid.color')
#debridlabel = control.setting('debrid.label')

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

try:
	if control.setting('resolver') == '0': 
		import resolveurl as urlresolver
		if xbmcaddon.Addon('script.module.resolveurl').getSetting('RealDebridResolver_enabled') == 'true':
			c = [i for i in debrid.credentials().values() if not '' in i.values()]
			if len(c) == 0: debridstatus = "false"
			else: debridstatus = "true"
		else:
			debridstatus = "false"
	else:
		import urlresolver
		if xbmcaddon.Addon('script.module.urlresolver').getSetting('RealDebridResolver_enabled') == 'true':
			c = [i for i in debrid.credentials().values() if not '' in i.values()]
			if len(c) == 0: debridstatus = "false"
			else: debridstatus = "true"
		else:
			debridstatus = "false"
except:
	debridstatus = "false"

_shst_regex = ['sh.st','viid.me']


class sources:
    def __init__(self):
        self.getConstants()
        self.sources = []

    def play(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
        try:
            url = None


            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)

            select = control.setting('hosts.mode') if select == None else select

            title = tvshowtitle if not tvshowtitle == None else title

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0:

                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemProperty)
                    control.window.setProperty(self.itemProperty, json.dumps(items))

                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)

                    control.sleep(200)

                    return control.execute('Container.Update(%s?action=addItem2&title=%s)' % (sys.argv[0], urllib.quote_plus(title.encode('utf-8'))))

                elif select == '0' or select == '1' or select == '3' or select == '4':
                    url = self.sourcesDialog(items)

                else:
                    url = self.sourcesDirect(items)


            if url == None:
                return self.errorForSources()

            try: meta = json.loads(meta)
            except: pass

            from resources.lib.modules2.player import player
            player().run(title, year, season, episode, imdb, tvdb, url, meta)
        except:
            pass

    def play_alter(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta):
        try:
            url = None
            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)
            if control.setting('hosts.mode') == '2': select = "1"
            else: select = "2"

            title = tvshowtitle if not tvshowtitle == None else title

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0:

                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemProperty)
                    control.window.setProperty(self.itemProperty, json.dumps(items))

                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)

                    control.sleep(200)

                    return control.execute('Container.Update(%s?action=addItem2&title=%s)' % (sys.argv[0], urllib.quote_plus(title.encode('utf-8'))))

                elif select == '0' or select == '1' or select == '5':
                    url = self.sourcesDialog(items)

                else:
                    url = self.sourcesDirect(items)

            if url == None:
                return self.errorForSources()

            meta = json.loads(meta)

            from resources.lib.modules2.player import player
            player().run(title, year, season, episode, imdb, tvdb, url, meta)
        except:
            pass

    def play_dialog(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
        try:
            url = None

            items = self.getSource_dialog(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)
            title = tvshowtitle if not tvshowtitle == None else title
            header = control.addonInfo('name')
            header2 = header.upper()
            try: meta = json.loads(meta)
            except: meta = ''
            progressDialog = control.progressDialog if control.setting('progress.dialog') == '0' else control.progressDialogBG
            progressDialog.create(header, '')
            progressDialog.update(0)
            filter = []

            for i in range(len(items)):

                try:
                    try:

                        label = '[B]%s[/B] | %s | [B][I]%s [/I][/B]' % (items[i]['scraper'], items[i]['source'], items[i]['quality'])


                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), label.upper(), '')
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), label.upper())

                    # if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)

                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)

                    if w.is_alive() == True: block = items[i]

                    if self.url == None: raise Exception()

                    try: progressDialog.close()
                    except: pass

                    control.sleep(200)
                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')

                    from resources.lib.modules2.player import player
                    player().run(title, year, season, episode, imdb, tvdb, self.url, meta)

                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

            self.errorForSources()
        except:
            pass

    def play_dialog_list(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
        try:
            url = None

            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)

            select = control.setting('hosts.mode') if select == None else select

            title = tvshowtitle if not tvshowtitle == None else title

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0: url = self.sourcesDialog2(items)
            if url == None: return self.errorForSources()

            meta = json.loads(meta)

            from resources.lib.modules2.player import player
            player().run(title, year, season, episode, imdb, tvdb, url, meta)
        except:
            pass

    def play_library(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
        try:
            url = None

            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)

            select = control.setting('hosts.mode') if select == None else select

            title = tvshowtitle if not tvshowtitle == None else title

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0:

                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemProperty)
                    control.window.setProperty(self.itemProperty, json.dumps(items))

                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)

                    control.sleep(200)

                    return control.execute('Container.Update(%s?action=addItem2&title=%s)' % (sys.argv[0], urllib.quote_plus(title.encode('utf-8'))))

                elif select == '0' or select == '1':
                    url = self.sourcesDialog(items)

                else:
                    url = self.sourcesDirect(items)

            if url == None:
                return self.errorForSources()

            meta = 'play_library'

            from resources.lib.modules2.player import player
            player().run(title, year, season, episode, imdb, tvdb, url, meta)
        except:
            pass

    def addItem(self, title):
        control.playlist.clear()

        items = control.window.getProperty(self.itemProperty)
        items = json.loads(items)

        if items == None or len(items) == 0: control.idle() ; sys.exit()

        meta = control.window.getProperty(self.metaProperty)
        meta = json.loads(meta)

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        downloads = True if control.setting('downloads') == 'true' and not (control.setting('movie.download.path') == '' or control.setting('tv.download.path') == '') else False

        if 'tvshowtitle' in meta and 'season' in meta and 'episode' in meta:
            name = '%s S%02dE%02d' % (title, int(meta['season']), int(meta['episode']))
        elif 'year' in meta:
            name = '%s (%s)' % (title, meta['year'])
        else:
            name = title

        systitle = urllib.quote_plus(title.encode('utf-8'))

        sysname = urllib.quote_plus(name.encode('utf-8'))

        poster = meta['poster'] if 'poster' in meta else '0'
        banner = meta['banner'] if 'banner' in meta else '0'
        thumb = meta['thumb'] if 'thumb' in meta else poster
        fanart = meta['fanart'] if 'fanart' in meta else '0'

        if poster == '0': poster = control.addonPoster()
        if banner == '0' and poster == '0': banner = control.addonBanner()
        elif banner == '0': banner = poster
        if thumb == '0' and fanart == '0': thumb = control.addonFanart()
        elif thumb == '0': thumb = fanart
        if control.setting('fanart') == 'true' and not fanart == '0': pass
        else: fanart = control.addonFanart()

        sysimage = urllib.quote_plus(poster.encode('utf-8'))

        downloadMenu = control.lang(32403).encode('utf-8')

        for i in range(len(items)):
            try:
                label = items[i]['label']

                syssource = urllib.quote_plus(json.dumps([items[i]]))

                sysurl = '%s?action=playItem2&title=%s&source=%s' % (sysaddon, systitle, syssource)

                cm = []

                if downloads == True:
                    cm.append((downloadMenu, 'RunPlugin(%s?action=download2&name=%s&image=%s&source=%s)' % (sysaddon, sysname, sysimage, syssource)))

				###togglescraper_sources###
                #if control.setting('internal.scrapers')=='true': cm.append((control.lang(33615).encode('utf-8'), 'RunPlugin(%s?action=togglescrapersources)' % (sysaddon)))
                #if control.setting('internal.scrapers')=='false': cm.append((control.lang(33614).encode('utf-8'), 'RunPlugin(%s?action=togglescrapersources)' % (sysaddon)))
				############################
                item = control.item(label=label)

                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})

                if not fanart == None: item.setProperty('Fanart_Image', fanart)

                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = meta)

                control.addItem(handle=syshandle, url=sysurl, listitem=item, isFolder=False)
            except:
                pass

        control.content(syshandle, 'files')
        control.directory(syshandle, cacheToDisc=True)

    def playItem(self, title, source):
        try:
            meta = control.window.getProperty(self.metaProperty)
            meta = json.loads(meta)

            year = meta['year'] if 'year' in meta else None
            season = meta['season'] if 'season' in meta else None
            episode = meta['episode'] if 'episode' in meta else None

            imdb = meta['imdb'] if 'imdb' in meta else None
            tvdb = meta['tvdb'] if 'tvdb' in meta else None

            next = [] ; prev = [] ; total = []

            for i in range(1,1000):
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    next.append(u)
                except:
                    break
            for i in range(-1000,0)[::-1]:
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    prev.append(u)
                except:
                    break

            items = json.loads(source)
            items = [i for i in items+next+prev][:40]

            header = control.addonInfo('name')
            header2 = header.upper()

            progressDialog = control.progressDialog if control.setting('progress.dialog') == '0' else control.progressDialogBG
            progressDialog.create(header, '')
            progressDialog.update(0)

            block = None

            for i in range(len(items)):
                try:
                    try:
                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))

                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)


                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    try: progressDialog.close()
                    except: pass

                    control.sleep(200)
                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')

                    from resources.lib.modules2.player import player
                    player().run(title, year, season, episode, imdb, tvdb, self.url, meta)

                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

            self.errorForSources()
        except:
            pass

    def createProgressDialog(self,header,items=None,i=None):
        progressDialog = control.progressDialog if control.setting('progress.dialog') == '0' else control.progressDialogBG
        progressDialog.create(header, '')
        if items != None and i != None:
            progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
        else:
            progressDialog.update(0)
        return progressDialog

    def downloadItem(self, name, image, source):
        try:
            next = [] ; prev = [] ; total = []

            for i in range(1,1000):
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    next.append(u)
                except:
                    break
            for i in range(-1000,0)[::-1]:
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    prev.append(u)
                except:
                    break

            items = json.loads(source)
            items = [i for i in items+next+prev][:40]

            header = control.addonInfo('name')
            header2 = header.upper()
            
            progressDialog = self.createProgressDialog(header)
            
            block = None

            success = False
            for i in range(len(items)):
                try:
                    try:
                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))

                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)


                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    try: progressDialog.close()
                    except: pass

                    control.sleep(200)
                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')

                    from resources.lib.modules2 import downloader
                    success = downloader.download(name, image, self.url)
                    if success:
                        break;
                    else:
                        progressDialog = self.createProgressDialog(header,items,i)
                except:
                    pass
            if not success:
                self.errorForSources()
        except:
            pass
    def getSource_dialog(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, presetDict=[], timeout=30):
        self.__scrapers = []
        sourceDict = []
        for pkg, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
        sourceDict = [i[0] for i in sourceDict if i[1] == False]
        sourceDict = [(i, __import__(i, globals(), locals(), [], -1).source()) for i in sourceDict]

        content = 'movie' if tvshowtitle == None else 'episode'
        if content == 'movie':
            sourceDict = [(i[0], i[1], getattr(i[1], 'movie', None)) for i in sourceDict]
        else:
            sourceDict = [(i[0], i[1], getattr(i[1], 'tvshow', None)) for i in sourceDict]
        sourceDict = [(i[0], i[1]) for i in sourceDict if not i[2] == None]

        try: sourceDict = [(i[0], i[1], control.setting('provider.' + i[0])) for i in sourceDict]
        except: sourceDict = [(i[0], i[1], 'true') for i in sourceDict]

        self.__scrapers = [i[1] for i in sourceDict  if not i[2] == 'false']

        self.title = title
        self.year = year
        self.imdb = imdb
        self.tvdb = tvdb
        self.season = season
        self.episode = episode
        self.tvshowtitle = tvshowtitle
        self.premiered = premiered

        print ("ASCENSION SELFSCRAPERS",   self.__scrapers)
        sourceDict = [i[0] for i in sourceDict if not i[2] == 'false']

        threads = []
        select_sources = []
        if control.setting('cachesources') == 'true':
                        control.makeFile(control.dataPath)
                        self.sourceFile = control.providercacheFile

        if content == 'movie':
            scraped_sources = self.scrape_movie_with_dialog()
        else:
            scraped_sources = self.scrape_tv_with_dialog()
        for item in scraped_sources:
            if type(item) == tuple:
                item = item[1]
            if type(item) == list:
                for subitem in item:
                    select_sources.extend(item)
            else:
                select_sources.append(item)
        return select_sources

    def scrape_tv_with_dialog(self, maximum_age=60, sort_function=None):
        try:
            timeout = int(control.setting('scrapers.timeout.0'))
        except:
            pass
        self.timeout = timeout
        allow_debrid = debridstatus == "true"
        scraper = universalscrapers.scrape_episode_with_dialog
        link, rest = scraper(
            self.tvshowtitle,
            self.year,
            self.premiered,
            self.season,
            self.episode,
            self.imdb,
            self.tvdb,
            timeout=self.timeout,
            extended=True,
            sort_function=self.sort_function,
            enable_debrid=allow_debrid)
        if type(link) == dict and "path" in link:
                link = link["path"]
        result = [link]
        result.extend(rest)
        return result

    def scrape_movie_with_dialog(self, maximum_age=60, sort_function=None):
        try:
            timeout = int(control.setting('scrapers.timeout.0'))
        except:
            pass
        self.timeout = timeout
        allow_debrid = debridstatus == "true"
        scraper = universalscrapers.scrape_movie_with_dialog
        link, rest = scraper(
            self.title,
            self.year,
            self.imdb,
            timeout=self.timeout,
            extended=True,
            sort_function=self.sort_function,
            enable_debrid=allow_debrid)
        if type(link) == dict and "path" in link:
            link = link["path"]
        result = [link]
        result.extend(rest)
        return result

    def to_dialog_tuple(self, scraper_array):

        results_array = []
        if scraper_array:
            for link in scraper_array:
                                try:
                                        url = link['url']
                                        quality = ""
                                        try:
                                                quality = link['quality']
                                        except:
                                                quality = "SD"
                                        if "1080" in quality: quality2 = "FHD"
                                        elif "HD" in quality: quality2 = "HD"
                                        else: quality2 = "SD"


                                        label = '%s | %s | %s' % (quality, link['provider'], link['source'])
                                        label = label.upper()
                                        if not url == '' or url == None:
                                                if not any(value in url for value in self.hostBlackList):
                                                        results_array.append(link)

                                except:
                                        pass
            return results_array

    def getSources(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, presetDict=[], timeout=30):
        try: xbmc.executebuiltin('Dialog.Close(busydialog)')
        except: pass
        progressDialog = control.progressDialog if control.setting('progress.dialog') == '0' else control.progressDialogBG
        progressDialog.create(control.addonInfo('name') + ' : ' + control.lang(33708).encode('utf-8'), '')
        progressDialog.update(0, 'Preparing Sources...')
        # if control.setting('cachesources') == 'true': self.prepareSources()

        content = 'movie' if tvshowtitle is None else 'episode'
        try:
            timeout = int(control.setting('scrapers.timeout.0'))
        except:
            pass

        allow_debrid = debridstatus == "true"
        if control.setting('cachesources') == 'true':
                        control.makeFile(control.dataPath)
                        self.sourceFile = control.providercacheFile

        if content == 'movie':
            title = self.getTitle(title)
            scraper = universalscrapers.scrape_movie
            links_scraper = scraper(
                    title,
                    year,
                    imdb,
                    timeout=timeout,
                    enable_debrid=allow_debrid)
        else:
            tvshowtitle = self.getTitle(tvshowtitle)
            scraper = universalscrapers.scrape_episode
            links_scraper = scraper(
                    tvshowtitle,
                    year,
                    premiered,
                    season,
                    episode,
                    imdb,
                    tvdb,
                    timeout=timeout,
                    enable_debrid=allow_debrid)
        thread = workers.Thread(self.get_uni_sources, links_scraper,
                                progressDialog)

        thread.start()
        for i in range(0, timeout * 2):
            try:
                if xbmc.abortRequested:
                    return sys.exit()
                try:
                    if progressDialog.iscanceled():
                        break
                except:
                    pass
                if not thread.is_alive(): break
                time.sleep(0.5)
            except:
                pass

        try:
            progressDialog.close()
        except:
            pass

        self.sourcesFilter()

        return self.sources

    def get_uni_sources(self, links_scraper, progressDialog):
			num_scrapers = len(universalscrapers.relevant_scrapers())
			index = 0
			#string1 = "Time Elapsed %s"
			string2 = control.lang(33705).encode('utf-8')###Sources found:
			string3 = control.lang(32406).encode('utf-8')###Remaining providers: %s
			string4 = control.lang(33707).encode('utf-8')###Completed: %s
			counthd = 0
			count1080 = 0
			countSD = 0
			for scraper_links in links_scraper():
					try:
						if xbmc.abortRequested:
							return sys.exit()
						if progressDialog.iscanceled():
							break
						index = index + 1
						percent = int((index * 100) / num_scrapers)
						#if scraper_links is not None:
						#    random.shuffle(scraper_links)
						for scraper_link in scraper_links:
							try:
									q = scraper_link['quality']
									if "1080" in q:
										count1080 += 1
									elif "HD" in q:
										counthd += 1
									elif "720" in q:
										counthd += 1
										scraper_link["quality"] = "720p"
									elif "560" in q:
										countSD += 1
										scraper_link["quality"] = "HD"
									elif "480" in q:
										countSD += 1
										scraper_link["quality"] = "SD"
									elif "DVD" in q:
										countSD += 1
										scraper_link["quality"] = "SD"
									else:
										countSD += 1

									totalcount = count1080 + counthd + countSD
							except:
								pass

							progressDialog.update(percent,
												  string2 + str(totalcount)
												  + ' | ' +
												  string4 % str(percent)+'%',
												  string3 % (num_scrapers - index))
							self.sources.append(scraper_link)
							try:
								if progressDialog.iscanceled():
									break
							except:
								pass
					except:
						pass		


    def prepareSources(self):
        try:
            control.makeFile(control.dataPath)

            self.sourceFile = control.providercacheFile
        except:
            pass

    def getTitle(self, title):
        title = cleantitle.normalize(title)
        return title

    def getMovieSource(self, title, year, imdb, source, call):
        source = cleantitle_get(str(source))
        type = "movie"

        try:
            url = None
            if url == None: url = call.movie(imdb, title, year)
            if url == None: raise Exception()
        except:
            pass

        try:
            sources = []
            sources = call.sources(url, self.hostDict, self.hostprDict)
            if sources == None: raise Exception()
            self.sources.extend(sources)
        except:
            pass

    def getEpisodeSource(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, source, call):

        source = cleantitle_get(str(source))
        try:
            url = None
            if url == None: url = call.tvshow(imdb, tvdb, tvshowtitle, year)
            if url == None: raise Exception()
        except:
            pass
        try:
            ep_url = None
            if url == None: raise Exception()
            if ep_url == None: ep_url = call.episode(url, imdb, tvdb, title, premiered, season, episode)
            if ep_url == None: raise Exception()
        except:
            pass

        try:
            sources = []
            sources = call.sources(ep_url, self.hostDict, self.hostprDict)
            if sources == None: raise Exception()
            self.sources.extend(sources)
        except:
            pass

    def getMovieSource2(self, title, year, imdb, source, call):
        str_call = str(call)
        r = re.findall('resources.lib.sources.(.+?).source', str_call)[0]

        if r:
                        source = r
        else: source = "Ascension"

        type = "movie"

        try:
            url = None
            if url == None: url = call.movie(imdb, title, year)
            if url == None: raise Exception()
        except:
            pass

        try:
            sources = []
            sources = call.sources(url, self.hostDict, self.hostprDict)
            if sources == None: raise Exception()
            self.sources.extend(sources)
        except:
            pass

        return sources

    def getEpisodeSource2(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, source, call):

        str_call = str(call)
        r = re.findall('resources.lib.sources.(.+?).source', str_call)[0]

        if r:
                        source = r
        else: source = "Ascension"

        type = "episode"
        try:
            url = None
            if url == None: url = call.tvshow(imdb, tvdb, tvshowtitle, year)
            if url == None: raise Exception()
        except:
            pass
        try:
            ep_url = None
            if url == None: raise Exception()
            if ep_url == None: ep_url = call.episode(url, imdb, tvdb, title, premiered, season, episode)
            if ep_url == None: raise Exception()
        except:
            pass

        try:
            sources = []
            sources = call.sources(ep_url, self.hostDict, self.hostprDict)
            if sources == None: raise Exception()
            self.sources.extend(sources)
        except:
            pass

        return sources

    def getURISource(self, url):
        try:
            sourceDict = []
            for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
            sourceDict = [i[0] for i in sourceDict if i[1] == False]
            sourceDict = [(i, __import__(i, globals(), locals(), [], -1).source()) for i in sourceDict]

            domain = (urlparse.urlparse(url).netloc).lower()

            domains = [(i[0], i[1].domains) for i in sourceDict]
            domains = [i[0] for i in domains if any(x in domain for x in i[1])]

            if len(domains) == 0: return False

            call = [i[1] for i in sourceDict if i[0] == domains[0]][0]

            self.sources = call.sources(url, self.hostDict, self.hostprDict)

            for i in range(len(self.sources)):
                try: self.sources[i]['autoplay'] = True
                except: pass

            self.sources = self.sourcesFilter()
            return self.sources
        except:
            pass

    def alterSources(self, url, meta):
        try:
            if control.setting('hosts.mode') == '2': url += '&select=1'
            else: url += '&select=2'
            control.execute('RunPlugin(%s)' % url)
        except:
            pass

    def clearSources(self):
        try:
            control.idle()

            yes = control.yesnoDialog(control.lang(32407).encode('utf-8'), '', '')
            if not yes: return

            control.makeFile(control.uniDataPath)
            dbcon = database.connect(control.uniCacheFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_src")
            dbcur.execute("DROP TABLE IF EXISTS rd_domains")
            dbcur.execute("VACUUM")
            dbcon.commit()

            control.infoDialog(control.lang(32408).encode('utf-8'), sound=True, icon='INFO')
        except:
            pass

    def sourcesFilter(self):
		provider = control.setting('hosts.sort.provider')

		quality = control.setting('hosts.quality')
		if quality == '':
			quality = '0'

		captcha = control.setting('hosts.captcha')

		HEVC = control.setting('HEVC')

		random.shuffle(self.sources)

		if provider == 'true':
			self.sources = sorted(self.sources, key=lambda k: k['scraper'])

		local = [i for i in self.sources if 'local' in i and i.get('local', False) == True]
		self.sources = [i for i in self.sources if not i in local]

		filter = []

		filter += [i for i in self.sources if i['direct'] == True]
		filter += [i for i in self.sources if i['direct'] == False]
		self.sources = filter

		filter = []
		filter += [i for i in self.sources if not i['source'].lower() in self.hostBlackList]

		self.sources = filter

		filter = []
		filter += local
		if quality in ['0']: filter += [i for i in self.sources if i['quality'] == '4k' and i.get('debridonly', False) == True]
		if quality in ['0']: filter += [i for i in self.sources if i['quality'] == '4k'  and i.get('debridonly', False) == False]

		if quality in ['0', '1']: filter += [i for i in self.sources if i['quality'] == '2k' and i.get('debridonly', False) == True]
		if quality in ['0', '1']: filter += [i for i in self.sources if i['quality'] == '2k'  and i.get('debridonly', False) == False]

		if quality in ['0' ,'1', '2']: filter += [i for i in self.sources if i['quality'] == '1080p' and i.get('debridonly', False) == True]
		if quality in ['0', '1', '2']: filter += [i for i in self.sources if i['quality'] == '1080p'  and i.get('debridonly', False) == False]
		if quality in ['0', '1', '2', '3']: filter += [i for i in self.sources if i['quality'] == '720p' and i.get('debridonly', False) == True]
		if quality in ['0', '1', '2', '3']: filter += [i for i in self.sources if i['quality'] == '720p' and i.get('debridonly', False) == False]
		filter += [i for i in self.sources if i['quality'] == 'SD' and i.get('debridonly', False) == True]
		filter += [i for i in self.sources if i['quality'] == 'SD' and i.get('debridonly', False) == False]

		if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'SCR']
		if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'CAM']
		self.sources = filter

		if not captcha == 'true':
			filter = [i for i in self.sources if i['source'].lower() in self.hostcapDict and not 'debrid' in i]
			self.sources = [i for i in self.sources if not i in filter]

		# filter = [i for i in self.sources if i['source'].lower() in self.hostblockDict and not 'debrid' in i]
		# self.sources = [i for i in self.sources if not i in filter]
		self.sources = self.filter_zips(self.sources)

		self.sources = self.sources[:1000]

		prem_identify = control.setting('prem.identify')
		if prem_identify == '': prem_identify = 'ff006400'
		prem_identify = self.getPremColor(prem_identify)

		for i in range(len(self.sources)):
			u = self.sources[i]['url']
			s = self.sources[i]['scraper'].lower()
			s = s.rsplit('.', 1)[0]
			p = self.sources[i]['source']
			d = self.sources[i].get('debridonly', False)
			d = str(d)
			# print ("DEBRID STATUS", d)
			p = re.sub('v\d*$', '', p)

			q = self.sources[i]['quality']
			try:
				f = (' | '.join(['[I]%s [/I]' % info.strip() for info in self.sources[i]['info'].split('|')]))
			except:
				f = ''

			if d == 'True':
				#label = '%02d |[I]DEB[/I] | [B]%s[/B] | ' % (int(i+1), p)
			#if not d == '': label = '%02d | [B]%s[/B] | [B]%s[/B] | ' % (int(i+1), p, d)
				if control.setting('prem.label') == 'true':
					label = '%02d | [COLOR %s][B]%s[/B][/COLOR] | ' % (int(i+1), prem_identify, p)#debrid providers label by name
				else:
					label = '%02d | [COLOR %s][B]%s[/B][/COLOR] | ' % (int(i+1), prem_identify, d)#debrid sources label is realdebrid
			else:
				label = '%02d | [B]%s[/B] | ' % (int(i+1), p)

			if q in ['4K', '2k', '1080p', '720p', 'SD']:
				label += '%s | %s | [B][I]%s [/I][/B]' % (s, f, q)
			#elif q == 'SD':
			#    label += '%s | %s | [I]%s [/I]' % (s, f, q)
			else:
				label += '%s | %s | [I]%s [/I]' % (s, f, q)
			label = label.replace('| 0 |', '|').replace(' | [I]0 [/I]', '')
			label = label.replace('[I]HEVC [/I]', 'HEVC')
			label = re.sub('\[I\]\s+\[/I\]', ' ', label)
			label = re.sub('\|\s+\|', '|', label)
			label = re.sub('\|(?:\s+|)$', '', label)

			self.sources[i]['label'] = label.upper()

		if not HEVC == 'true':
			self.sources = [i for i in self.sources if not 'HEVC' in str(i['label'])]
			#self.sources = [i for i in self.sources if not 'HEVC' or if not'X265' in str(i['label'])]

		return self.sources

    def filter_zips(self, sources):
                filtered = []
                for item in sources:
                        url = item['url'].encode('utf-8')
                        # ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
                        # print ("POSEIDON FILTERING", ext)
                        if "google" in url.lower():
                                filtered.append(item)
                        else:
                                if not any(value in url.lower() for value in self.blacklist_zips):
                                        filtered.append(item)
                return filtered

    def sourcesResolve(self, item, info=False):
        try:
            self.url = None

            u = url = item['url']

            # d = item['debrid'] ;
            direct = item['direct']

            provider = item['scraper'].lower()

            # if not provider.endswith(('_mv', '_tv', '_mv_tv')):
                # sourceDict = []
                # for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
                # provider = [i[0] for i in sourceDict if i[1] == False and i[0].startswith(provider + '_')][0]

            #source = __import__(provider, globals(), locals(), [], -1).source()
            u = url = item["url"]

            if url == None: raise Exception()
            if any(value in url for value in _shst_regex): u = unshorten._unshorten_shst(url)

            # if not d == '':
                # url = debrid.resolver(url, d)

            if not direct == True:

                                if not debridstatus == 'true': hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True, include_universal=False)
                                else: hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True, include_universal=True)
                                if hmf.valid_url() == True: url = hmf.resolve()

            if url == False or url == None: raise Exception()

            ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            if ext == 'rar': raise Exception()

            try: headers = url.rsplit('|', 1)[1]
            except: headers = ''
            headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
            headers = dict(urlparse.parse_qsl(headers))

            xbmc.log("url3:" + repr(url), xbmc.LOGNOTICE)


            if url.startswith('http') and '.m3u8' in url:
                result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
                if result == None: raise Exception()

            elif url.startswith('http'):
                result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='30')
                if result == None: raise Exception()

            else:
                raise Exception()

            xbmc.log("url4:" + repr(url), xbmc.LOGNOTICE)


            self.url = url
            xbmc.log("url2:" + repr(url), xbmc.LOGNOTICE)
            return url
        except:
            if info == True: self.errorForSources()
            return

    def sourcesDialog(self, items):
        try:
            labels = [i['label'] for i in items]

            select = control.selectDialog(labels)
            if select == -1: return 'close://'

            next = [y for x,y in enumerate(items) if x >= select]
            prev = [y for x,y in enumerate(items) if x < select][::-1]

            items = [items[select]]
            items = [i for i in items+next+prev][:40]

            header = control.addonInfo('name')
            header2 = header.upper()

            progressDialog = control.progressDialog if control.setting('progress.dialog') == '0' else control.progressDialogBG
            progressDialog.create(header, '')
            progressDialog.update(0)

            block = None

            for i in range(len(items)):
                try:
                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    try:
                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)


                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    self.selectedSource = items[i]['label']

                    try: progressDialog.close()
                    except: pass

                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')
                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

        except:
            try: progressDialog.close()
            except: pass

    def sourcesDialog2(self, items):
        try:
            labels = [i['label'] for i in items]

            select = dialogs_list.select_ext("Select Link", items)


            selected_items = select
            if not len(selected_items) > 1: return self.errorForSources()
            header = control.addonInfo('name')
            header2 = header.upper()

            progressDialog = control.progressDialog if control.setting('progress.dialog') == '0' else control.progressDialogBG
            progressDialog.create(header, '')
            progressDialog.update(0)

            block = None

            for i in range(len(selected_items)):
                try:
                    if selected_items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, selected_items[i])
                    w.start()

                    try:
                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(selected_items))) * i), str(selected_items[i]['label']), str(' '))
                    except:
                        progressDialog.update(int((100 / float(len(selected_items))) * i), str(header2), str(selected_items[i]['label']))

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)


                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = selected_items[i]['source']

                    if self.url == None: raise Exception()

                    self.selectedSource = selected_items[i]['label']

                    try: progressDialog.close()
                    except: pass

                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')
                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

        except:
            try: progressDialog.close()
            except: pass

    def sourcesDirect(self, items):
        # filter = [i for i in items if i['source'].lower() in self.hostcapDict and i['debrid'] == '']
        # items = [i for i in items if not i in filter]

        # filter = [i for i in items if i['source'].lower() in self.hostblockDict and i['debrid'] == '']
        items = [i for i in items]

        # items = [i for i in items if ('autoplay' in i and i['autoplay'] == True) or not 'autoplay' in i]

        if control.setting('autoplay.sd') == 'true':
                        items = [i for i in items if not i['quality'] in ['4K', '2k', '1080p', 'HD']]

        u = None

        header = control.addonInfo('name')
        header2 = header.upper()

        try:
            control.sleep(1000)

            progressDialog = control.progressDialog if control.setting('progress.dialog') == '0' else control.progressDialogBG
            progressDialog.create(header, '')
            progressDialog.update(0)
        except:
            pass

        for i in range(len(items)):
            try:
                if progressDialog.iscanceled(): break
                progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
            except:
                progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))

            try:
                if xbmc.abortRequested == True: return sys.exit()

                url = self.sourcesResolve(items[i])
                if u == None: u = url
                if not url == None: break
            except:
                pass

        try: progressDialog.close()
        except: pass

        return u

    def errorForSources(self):
        control.infoDialog(control.lang(32401).encode('utf-8'), sound=False, icon='INFO')

    def getConstants(self):
        self.itemProperty = 'plugin.video.Asc3nsi0n.container.items'

        self.metaProperty = 'plugin.video.Asc3nsi0n.container.meta'

        try:
            self.hostDict = urlresolver.relevant_resolvers(order_matters=True)
            self.hostDict = [i.domains for i in self.hostDict if not '*' in i.domains]
            self.hostDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostDict)]
            self.hostDict = [x for y,x in enumerate(self.hostDict) if x not in self.hostDict[:y]]
        except:
            self.hostDict = []

        self.hostBlackList = []

        self.hostmyDict = ['uploadrocket.net','userscloud','alfafile','.avi','.mkv','.mov','.mp4','.xvid','.divx','oboom', 'rapidgator', 'rg.to',  'uploaded', 'ul.to', 'filefactory', 'nitroflare', 'turbobit', '1fichier','uptobox', '1fich', 'uploadrocket','uploading','hugefiles', 'uploaded' , 'clicknupload' , 'rlsbb.com' , 'nfo.rlsbb.com']
        self.hostprDict = self.hostDict + self.hostmyDict
        self.hostcapDict = ['hugefiles.net', 'kingfiles.net', 'openload.io', 'openload.co', 'oload.tv', 'thevideo.me', 'vidup.me', 'streamin.to', 'torba.se', 'openload']
        self.blacklist_zips = ['.zip', '.jpeg', '.img', '.jpg', '.ZIP', '.png' , '.sub', '.srt']

        self.hostblockDict = []

        self.debridDict = debrid.debridDict()

    @staticmethod
    def sort_function(item):
        """
        transform items quality into a string that's sort-able
        Args:
            item: scraper link
        Returns:
            sortable quality string
        """
        if 'quality' in item[1][0]:
            quality = item[1][0]["quality"]
        else:
            quality = item[1][0]["path"]["quality"]

        if quality.startswith("1080"):
            quality = "HDa"
        elif quality.startswith("720"):
            quality = "HDb"
        elif quality.startswith("560"):
            quality = "HDc"
        elif quality == "DVD":
            quality = "HDd"
        elif quality == "HD":
            quality = "HDe"
        elif quality.startswith("480"):
            quality = "SDa"
        elif quality.startswith("360"):
            quality = "SDb"
        elif quality.startswith("SD"):
            quality = "SDc"
        return quality

	def getPremColor(self, n):
		if n == '0': n = 'ff006400'#green
		elif n == '1': n = 'fffe0000'#red
		elif n == '2': n = 'ffffff01'#yellow
		elif n == '3': n = 'ffff1494'#deeppink
		elif n == '4': n = 'ff01ffff'#cyan
		elif n == '5': n = 'ff0000fe'#blue
		elif n == '6': n = 'ffffd701'#gold
		elif n == '7': n = 'ffff00ff'#magenta
		elif n == '8': n = 'ff9acd32'#yellowgreen
		elif n == '9': n = 'ffffffff'#white
		else: n == 'ff006400'#green
		return n		  