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
# Addon Provider: Mr.Blamo

import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['drama4u.us']
        self.base_link = 'http://drama4u.us'
        self.search_link = '/search?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases))
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases))
            return self.__get_episode_link(url)
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases))
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return self.__get_episode_link(url, episode)

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'tab-pane'})
            r = dom_parser.parse_dom(r, 'iframe', req='src')
            r = [i.attrs['src'] for i in r]

            for i in r:
                try:
                    if 'drama4u' in i or 'k-vid' in i:
                        r = client.request(i, referer=url)
                        r = re.findall('''var\s*source\s*=\s*\[({.*?})\]\s*;''', r)[0]

                        i = [(match[1], match[0]) for match in re.findall('''["']?label\s*["']?\s*[:=]\s*["']?([^"',]+)["']?(?:[^}\]]+)["']?\s*file\s*["']?\s*[:=,]?\s*["']([^"']+)''', r, re.DOTALL)]
                        i += [(match[0], match[1]) for match in re.findall('''["']?\s*file\s*["']?\s*[:=,]?\s*["']([^"']+)(?:[^}>\]]+)["']?\s*label\s*["']?\s*[:=]\s*["']?([^"',]+)''', r, re.DOTALL)]
                        r = [(x[0].replace('\/', '/'), source_utils.label_to_quality(x[1])) for x in i]

                        for u, q in list(set(r)):
                            try:
                                tag = directstream.googletag(u)
                                if tag:
                                    sources.append({'source': 'gvideo', 'quality': tag[0].get('quality', 'SD'), 'language': 'ko', 'url': u, 'direct': True, 'debridonly': False})
                                else:
                                    sources.append({'source': 'CDN', 'quality': q, 'language': 'ko', 'url': u, 'direct': True, 'debridonly': False})
                            except:
                                pass
                    else:
                        valid, host = source_utils.is_host_valid(i, hostDict)
                        if not valid: continue

                        sources.append({'source': host, 'quality': 'SD', 'language': 'ko', 'url': i, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.query(titles[0]))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'div', attrs={'id': 'container-search'})
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'movie-cat'})
            r = dom_parser.parse_dom(r, 'h4', attrs={'class': 'title'})
            r = dom_parser.parse_dom(r, 'a', req=['title', 'href'])
            r = [(i.attrs['href'], i.attrs['title']) for i in r]
            r = [(i[0]) for i in r if cleantitle.get(i[1]) in t][0]

            return source_utils.strip_domain(r)
        except:
            return

    def __get_episode_link(self, url, episode='1'):
        try:
            if not url:
                return

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            r = dom_parser.parse_dom(r, 'div', attrs={'id': 'list-espisode'})
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'movie-item-espisode'})
            r = dom_parser.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href'], i.content) for i in r]
            r = [(i[0], re.findall('EP\s*(\d+)$', i[1])) for i in r]
            r = [i[0] for i in r if i[1] and int(i[1][0]) == int(episode)][0]

            return source_utils.strip_domain(r)
        except:
            return

