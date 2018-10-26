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
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.modules import control

if control.setting('clrsources.start.uni') == 'true' and control.setting('scraper.default') == '0' or control.setting('scraper.default') == '3':
	#if control.setting('scraper.default') == '0' or '3':
		try:
			control.idle()
			control.makeFile(control.uniDataPath)
			dbcon = database.connect(control.uniCacheFile)
			dbcur = dbcon.cursor()
			dbcur.execute("DROP TABLE IF EXISTS rel_src")
			dbcur.execute("DROP TABLE IF EXISTS rd_domains")
			dbcur.execute("VACUUM")
			dbcon.commit()
		except:
			pass
if control.setting('clrsources.start.int') == 'true' and control.setting('scraper.default') == '1' or control.setting('scraper.default') == '3':
	#if control.setting('scraper.default') == '1' or '3':
		try:
			control.idle()
			control.makeFile(control.dataPath)
			dbcon = database.connect(control.providercacheFile)
			dbcur = dbcon.cursor()
			dbcur.execute("DROP TABLE IF EXISTS rel_src")
			dbcur.execute("DROP TABLE IF EXISTS rel_url")
			dbcur.execute("VACUUM")
			dbcon.commit()
		except:
			pass

if control.setting('resolver.clear.start') == 'true':
	if control.setting('resolver') == '0':
		control.execute('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache')
	else:
		control.execute('RunPlugin(plugin://script.module.urlresolver/?mode=reset_cache')

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

'''
############## UPDATE MESSAGE ################

import time,os

newVerFile = os.path.join(control.addonPath, 'news.txt')

if os.path.exists(newVerFile):
	time.sleep(20)
	from resources.lib.modules import message
	message.viewDialog(newVerFile,'[B]Ascension Update Notice![/B]')
	time.sleep(5)
	try: os.remove(newVerFile)
	except: pass
'''
