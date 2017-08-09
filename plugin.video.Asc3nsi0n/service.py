import urllib , urllib2 , sys , re , xbmcplugin , xbmcgui , xbmcaddon , xbmc , os, shutil, time

# ADD TO addon.xml>>>>>>
#	<extension point="xbmc.service" library="service.py" start="login" />

addonsPath     = xbmc.translatePath ( os.path.join ( 'special://home/addons' , '' ) )
addonxml       = os.path.join ( addonsPath , 'plugin.video.Asc3nsi0n' , 'addon.xml' )
service        = os.path.join ( addonsPath , 'plugin.video.Asc3nsi0n' , 'service.py' )
#repozip       = os.path.join ( addonsPath , 'packages' , 'repository.UNKNOWN.zip' )
readme         = os.path.join ( addonsPath , 'plugin.video.Asc3nsi0n' , 'README' )
userdataPath   = xbmc.translatePath ( os.path.join ( 'special://userdata' , '' ) )
databasePath   = xbmc.translatePath('special://database')
thumbnailsPath = xbmc.translatePath('special://thumbnails')
Asc3nsi0ndata  = xbmc.translatePath ( os.path.join ( userdataPath+'/addon_data/plugin.video.Asc3nsi0n' , '' ) )
texturesDb     = os.path.join(databasePath,"Textures13.db")


ExodusPath  = xbmc.translatePath ( os.path.join ( addonsPath , 'plugin.video.exodus' ) )
GRPath  = xbmc.translatePath ( os.path.join ( addonsPath , 'plugin.video.genesisreborn' ) )
GRArtPath  = xbmc.translatePath ( os.path.join ( addonsPath , 'script.genesisreborn.artwork' ) )
GRMetaPath  = xbmc.translatePath ( os.path.join ( addonsPath , 'script.genesisreborn.metadata' ) )
GRDataPath = xbmc.translatePath ( os.path.join ( userdataPath+'/addon_data' , 'plugin.video.genesisreborn' ) )


def killxbmc(over=None):
	if over: choice = 1
	else: choice = xbmcgui.Dialog().yesno('CBOX Update', 'Kodi needs to Close to apply an Update.', 'Would you like to continue?', nolabel='[B]Cancel[/B]',yeslabel='[B]Yes[/B]')
	if choice == 1:
		os._exit(1)
		

if os.path.exists(readme)==False:

	#xbmcgui . Dialog ( ) . ok ( "[B]Major CBOX Update[/B]" , "Your CBOX has been Updated. [B][COLOR ff1e90ff]Ascension[/COLOR][/B] is now your main Add-on, it has the same features as [B]Exodus[/B] and more!" , "", "[B][COLOR ff1e90ff]CBOX[/B] Movies & TVShows[/COLOR] no longer use Ascension and are [B][COLOR ffd20000]direct play[/COLOR][/B] links." )	
	
	#remove exodus	
	try:shutil.rmtree(ExodusPath, ignore_errors=True)
	except:pass	
	

	#remove genesisreborn	
	try:shutil.rmtree(GRPath, ignore_errors=True)
	except:pass	

	try:shutil.rmtree(GRArtPath, ignore_errors=True)
	except:pass	
	
	try:shutil.rmtree(GRMetaPath, ignore_errors=True)
	except:pass		

	try:shutil.rmtree(GRDataPath, ignore_errors=True)
	except:pass	
	
	
	#remove Asc3nsi0n userdata files for refresh
	try:os.remove(Asc3nsi0ndata+"/cache.db")
	except:pass	
	
	try:os.remove(Asc3nsi0ndata+"/meta")
	except:pass	

	try:os.remove(Asc3nsi0ndata+"/meta.5.db")
	except:pass	

	try:os.remove(Asc3nsi0ndata+"/regex.db")
	except:pass
	
	try:os.remove(Asc3nsi0ndata+"/bookmarks.db")
	except:pass	
	
	
	#delete thumbnails NEW
	#try:shutil.rmtree(thumbnailsPath)	
	#except:pass	

	#try:os.remove(texturesDb, *, dir_fd=None)
	#except:pass	
	
	
	
	#delete thumbnails OLD
	#try:shutil.rmtree(userdataPath+"/Thumbnails")	
	#except:pass	
	
	#if os.path.exists(thumbnailsPath) == True:	
	#	shutil.rmtree(thumbnailsPath)
	#else:pass	
	
	#if os.path.exists(texturesDb) == True:	
	#	os.unlink(texturesDb)
	#else:pass

	#try:os.remove(texturesDb, *, dir_fd=None)
	#except:pass	


	xbmcgui . Dialog ( ) . ok ( "[B]CBOX Update[/B]" , "[COLOR ff1e60ff][B]Exodus[/B][/COLOR] has been removed and [B][COLOR ff1e90ff]Ascension[/COLOR][/B] is now your MAIN Add-on." , "", "Many [B]Add-on[/B] Shortcuts have been removed from the [B]Homescreen[/B], you can still find them in the [COLOR green][B]Add-ons[/B][/COLOR] section.                                                               Your device requires a [COLOR ff7f0000][B]Reboot[/B][/COLOR] to complete the update." )
	
	time.sleep(2)
	
	
	a=open(addonxml).read()
	f= open ( addonxml , mode = 'w' )
	f . write ( a.replace('<extension point="xbmc.service" library="service.py" start="login" />','') )
	
	#xbmc . executebuiltin ( 'UpdateLocalAddons' )
	#xbmc . executebuiltin ( 'UpdateAddonRepos' )	
	#try:os.remove(service)
	#except:pass
	
	time.sleep(2)
	
	#try:killxbmc()
	#except:pass	
		
	
	xbmc.executebuiltin('reboot')

else:
        try:os.remove(readme)
        except:pass


		
		
		
		
		
		
		
		
		
		

		
	
	

i1i1II = """If you are seeing this message this means your CBOX has been updated.

Please read this as there has been big changes...

#1
Ascension is now your Main Kodi Add-on!
It has all the same features as Exodus but with extras.

___________________________________________________________


#2
The first two home buttons, Movie & TV Shows now play instantly.(No selecting links)
I will continute to add new TV Shows (Full Seasons) on a regular basis."""

	
	
#if os.path.exists(readme)==False:
    #if xbmcgui.getCurrentWindowDialogId()< 10001:
        #def O0 ( heading , text ) :
         #id = 10147
         #if 70 - 70: oo0 . O0OO0O0O - oooo
         #xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
         #xbmc . sleep ( 100 )
         #if 11 - 11: ii1I - ooO0addonso
         #ii11i = xbmcgui . Window ( id )
         #if 66 - 66: iIiI * iIiiiI1IiI1I1 * o0OoOoOO00
         #I11i = 50
         #while ( I11i > 0 ) :
          #try :
           #xbmc . sleep ( 30 )
           #I11i -= 1
           #ii11i . getControl ( 1 ) . setLabel ( heading )
           #ii11i . getControl ( 5 ) . setText ( text )
           #return
          #except :
           #pass
        #O0 ( '[COLOR red][B]CBOX Mediaboxes[/B][/COLOR]' , i1i1II )
        #I11i = 50	
        #n=0
        #import time
        #while n < 30:
            #time.sleep(1)
            #n += 1
        #a=open(addonxml).read()
        #f= open ( addonxml , mode = 'w' )
        #f . write ( a.replace('<extension point="xbmc.service" library="service.py" start="login" />','') )
        #xbmc . executebuiltin ( 'UpdateLocalAddons' )
        #xbmc . executebuiltin ( 'UpdateAddonRepos' )	
        #try:os.remove(service)
        #except:pass
        #try:os.remove(repozip)
        #except:pass
		
