# -*- coding: utf-8 -*-

'''
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
'''	

import os,time,hashlib

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.modules import control


def fetch(items, lang):
    try:
        t2 = int(time.time())
        metacacheFile = os.path.join(control.dataPath, 'meta.5.db')
        dbcon = database.connect(metacacheFile)
        dbcur = dbcon.cursor()
    except:
        try: dbcon.close()
        except: pass
        return items

    for i in range(0, len(items)):
        try:
            dbcur.execute("SELECT * FROM meta WHERE (imdb = '%s' and lang = '%s' and not imdb = '0') or (tmdb = '%s' and lang = '%s' and not tmdb = '0') or (tvdb = '%s' and lang = '%s' and not tvdb = '0')" % (items[i]['imdb'], lang, items[i]['tmdb'], lang, items[i]['tvdb'], lang))
            match = dbcur.fetchone()

            t1 = int(match[5])
            update = (abs(t2 - t1) / 3600) >= 720
            if update == True: raise Exception()

            item = eval(match[4].encode('utf-8'))
            item = dict((k,v) for k, v in item.iteritems() if not v == '0')

            if items[i]['fanart'] == '0':
                try: items[i].update({'fanart': item['fanart']})
                except: pass

            item = dict((k,v) for k, v in item.iteritems() if not k == 'fanart')
            items[i].update(item)

            items[i].update({'metacache': True})
        except:
            pass

    try: dbcon.close()
    except: pass

    return items


def insert(meta):
    try:
        if not meta: return
        control.makeFile(control.dataPath)
        metacacheFile = os.path.join(control.dataPath, 'meta.5.db')

        dbcon = database.connect(metacacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS meta (""imdb TEXT, ""tmdb TEXT, ""tvdb TEXT, ""lang TEXT, ""item TEXT, ""time TEXT, ""UNIQUE(imdb, tmdb, tvdb, lang)"");")
        t = int(time.time())
        r = False
        for m in meta:
            try:
                i = repr(m['item'])
                try: dbcur.execute("DELETE * FROM meta WHERE (imdb = '%s' and lang = '%s' and not imdb = '0') or (tmdb = '%s' and lang = '%s' and not tmdb = '0') or (tvdb = '%s' and lang = '%s' and not tvdb = '0')" % (m['imdb'], m['lang'], m['tmdb'], m['lang'], m['tvdb'], m['lang']))
                except: pass
                try: dbcur.execute("INSERT INTO meta Values (?, ?, ?, ?, ?, ?)", (m['imdb'], m['tmdb'], m['tvdb'], m['lang'], i, t))
                except: r = True ; break
            except:
                pass
        dbcon.commit()
        dbcon.close()

        if r == False: return

        control.deleteFile(metacacheFile)
        dbcon = database.connect(metacacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS meta (""imdb TEXT, ""tmdb TEXT, ""tvdb TEXT, ""lang TEXT, ""item TEXT, ""time TEXT, ""UNIQUE(imdb, tmdb, tvdb, lang)"");")
        t = int(time.time())
        r = False
        for m in meta:
            try:
                i = repr(m['item'])
                try: dbcur.execute("DELETE * FROM meta WHERE (imdb = '%s' and lang = '%s' and not imdb = '0') or (tmdb = '%s' and lang = '%s' and not tmdb = '0') or (tvdb = '%s' and lang = '%s' and not tvdb = '0')" % (m['imdb'], m['lang'], m['tmdb'], m['lang'], m['tvdb'], m['lang']))
                except: pass
                dbcur.execute("INSERT INTO meta Values (?, ?, ?, ?, ?, ?)", (m['imdb'], m['tmdb'], m['tvdb'], m['lang'], i, t))
            except:
                pass
        dbcon.commit()
        dbcon.close()
    except:
        return

def local(items, link, poster, fanart):
    try:
        dbcon = database.connect(control.metaFile())
        dbcur = dbcon.cursor()
        args = [i['imdb'] for i in items]
        dbcur.execute('SELECT * FROM mv WHERE imdb IN (%s)'  % ', '.join(list(map(lambda arg:  "'%s'" % arg, args))))
        data = dbcur.fetchall()
    except:
        return items

    for i in range(0, len(items)):
        try:
            item = items[i]

            match = [x for x in data if x[1] == item['imdb']][0]

            try:
                if poster in item and not item[poster] == '0': raise Exception()
                if match[2] == '0': raise Exception()
                items[i].update({poster: link % ('300', '/%s.jpg' % match[2])})
            except:
                pass
            try:
                if fanart in item and not item[fanart] == '0': raise Exception()
                if match[3] == '0': raise Exception()
                items[i].update({fanart: link % ('1280', '/%s.jpg' % match[3])})
            except:
                pass
        except:
            pass

    return items
