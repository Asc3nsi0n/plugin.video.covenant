
import os,xbmc
logfile    = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Asc3nsi0n', 'log.txt'))


def log(text):
	file = open(logfile,"w+")
	file.write(str(text))

def check4update():
	import re,time,xbmc,xbmcgui
	from resources.lib.modules import client

	addonxml = xbmc.translatePath('special://home/addons/script.module.Asc3nsi0n/addon.xml')
	file     = open(addonxml)
	data     = file.read()
	file.close()

	c_version = re.compile('" version="(.+?)"').findall(data)[0]
	c_version2= (c_version).replace('.','')
	
	log(c_version2)

	html = client.request('https://raw.githubusercontent.com/CBOX/addons.xml')

	o_version = re.compile('script.module.Asc3nsi0n.+?version="(.+?)"').findall(html)[0]
	o_version2= (o_version).replace('.','')
	log(o_version2)
	if c_version2 < o_version2:
		update = 'https://github.com/CBOX/script.module.Asc3nsi0n-%s.zip'%o_version
		install(o_version,update)
		xbmc.executebuiltin("UpdateAddonRepos")
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(5)
		xbmcgui.Dialog().notification('Ascension','Updated Successfully')
	
	
def install(vers,url):
    import xbmc,xbmcgui,os,re,time
    from resources.lib.modules import downloader2
    addon_folder = xbmc.translatePath('special://home/addons/script.module.Asc3nsi0n/')
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("Ascension","Installing Dependency Update v[COLOR red]%s[/COLOR]"%vers,'', 'Please Wait')
    lib=os.path.join(path, 'content.zip')
    try:
       os.remove(lib)
    except:
       pass
	   
    import shutil

    shutil.rmtree(addon_folder)
    try:
        downloader2.download(url, lib, dp)
        addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
        time.sleep(3)
    except:
        xbmcgui.Dialog().ok('Ascension','Oops..Something Went Wrong Downloading The Update...Try Again')
    dp = xbmcgui.DialogProgress()
    dp.create("Ascension","Installing Dependency Update Version [COLOR red]%s[/COLOR]"%vers,'', 'Please Wait')
    dp.update(0,"", "Installing... Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    try:
        unzip(lib,addonfolder,dp)
    except:
        xbmcgui.Dialog().ok('Ascension','Oops..Something Went Wrong Installing The Update...Try Again')
	
	
def unzip(_in, _out, dp):
	import zipfile,sys
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok('Ascension', 'Process was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True