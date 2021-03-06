# -*- coding: utf-8 -*-

import sys, xbmc

from resources.lib.modules import control
from resources.lib.modules import trakt

trakt.notification = False if control.setting('trakt.notifications') == 'false' else True
traktIndicators = trakt.getTraktIndicatorsInfo()


def getMovieIndicators(refresh=False):
	try:
		if traktIndicators is True:
			raise Exception()
		from metahandler import metahandlers
		indicators = metahandlers.MetaData()
		return indicators
	except:
		pass

	try:
		if traktIndicators is False:
			raise Exception()
		if refresh is False:
			timeout = 720
		elif trakt.getWatchedActivity() < trakt.timeoutsyncMovies():
			timeout = 720
		else:
			timeout = 0
		indicators = trakt.cachesyncMovies(timeout = timeout)
		return indicators
	except:
		pass


def getTVShowIndicators(refresh=False):
	try:
		if traktIndicators is True:
			raise Exception()

		from metahandler import metahandlers
		indicators = metahandlers.MetaData()
		return indicators
	except:
		pass

	try:
		if traktIndicators is False:
			raise Exception()
		if refresh is False:
			timeout = 720
		elif trakt.getWatchedActivity() < trakt.timeoutsyncTVShows():
			timeout = 720
		else:
			timeout = 0
		indicators = trakt.cachesyncTVShows(timeout = timeout)
		return indicators
	except:
		pass


def getSeasonIndicators(imdb, refresh=False):
	try:
		if traktIndicators is True:
			raise Exception()
		from metahandler import metahandlers
		indicators = metahandlers.MetaData()
		return indicators
	except:
		pass

	try:
		if traktIndicators is False:
			raise Exception()
		if refresh is False:
			timeout = 720
		elif trakt.getWatchedActivity() < trakt.timeoutsyncSeason(imdb = imdb):
			timeout = 720
		else:
			timeout = 0
		indicators = trakt.cachesyncSeason(imdb = imdb, timeout = timeout)
		return indicators
	except:
		pass


def getMovieOverlay(indicators, imdb):
	try:
		try:
			playcount = indicators._get_watched('movie', imdb, '', '')
			return str(playcount)
		except:
			playcount = [i for i in indicators if i == imdb]
			playcount = 7 if len(playcount) > 0 else 6
			return str(playcount)
	except:
		return '6'


def getTVShowOverlay(indicators, imdb, tvdb):
	try:
		try:
			playcount = indicators._get_watched('tvshow', imdb, '', '')
			return str(playcount)
		except:
			playcount = [i[0] for i in indicators if i[0] == tvdb and len(i[2]) >= int(i[1])]
			playcount = 7 if len(playcount) > 0 else 6
			return str(playcount)
	except:
		return '6'


def getSeasonOverlay(indicators, imdb, tvdb, season):
	try:
		try:
			playcount = indicators._get_watched('season', imdb, '', season)
			return str(playcount)
		except:
			playcount = [i for i in indicators if int(season) == int(i)]
			playcount = 7 if len(playcount) > 0 else 6
			return str(playcount)
	except:
		return '6'


def getEpisodeOverlay(indicators, imdb, tvdb, season, episode):
	try:
		try:
			playcount = indicators._get_watched_episode({'imdb_id': imdb, 'season': season, 'episode': episode, 'premiered': ''})
			return str(playcount)
		except:
			playcount = [i[2] for i in indicators if i[0] == tvdb]
			playcount = playcount[0] if len(playcount) > 0 else []
			playcount = [i for i in playcount if int(season) == int(i[0]) and int(episode) == int(i[1])]
			playcount = 7 if len(playcount) > 0 else 6
			return str(playcount)
	except:
		return '6'


def getShowCount(indicators, imdb, tvdb, limit = False):
	try:
		if traktIndicators is False:
			raise Exception()
		result = trakt.showCount(imdb)

		if limit and result:
			result['unwatched'] = min(99, result['unwatched'])

		return result
	except:

		try:
			for indicator in indicators:
				if indicator[0] == tvdb:
					total = indicator[1]
					watched = len(indicator[2])
					unwatched = total - watched
					if limit:
						unwatched = min(99, unwatched)

					return {'total': total, 'watched': watched, 'unwatched': unwatched}
		except:
			pass
		return None


def getSeasonCount(imdb, season = None, season_special = False, limit = False):
	try:
		if traktIndicators is False:
			raise Exception()

		result = trakt.seasonCount(imdb)

		if season is None:
			if limit and result:
				for i in range(len(result)):
					result[i]['unwatched'] = min(99, result[i]['unwatched'])
			return result
		else:
			if control.setting('tv.specials') == 'true' and season_special is True:
				result = result[int(season)]
			else:
				result = result[int(season) - 1]

				# if int(season) > 1:
					# result = result[int(season) - 1]
				# else:
					# result = result[int(season)]
			if limit:
				result['unwatched'] = min(99, result['unwatched'])
			return result
	except:
		pass
	return None


def markMovieDuringPlayback(imdb, watched):
	try:
		if traktIndicators is False:
			raise Exception()

		if int(watched) == 7:
			trakt.markMovieAsWatched(imdb)
		else:
			trakt.markMovieAsNotWatched(imdb)

		trakt.cachesyncMovies()

		# if trakt.getTraktAddonMovieInfo() is True:
			# log_utils.log('trakt.getTraktAddonMovieInfo = True', __name__, log_utils.LOGDEBUG)
			# trakt.markMovieAsNotWatched(imdb)
	except:
		pass

	try:
		from metahandler import metahandlers
		metaget = metahandlers.MetaData()
		metaget.get_meta('movie', name='', imdb_id=imdb)
		metaget.change_watched('movie', name='', imdb_id=imdb, watched=int(watched))
	except:
		pass


def markEpisodeDuringPlayback(imdb, tvdb, season, episode, watched):
	try:
		if traktIndicators is False:
			raise Exception()

		if int(watched) == 7:
			trakt.markEpisodeAsWatched(imdb, tvdb, season, episode)
		else:
			trakt.markEpisodeAsNotWatched(imdb, tvdb, season, episode)

		trakt.cachesyncTVShows()

		# if trakt.getTraktAddonEpisodeInfo() is True:
			# log_utils.log('trakt.getTraktAddonEpisodeInfo = True', __name__, log_utils.LOGDEBUG)
			# trakt.markEpisodeAsNotWatched(imdb, tvdb, season, episode)
	except:
		pass

	try:
		from metahandler import metahandlers
		metaget = metahandlers.MetaData()
		metaget.get_meta('tvshow', name='', imdb_id=imdb)
		metaget.get_episode_meta('', imdb_id=imdb, season=season, episode=episode)
		metaget.change_watched('episode', '', imdb_id=imdb, season=season, episode=episode, watched=int(watched))
	except:
		pass


def movies(imdb, watched):
	try:
		if traktIndicators is False:
			raise Exception()

		if int(watched) == 7:
			trakt.watch(imdb=imdb, refresh=True, notification=trakt.notification)
		else:
			trakt.unwatch(imdb=imdb, refresh=True, notification=trakt.notification)
	except:
		pass

	try:
		from metahandler import metahandlers
		metaget = metahandlers.MetaData()
		metaget.get_meta('movie', name='', imdb_id=imdb)
		metaget.change_watched('movie', name='', imdb_id=imdb, watched=int(watched))

		if traktIndicators is False:
			control.refresh()
	except:
		pass


def episodes(imdb, tvdb, season, episode, watched):
	try:
		if traktIndicators is False:
			raise Exception()

		if int(watched) == 7:
			trakt.watch(imdb=imdb, tvdb=tvdb, season=season, episode=episode, refresh=True, notification=trakt.notification)
		else:
			trakt.unwatch(imdb=imdb, tvdb=tvdb, season=season, episode=episode, refresh=True, notification=trakt.notification)
	except:
		pass

	try:
		from metahandler import metahandlers
		metaget = metahandlers.MetaData()
		metaget.get_meta('tvshow', name='', imdb_id=imdb)
		metaget.get_episode_meta('', imdb_id=imdb, season=season, episode=episode)
		metaget.change_watched('episode', '', imdb_id=imdb, season=season, episode=episode, watched=int(watched))

		if traktIndicators is False:
			tvshowsUpdate(imdb=imdb, tvdb=tvdb)
	except:
		pass


def seasons(tvshowtitle, imdb, tvdb, season, watched):
	tvshows(tvshowtitle=tvshowtitle, imdb=imdb, tvdb=tvdb, season=season, watched=watched)


def tvshows(tvshowtitle, imdb, tvdb, season, watched):
	watched = int(watched)

	try:
		if traktIndicators is True:
			raise Exception()

		from metahandler import metahandlers
		from resources.lib.menus import episodes

		name = control.addonInfo('name')

		dialog = control.progressDialogBG
		dialog.create(str(name), str(tvshowtitle))
		dialog.update(0, str(name), str(tvshowtitle))

		metaget = metahandlers.MetaData()
		metaget.get_meta('tvshow', name='', imdb_id=imdb)

		items = episodes.Episodes().get(tvshowtitle, '0', imdb, tvdb, idx = False)

		for i in range(len(items)):
			items[i]['season'] = int(items[i]['season'])
			items[i]['episode'] = int(items[i]['episode'])

		try:
			items = [i for i in items if int('%01d' % int(season)) == int('%01d' % i['season'])]
		except:
			pass

		items = [{'label': '%s S%02dE%02d' % (tvshowtitle, i['season'], i['episode']), 'season': int('%01d' % i['season']), 'episode': int('%01d' % i['episode'])} for i in items]

		count = len(items)

		for i in range(count):
			if xbmc.abortRequested is True:
				return sys.exit()
			dialog.update(int(100.0 / count * i), str(name), str(items[i]['label']))
			season, episode = items[i]['season'], items[i]['episode']
			metaget.get_episode_meta('', imdb_id = imdb, season = season, episode = episode)
			metaget.change_watched('episode', '', imdb_id = imdb, season = season, episode = episode, watched = watched)

		tvshowsUpdate(imdb = imdb, tvdb = tvdb)

		try:
			dialog.close()
		except:
			pass
	except:
		try:
			dialog.close()
		except:
			pass

	try:
		if traktIndicators is False:
			raise Exception()
		if watched == 7:
			trakt.watch(imdb = imdb, tvdb = tvdb, season = season, refresh = True, notification = trakt.notification)
		else:
			trakt.unwatch(imdb = imdb, tvdb = tvdb, season = season, refresh = True, notification = trakt.notification)
	except:
		# import traceback
		# traceback.print_exc()
		# pass
		from resources.lib.modules import log_utils
		log_utils.error()


def tvshowsUpdate(imdb, tvdb):
	try:
		if traktIndicators is True:
			raise Exception()

		from metahandler import metahandlers
		from resources.lib.menus import episodes

		name = control.addonInfo('name')
		metaget = metahandlers.MetaData()
		metaget.get_meta('tvshow', name='', imdb_id=imdb)

		items = episodes.Episodes().get('', '0', imdb, tvdb, idx=False)

		for i in range(len(items)):
			items[i]['season'] = int(items[i]['season'])
			items[i]['episode'] = int(items[i]['episode'])

		seasons = {}

		for i in items:
			if i['season'] not in seasons:
				seasons[i['season']] = []
			seasons[i['season']].append(i)

		countSeason = 0

		metaget.get_seasons('', imdb, seasons.keys()) # Must be called to initialize the database.

		for key, value in seasons.iteritems():
			countEpisode = 0
			for i in value:
				countEpisode += int(metaget._get_watched_episode({'imdb_id': i['imdb'], 'season': i['season'], 'episode': i['episode'], 'premiered': ''}) == 7)
			countSeason += int(countEpisode == len(value))
			metaget.change_watched('season', '', imdb_id = imdb, season = key, watched = 7 if countEpisode == len(value) else 6)
		metaget.change_watched('tvshow', '', imdb_id = imdb, watched = 7 if countSeason == len(seasons.keys()) else 6)
	except:
		# import traceback
		# traceback.print_exc()
		from resources.lib.modules import log_utils
		log_utils.error()
	control.refresh()
