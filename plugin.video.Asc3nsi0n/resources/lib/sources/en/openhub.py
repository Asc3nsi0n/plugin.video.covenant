# -*- coding: utf-8 -*-

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['tinydl.com']
        self.base_link = 'http://tinydl.com'
        self.search_link = '/search/%s/feed/rss2/'


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

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            title = (title).replace(' ','+')
			
            url   = 'http://openhub.pw/?s='+title.lower()

            open  = client.request(url)
		
            match = re.compile('<div class="result-item">(.+?)</article>',re.DOTALL).findall(open)[0]
			
            url   = re.compile('href="(.+?)"').findall(match)[0]
            year  = re.compile('<span class="year">(.+?)<').findall(match)[0]
            if title in match.lower():
			
				open = client.request(url)
				
				url  = re.compile('iframe class.+?src="(.+?)"').findall(open)[0]
				qual = re.compile('<span class="qualityx">(.+?)<').findall(open)[0]
				
				if '720' in qual or 'hd' in qual or 'HD' in qual:
					qual = 'HD'
				elif '1080' in qual:
					qual = '1080p'
				else:
					qual = 'SD'
                    sources.append({'source': 'openload', 'quality': qual, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


