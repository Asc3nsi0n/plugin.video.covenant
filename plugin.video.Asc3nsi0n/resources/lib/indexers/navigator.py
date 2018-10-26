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

import os, base64, sys, urllib2, urlparse
import xbmc, xbmcaddon, xbmcgui

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1])
artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()
traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
	ADDON_ID      = xbmcaddon.Addon().getAddonInfo('id')
	HOMEPATH      = xbmc.translatePath('special://home/')
	ADDONSPATH    = os.path.join(HOMEPATH, 'addons')
	THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
	NEWSFILE      = base64.b64decode(b'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L2ZBaGE5RVRD')
	LOCALNEWS     = os.path.join(THISADDONPATH, 'whatsnew.txt')

	def root(self):
		#self.addDirectoryItem('[COLOR=blue]News and Updates[/COLOR]', 'newsNavigator', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
		self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')

		if not control.setting('lists.widget') == '0':
			self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
			self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

		#if not control.setting('movie.widget') == '0':
		#    self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

		#if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
		#    self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

		if self.getMenuEnabled('navi.kidscorner') == True:
			self.addDirectoryItem(32610, 'kidsplace', 'kidsplace.png', 'DefaultMovies.png')

		if self.getMenuEnabled('navi.ytplaylists') == True:
			self.addDirectoryItem(33747, 'ytplaylists', 'youtube.png', 'DefaultMovies.png')

		if self.getMenuEnabled('navi.docu') == True:
			self.addDirectoryItem(32631, 'docuHeaven', 'movies.png', 'DefaultMovies.png')

		if self.getMenuEnabled('navi.sports') == True:
			self.addDirectoryItem(33732, 'sports', 'sports.png', 'DefaultMovies.png')

		if self.getMenuEnabled('navi.adult') == True:
			self.addDirectoryItem(33733, 'adult', 'xxx.png', 'DefaultMovies.png')

		#if self.getMenuEnabled('navi.fitness') == True:
		#    self.addDirectoryItem(32611, 'fitness', 'fitness.png', 'DefaultMovies.png')

		#if self.getMenuEnabled('navi.legends') == True:
		#    self.addDirectoryItem(32612, 'legends', 'legends.png', 'DefaultMovies.png')

		#if self.getMenuEnabled('navi.podcasts') == True:
		#    self.addDirectoryItem(32620, 'podcastNavigator', 'podcast.png', 'DefaultVideoPlaylists.png')

		self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

		downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
		if downloads == True:
			self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

		self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')

		self.endDirectory()

	def getMenuEnabled(self, menu_title):
		is_enabled = control.setting(menu_title).strip()
		if (is_enabled == '' or is_enabled == 'false'): return False
		return True

	#######################################################################
	# News and Update Code
	def news(self):
			message=self.open_news_url(self.NEWSFILE)
			r = open(self.LOCALNEWS)
			compfile = r.read()       
			if len(message)>1:
					if compfile == message:pass
					else:
							text_file = open(self.LOCALNEWS, "w")
							text_file.write(message)
							text_file.close()
							compfile = message
			self.showText('[B][COLOR springgreen]Latest Updates and Information[/COLOR][/B]', compfile)
		
	def open_news_url(self, url):
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'klopp')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			print link
			return link

	def showText(self, heading, text):
		id = 10147
		xbmc.executebuiltin('ActivateWindow(%d)' % id)
		xbmc.sleep(500)
		win = xbmcgui.Window(id)
		retry = 50
		while (retry > 0):
			try:
				xbmc.sleep(10)
				retry -= 1
				win.getControl(1).setLabel(heading)
				win.getControl(5).setText(text)
				quit()
				return
			except: pass
	#######################################################################


	def movies(self, lite=False):
		if self.getMenuEnabled('navi.movietrending') == True:
			self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
		if self.getMenuEnabled('navi.moviepopular') == True:
			self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.moviewidget') == True:
			self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
		if self.getMenuEnabled('navi.moviegenre') == True:
			self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.moviepl') == True:
			self.addDirectoryItem(33738, 'moviePlaylistNavigator', 'imdb.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.movieviews') == True:
			#self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
			self.addDirectoryItem(33744, 'movieMosts', 'most-voted.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.moviebests') == True:
			self.addDirectoryItem(33746, 'movieBests', 'bests.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.movieoscars') == True:
			self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')	
		if self.getMenuEnabled('navi.movieboxoffice') == True:
			self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.movietheaters') == True:
			self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
		if self.getMenuEnabled('navi.movieyears') == True:
			self.addDirectoryItem(32012, 'movieYears', 'calendar.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.moviecerts') == True:
			self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
		if not control.setting('lists.widget') == '0':
			self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
		if self.getMenuEnabled('navi.moviereview') == True:
			self.addDirectoryItem(32623, 'movieReviews', 'reviews.png', 'DefaultMovies.png')
		if self.getMenuEnabled('navi.movielanguages') == True:
			self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')

		self.addDirectoryItem(32013, 'moviePersons', 'people.png', 'DefaultMovies.png')
		self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
		self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

		self.endDirectory()


	def mymovies(self, lite=False):
		self.accountCheck()

		if traktCredentials == True and imdbCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
			self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

		elif traktCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

		elif imdbCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
			self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

		if traktCredentials == True:
			self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

		elif imdbCredentials == True:
			self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

		if traktIndicators == True:
			self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

		self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

		if lite == False:
			self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
			self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
			self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

		self.endDirectory()


	def movieplaylists(self, lite=False):
		self.addDirectoryItem('[B]Disney & Pixar[/B]', 'movies&url=disney', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Kids & Animation[/B]', 'movies&url=animation', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]DC Universe[/B]', 'movies&url=dc', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Marvel Universe[/B]', 'movies&url=marvel', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Greatest Movies: 2000-2017[/B]', 'movies&url=imdb1', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top 1000 Movies[/B]', 'movies&url=thousand', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('                                        ', '', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('80s Movies', 'movies&url=eighties', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Alien Invasion', 'movies&url=imdb13', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Alchoholic', 'movies&url=imdb50', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Anime', 'movies&url=anime', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Artificial Intelligence', 'movies&url=imdb11', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Artists , Painters , Writers', 'movies&url=imdb46', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Avant Garde', 'movies&url=avant', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Based On A True Story', 'movies&url=true', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Based on a True Story 2', 'movies&url=imdb37', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Based In One Room', 'movies&url=imdb18', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Biker', 'movies&url=biker', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Biographical', 'movies&url=imdb53', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('B Movies', 'movies&url=bmovie', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Breaking The Fourth Wall', 'movies&url=breaking', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Business', 'movies&url=business', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Capers', 'movies&url=caper', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Car Chases', 'movies&url=car', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Character Study', 'movies&url=char', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Chick Flix', 'movies&url=chick', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Christmas', 'movies&url=xmass', control.addonIcon(), 'season.jpg')
		self.addDirectoryItem('Coming to Age', 'movies&url=coming', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Competition', 'movies&url=competition', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Conspiracy', 'movies&url=imdb16', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Contract Killers', 'movies&url=imdb14', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Courtroom', 'movies&url=imdb35', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Cult', 'movies&url=cult', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Cult 2', 'movies&url=imdb9', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Cyberpunk', 'movies&url=cyber', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Disaster & Apocalyptic', 'movies&url=imdb27', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Drug Addiction', 'movies&url=drugs', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Drug Addiction 2', 'movies&url=imdb43', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Dystopia', 'movies&url=dystopia', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Easter', 'movies&url=easter', control.addonIcon(), 'season.jpg')
		self.addDirectoryItem('Epic', 'movies&url=epic', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Espionage', 'movies&url=espionage', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Experimental', 'movies&url=expiremental', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Existential', 'movies&url=Existential', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Fairy Tale', 'movies&url=fairytale', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Farce', 'movies&url=farce', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Father - Son', 'movies&url=imdb36', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Femme Fatale', 'movies&url=femme', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Futuristic', 'movies&url=futuristic', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Gangster', 'movies&url=imdb39', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Halloween', 'movies&url=halloween', control.addonIcon(), 'season.jpg')
		self.addDirectoryItem('Heist', 'movies&url=heist', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Heist Caper', 'movies&url=imdb10', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Heists, Cons, Scams & Robbers', 'movies&url=imdb31', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Heroic Bloodshed', 'movies&url=imdb15', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('High School', 'movies&url=highschool', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Horror Remakes', 'movies&url=remakes', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Horror Series', 'movies&url=imdb2', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Horror Of The Skull Posters', 'movies&url=imdb3', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Inspirational', 'movies&url=imdb20', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('James Bond', 'movies&url=bond', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Kidnapping', 'movies&url=kidnapped', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Kung Fu', 'movies&url=kungfu', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Love', 'movies&url=imdb47', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Man Vs. Nature', 'movies&url=imdb38', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Mental, Physical Illness and Disability Movies', 'movies&url=imdb29', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Monster', 'movies&url=monster', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Motivational', 'movies&url=imdb26', control.addonIcon(), 'DefaultMovies.png')
		#self.addDirectoryItem('Movie Box Sets', 'movies&url=box', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Movie Clones', 'movies&url=imdb22', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Movies For Intelligent People', 'movies&url=imdb19', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Movie Loners', 'movies&url=loners', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Movies & Racism', 'movies&url=racist', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Music or Musical', 'movies&url=imdb28', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Neo Noir', 'movies&url=neo', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('New Years', 'movies&url=newyear', control.addonIcon(), 'season.jpg')
		self.addDirectoryItem('Old Age', 'movies&url=imdb41', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Parenthood', 'movies&url=parenthood', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Parody', 'movies&url=parody', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Post Apocalypse', 'movies&url=apocalypse', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Puff Puff Pass', 'movies&url=imdb45', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Prison & Escape', 'movies&url=imdb34', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Private Eye', 'movies&url=private', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Remakes', 'movies&url=remake', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Revenge', 'movies&url=imdb25', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Road Movies', 'movies&url=road', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Road Trip & Travel', 'movies&url=imdb32', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Robots', 'movies&url=robot', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Satire', 'movies&url=satire', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Schizophrenia', 'movies&url=schiz', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Serial Killers', 'movies&url=serial', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Serial Killers 2', 'movies&url=imdb42', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Shocking', 'movies&url=imdb52', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Slasher', 'movies&url=slasher', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Sleeper Hits', 'movies&url=sleeper', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Sleeper Hits 2', 'movies&url=imdb8', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Smut and Trash', 'movies&url=imdb24', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Spiritual', 'movies&url=spiritual', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Spoofs', 'movies&url=spoof', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Spy', 'movies&url=imdb33', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Star Wars', 'movies&url=star', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Steampunk', 'movies&url=steampunk', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Superheros', 'movies&url=superhero', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Stephen King and Adaptations', 'movies&url=imdb12', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Suicide', 'movies&url=imdb49', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Supernatural', 'movies&url=supernatural', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Teach You a Thing or 2', 'movies&url=imdb54', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Tech Geeks', 'movies&url=imdb21', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Tech Noir', 'movies&url=tech', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Teenage', 'movies&url=imdb40', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Thanksgiving', 'movies&url=thanx', control.addonIcon(), 'season.jpg')
		self.addDirectoryItem('Time Travel', 'movies&url=time', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Time Travel 2', 'movies&url=imdb44', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Twist Ending', 'movies&url=imdb30', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Underrated', 'movies&url=imdb23', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Vampires', 'movies&url=vampire', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Video Games', 'movies&url=imdb51', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Virtual Reality', 'movies&url=vr', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Wilhelm Scream', 'movies&url=wilhelm', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Winter', 'movies&url=imdb48', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('Zombies', 'movies&url=zombie', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('                                        ', '', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Action Movies 00-17', 'movies&url=action', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Action Movies 60-99', 'movies&url=action2', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Animated 00-17', 'movies&url=animated', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Cop Movies', 'movies&url=cop', control.addonIcon(), 'DefaultMovies.png')		
		self.addDirectoryItem('[B]Top[/B] Documentaries 00-17', 'movies&url=docs', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Gangster Movies', 'movies&url=gangster', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Horror Movies', 'movies&url=horror', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Kung Fu', 'movies&url=imdb17', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Romantic Movies', 'movies&url=romance', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Top[/B] Satirical Movies', 'movies&url=imdb4', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('                                        ', '', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Greatest[/B] Horror Films of All Time', 'movies&url=horror', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Greatest[/B] Political Movies', 'movies&url=political', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Greatest[/B] Sci-Fi Films of All Time', 'movies&url=scifi', control.addonIcon(), 'DefaultMovies.png')
		self.addDirectoryItem('[B]Greatest[/B] Westerns of All Time', 'movies&url=western', control.addonIcon(), 'DefaultMovies.png')		
		self.addDirectoryItem('[B]Greatest[/B] War Movies', 'movies&url=war', control.addonIcon(), 'DefaultMovies.png')
		#self.addDirectoryItem('[B]Greatest[/B] Woman Directed Movies', 'movies&url=women', control.addonIcon(), 'DefaultMovies.png')

		self.endDirectory(file=True)
		
		
	def movieBests(self, lite=False):
		self.addDirectoryItem('[B]100 Best[/B] All Time', 'movies&url=besgreatest', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Action', 'movies&url=besaction', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Adventure', 'movies&url=besadventure', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Biography', 'movies&url=besbiography', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Comedy', 'movies&url=bescomedy', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Crime', 'movies&url=bescrime', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Drama', 'movies&url=besdrama', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Family', 'movies&url=besfamily', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Fantasy', 'movies&url=besfantasy', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Hindi', 'movies&url=beshindi', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] History', 'movies&url=beshistory', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Musical', 'movies&url=besmusical', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Mysteries', 'movies&url=besmystery', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Romance', 'movies&url=besromance', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Sports', 'movies&url=bessports', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Thrillers', 'movies&url=besthriller', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] Urban', 'movies&url=besurban', 'bests.png', 'DefaultMovies.png')
		self.addDirectoryItem('[B]100 Best[/B] War', 'movies&url=beswar', 'bests.png', 'DefaultMovies.png')

		self.endDirectory(file=True)


	def movieMosts(self, lite=False):
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] This Week', 'movies&url=played1', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] This Month', 'movies&url=played2', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] This Year', 'movies&url=played3', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] All Time', 'movies&url=played4', 'most-voted.png', 'DefaultMovies.png')
		#self.addDirectoryItem('                                        ', '', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] This Week', 'movies&url=collected1', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] This Month', 'movies&url=collected2', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] This Year', 'movies&url=collected3', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] All Time', 'movies&url=collected4', 'most-voted.png', 'DefaultMovies.png')
		#self.addDirectoryItem('                                        ', '', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] This Week', 'movies&url=watched1', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] This Month', 'movies&url=watched2', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] This Year', 'movies&url=watched3', 'most-voted.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] All Time', 'movies&url=watched4', 'most-voted.png', 'DefaultMovies.png')

		self.endDirectory(file=True)


	def tvshows(self, lite=False):
		if self.getMenuEnabled('navi.tvTrending') == True:
			self.addDirectoryItem(32017, 'tvshows&url=trending', 'people-watching.png', 'DefaultRecentlyAddedEpisodes.png')
		if self.getMenuEnabled('navi.tvPopular') == True:
			self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvGenres') == True:
			self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvRating') == True:
			self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvViews') == True:
			#self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
			self.addDirectoryItem(33745, 'tvshowMosts', 'most-voted.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvNetworks') == True:
			self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvCertificates') == True:
			self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvAiring') == True:
			self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvActive') == True:
			self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvPremier') == True:
			self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvAdded') == True:
			self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
		if not control.setting('lists.widget') == '0':
			self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')
		if self.getMenuEnabled('navi.tvCalendar') == True:
			self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')
		if self.getMenuEnabled('navi.tvReviews') == True:
			self.addDirectoryItem(32623, 'tvReviews', 'reviews.png', 'DefaultTVShows.png')
		if self.getMenuEnabled('navi.tvLanguages') == True:
			self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
		self.addDirectoryItem(32013, 'tvPersons', 'people.png', 'DefaultTVShows.png')
		self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
		self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

		self.endDirectory()


	def mytvshows(self, lite=False):
		self.accountCheck()

		if traktCredentials == True and imdbCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
			self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

		elif traktCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

		elif imdbCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

		if traktCredentials == True:
			self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

		elif imdbCredentials == True:
			self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

		if traktIndicators == True:
			self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
			self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
			self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

		self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

		if traktCredentials == True:
			self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

		if lite == False:
			self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

		self.endDirectory()


	def tvshowMosts(self):
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] This Week', 'tvshows&url=played1', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] This Month', 'tvshows&url=played2', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] This Year', 'tvshows&url=played3', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR green]Played[/COLOR][/B] All Time', 'tvshows&url=played4', 'most-voted.png', 'DefaultTVShows.png')
		#self.addDirectoryItem('                                        ', '', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] This Week', 'tvshows&url=collected1', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] This Month', 'tvshows&url=collected2', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] This Year', 'tvshows&url=collected3', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR gold]Collected[/COLOR][/B] All Time', 'tvshows&url=collected4', 'most-voted.png', 'DefaultTVShows.png')
		#self.addDirectoryItem('                                        ', '', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] This Week', 'tvshows&url=watched1', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] This Month', 'tvshows&url=watched2', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] This Year', 'tvshows&url=watched3', 'most-voted.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most [B][COLOR firebrick]Watched[/COLOR][/B] All Time', 'tvshows&url=watched4', 'most-voted.png', 'DefaultTVShows.png')

		self.endDirectory(file=True)


	def kidscornerWIPbak(self, lite=False):
		self.addDirectoryItem('Kids Cartoons', 'youtubekids', 'kids.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Kids/Animated Movies', 'movies&url=animation', 'kids.png', 'DefaultMovies.png')
		self.endDirectory()


	def sports(self, lite=False):
		from resources.lib.modules import sports
		from resources.lib.modules import sports_utils
		try:
			statuslabel = sports_utils.statuslabel
			statusicon = sports_utils.statusicon
		except:
			statuslabel = 'Unknown'
			statusicon = os.path.join(artPath, 'sports.png')

		self.addDirectoryItem('NHL', 'nhlgames', sports.NHLicon, 'DefaultAddonProgram.png')
		self.addDirectoryItem('MLB', 'mlbgames', sports.MLBicon, 'DefaultAddonProgram.png')
		#self.addDirectoryItem('STATUS : ' + statuslabel, 'ignore', statusicon, 'DefaultAddonProgram.png')

		self.endDirectory()


	def tools(self):
		self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32044, 'openSettings&query=4.1', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32628, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32045, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32046, 'openSettings&query=7.0', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32047, 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32048, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32604, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32614, 'clearMetaCache', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32613, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(33734, 'speedtest', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32073, 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png')
		if control.setting('resolver') == '0': self.addDirectoryItem(33735, 'resolveurlSettings', 'urlresolver.png', 'DefaultAddonProgram.png')
		if control.setting('resolver') == '1': self.addDirectoryItem(33736, 'urlresolverSettings', 'urlresolver.png', 'DefaultAddonProgram.png')

		self.endDirectory(file=True)


	def library(self):
		self.addDirectoryItem(32557, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
		self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
		self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

		if trakt.getTraktCredentialsInfo():
			self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
			self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
			self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

		self.endDirectory()


	def downloads(self):
		movie_downloads = control.setting('movie.download.path')
		tv_downloads = control.setting('tv.download.path')

		if len(control.listDir(movie_downloads)[0]) > 0:
			self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
		if len(control.listDir(tv_downloads)[0]) > 0:
			self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

		self.endDirectory(file=True)


	def search(self):
		self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
		self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
		self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
		self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

		self.endDirectory(file=True)


	def views(self):
		try:
			control.idle()

			items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

			select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

			if select == -1: return

			content = items[select][1]

			title = control.lang(32059).encode('utf-8')
			url = '%s?action=addView&content=%s' % (sys.argv[0], content)

			poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

			item = control.item(label=title)
			item.setInfo(type='Video', infoLabels = {'title': title})
			item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
			item.setProperty('Fanart_Image', fanart)

			control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
			control.content(int(sys.argv[1]), content)
			control.directory(int(sys.argv[1]), cacheToDisc=True)

			from resources.lib.modules import views
			views.setView(content, {})
		except:
			return


	def accountCheck(self):
		if traktCredentials == False and imdbCredentials == False:
			control.idle()
			control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
			sys.exit()


	def infoCheck(self, version):
		try:
			control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
			return '1'
		except:
			return '1'


	def clearCache(self):
		control.idle()
		yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
		if not yes: return
		from resources.lib.modules import cache
		cache.cache_clear()
		control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

	def clearCacheMeta(self):
		control.idle()
		yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
		if not yes: return
		from resources.lib.modules import cache
		cache.cache_clear_meta()
		control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

	def clearCacheProviders(self):
		control.idle()
		yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
		if not yes: return
		from resources.lib.modules import cache
		cache.cache_clear_providers()
		control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

	def clearCacheSearchold(self):
		control.idle()
		yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
		if not yes: return
		from resources.lib.modules import cache
		cache.cache_clear_search()
		control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')
		
	def clearCacheSearch(self):
		control.idle()
		if control.yesnoDialog(control.lang(32056).encode('utf-8'), '', ''):
			control.setSetting('tvsearch', '')
			control.setSetting('moviesearch', '')
			control.refresh()

	def clearCacheAll(self):
		control.idle()
		yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
		if not yes: return
		from resources.lib.modules import cache
		cache.cache_clear_all()
		control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

	def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
		try: name = control.lang(name).encode('utf-8')
		except: pass
		url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
		thumb = os.path.join(artPath, thumb) if not artPath == None else icon
		cm = []
		if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
		if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
		item = control.item(label=name)
		item.addContextMenuItems(cm)
		item.setArt({'icon': thumb, 'thumb': thumb})
		if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
		control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

	def endDirectory(self, file=False):
		if file == True:
			control.content(syshandle, 'files')
		else:
			control.content(syshandle, 'addons')
		control.directory(syshandle, cacheToDisc=True)