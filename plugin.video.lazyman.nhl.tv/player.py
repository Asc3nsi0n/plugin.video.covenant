import xbmc

class LazyManPlayer(xbmc.Player):
  def __init__(self, *args, **kwargs):
    xbmc.log("Player started")

  def onPlayBackStarted(self):
    xbmc.log("Playback started {}" % self.getPlayingFile(), xbmc.LOGNOTICE)

  def onPlayBackStopped(self):
    xbmc.log("Playback stopped", xbmc.LOGNOTICE)

  def onPlayBackEnded(self):
    xbmc.log("Playback ended", xbmc.LOGNOTICE)

