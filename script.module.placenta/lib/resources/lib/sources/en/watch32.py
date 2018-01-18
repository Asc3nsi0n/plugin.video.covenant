# NEEDS FIXING

# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: MuadDib

import re,json,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watch32hd.co']
        self.base_link = 'https://watch32hd.co'
        self.search_link = '/watch?v=%s_%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title'] ; year = data['year']
            h = {'User-Agent': client.randomagent()}
            v = '%s_%s' % (cleantitle.geturl(title).replace('-', '_'), year)

            url = '/watch?v=%s' % v
            url = urlparse.urljoin(self.base_link, url)

            html = client.request(url, headers=h, referer=url)
            varid = re.compile('var frame_url = "(.+?)"',re.DOTALL).findall(html)[0].replace('/embed/','/streamdrive/info/')

            res_chk = re.compile('class="title"><h1>(.+?)</h1>',re.DOTALL).findall(html)[0]
            varid = 'http:'+varid
            holder = client.request(varid, headers=h)
            links = re.compile('"src":"(.+?)"',re.DOTALL).findall(holder)
                        
            for vid_url in links:
                vid_url = vid_url.replace('\\','')
                vid_url = urlparse.urljoin('https://vidlink.org', vid_url)
                quality,info = source_utils.get_release_quality(res_chk, vid_url)
                sources.append({'source': 'VidLink', 'quality': str(quality), 'language': 'en', 'url': vid_url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return directstream.googlepass(url)


