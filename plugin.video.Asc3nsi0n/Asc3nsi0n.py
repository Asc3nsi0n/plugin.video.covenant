# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Provider: Asc3nsi0n
# Addon id: plugin.video.Asc3nsi0n
# Addon Provider: MuadDib

import urlparse,sys,os,urllib,xbmcgui,xbmc,xbmcaddon
from resources.lib.modules import log_utils

dialog = xbmcgui.Dialog()

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

subid = params.get('subid')

docu_category = params.get('docuCat')

docu_watch = params.get('docuPlay')

podcast_show = params.get('podcastshow')

podcast_cat = params.get('podcastlist')

podcast_cats = params.get('podcastcategories')

podcast_episode = params.get('podcastepisode')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0","1") else 0

if action == None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()

elif action == 'newsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().news()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'moviePlaylistNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movieplaylists()

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'libraryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'clearCacheSearch':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheSearch()

elif action == 'clearAllCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheAll()

elif action == 'clearMetaCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheMeta()
    
elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'movieSearchnew':
    from resources.lib.indexers import movies
    movies.movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(name)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieMosts':
	from resources.lib.indexers import navigator
	navigator.navigator().movieMosts()

elif action == 'movieBests':
	from resources.lib.indexers import navigator
	navigator.navigator().movieBests()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvSearchnew':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(name)
    
elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvshowMosts':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshowMosts()

elif action == 'tvReviews':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'movieReviews':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url, windowedtrailer)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'youtubekids':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'fitness':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'legends':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'podcastNavigator':
    from resources.lib.indexers import podcast
    podcast.podcast().root()

elif action == 'podcastOne':
    from resources.lib.indexers import podcast
    if not podcast_show == None:
        podcast.podcast().pco_show(podcast_show)
    elif not podcast_cat == None:
        podcast.podcast().pco_cat(podcast_cat)
    elif not podcast_cats == None:
        podcast.podcast().pcocats_list()
    elif not podcast_episode == None:
        podcast.podcast().podcast_play(action, podcast_episode)
    else:
        podcast.podcast().pco_root()

elif action == 'docuHeaven':
    from resources.lib.indexers import docu
    if not docu_category == None:
        docu.documentary().docu_list(docu_category)
    elif not docu_watch == None:
        docu.documentary().docu_play(docu_watch)
    else:
        docu.documentary().root()

elif action == 'podbay':
    from resources.lib.indexers import podcast
    if not podcast_show == None:
        podcast.podcast().pb_show(podcast_show)
    elif not podcast_cat == None:
        podcast.podcast().pb_cat(podcast_cat)
    elif not podcast_cats == None:
        podcast.podcast().pb_root()
    elif not podcast_episode == None:
        podcast.podcast().podcast_play(action, podcast_episode)
    else:
        podcast.podcast().pb_root()

elif action == 'sectionItem':
    pass # Placeholder. This is a non-clickable menu item for notes, etc.

elif action == 'play':
	from resources.lib.modules import control
	from resources.lib.modules import playmenu
	#Uni-Scrapers
	if control.setting('scraper.default') == '0':
		playmenu.UniScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	#Internal-Scrapers
	if control.setting('scraper.default') == '1':
		playmenu.IntScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	#Lambda-Scrapers
	if control.setting('scraper.default') == '2':
		playmenu.LambScrapers(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	#Prompt-Scrapers
	if control.setting('scraper.default') == '3':
		#yesno
		if control.setting('scraper.dialog') == '0':
			playmenu.ScrDialog0(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		#select
		if control.setting('scraper.dialog') == '1':
			playmenu.ScrDialog1(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		#custom
		if control.setting('scraper.dialog') == '2':
			playmenu.ScrDialog2(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == "show" and p == "tvshowtitle":
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try: control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        elif rtype == "episode":
            try: control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)

elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'moviesToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libmovies().silent(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'tvshowsToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libtvshows().silent(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()

elif action == 'resolveurlSettings':
	try: import resolveurl
	except: pass
	resolveurl.display_settings()

elif action == 'urlresolverSettings':
	try: import urlresolver
	except: pass
	urlresolver.display_settings()

########NEPTUNE RISING####################################

elif action == 'download2':
    from resources.lib.modules2 import sources
    sources.sources().downloadItem(name,image, source)
	
elif action == 'play2':
    from resources.lib.modules2 import control
    select = control.setting('hosts.mode')
    if select == '3' and 'plugin' in control.infoLabel('Container.PluginName'):
		from resources.lib.modules2 import sources
		sources.sources().play_dialog(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
    elif select == '4' and 'plugin' in control.infoLabel('Container.PluginName'):
		from resources.lib.modules2 import sources
		sources.sources().play_dialog_list(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
    else:
		from resources.lib.modules2 import sources										  
		sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
	
elif action == 'play_alter':
		from resources.lib.modules2 import sources
		sources.sources().play_alter(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta)

elif action == 'addItem2':
    from resources.lib.modules2 import sources
    sources.sources().addItem(title)

elif action == 'playItem2':
    from resources.lib.modules2 import sources
    sources.sources().playItem(title, source)

elif action == 'uniscrapersettings': xbmcaddon.Addon('script.module.universalscrapers').openSettings()

##########################################################

elif action == 'messagetest':
	from resources.lib.modules import message
	#RDinfoURL   = 'http://ENTERURL/realdebrid.txt'
	RDinfoLocal = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Asc3nsi0n', 'resources', 'msg', 'realdebrid.txt'))
	message.viewDialog(RDinfoLocal,'[B]What is Real Debrid ?[/B]')

#####################REGEX#########################

elif action == 'adult':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().adult()
	
elif action == 'xvideos':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().xvideos()

####################################################

elif action == 'localXML':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().localXML(url, content)

elif action == 'remoteXML':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().remoteXML(url, content)

elif action == 'Asc3nsi0nRoot':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().root()

elif action == 'ytplaylists':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().ytplaylists()

elif action == 'animation':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().kidsplace()

elif action == 'kidsplace':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().kidsplace()

elif action == 'kidspopular':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().kidspopular()

elif action == 'directory':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().get(url)

elif action == 'parental':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().parental_controls()

elif action == 'qdirectory':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().youtube(url, action)

elif action == 'play3':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.player().play(url)

elif action == 'browser':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import Asc3nsi0n
    Asc3nsi0n.indexer().delSearch()

################################################

elif action == 'sports':
	from resources.lib.modules import sports
	sports.clearicons()
	from resources.lib.indexers import navigator
	navigator.navigator().sports()

elif action == 'nhlgames':
	from resources.lib.modules import sports
	sports.nhlgames()

elif action == 'mlbgames':
	from resources.lib.modules import sports
	sports.mlbgames()

elif action == 'feeds':
	from resources.lib.modules import sports
	dategames = sports.games(params['date'],params['provider'])
	gameDict = dict(map(lambda g: (g.id, g), dategames))
	sports.listfeeds(gameDict[int(params['game'])], params['date'],params['provider'])

elif action == 'playsports':
	from resources.lib.modules import control
	control.busy()
	from resources.lib.modules import sports
	sports.playgame(params['date'],params['feedId'],params['provider'],params['state'])

elif action == 'listyears':
	from resources.lib.modules import sports
	sports.listyears(params['provider'])

elif action == 'listmonths':
	from resources.lib.modules import sports
	sports.listmonths(params['year'],params['provider'])

elif action == 'listdays':
	from resources.lib.modules import sports
	sports.listdays(params['year'],params['month'],params['provider'])

elif action == 'listgames':
	from resources.lib.modules import sports
	sports.listgames("%d-%02d-%02d" % (int(params['year']),int(params['month']),int(params['day'])),params['provider'])

elif action == 'listgamesyest':
	from resources.lib.modules import sports
	from resources.lib.modules import sports_utils
	sports.listgames(sports_utils.yesterday().strftime("%Y-%m-%d"),params['provider'],True)

elif action == 'listtodaysgames':
	from resources.lib.modules import sports
	from resources.lib.modules import sports_utils
	sports.listgames(sports_utils.today().strftime("%Y-%m-%d"),params['provider'],True)

##########################################################################################

elif action == 'speedtest':
	from resources.lib.modules import speedtest
	speedtest.speedtest()
