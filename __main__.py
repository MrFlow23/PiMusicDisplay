
#############################################################################
### imports

import tkinter as tk
import time
import sys
import datetime

# own stuff
from config_reader import ConfigReader
from window import Window
from system import System
from if_mopidy import IF_Mopidy
from if_spotifyconnectweb import IF_SpotifyConnectWeb
from remote_ir import RemoteIR
from cover_loader import CoverLoader


#############################################################################
# init

print(' ### PiMusicDisplay ### ')

now = datetime.datetime.now()
print(now)

debug = False
if len(sys.argv) > 1 and sys.argv[1] == "-d":
   debug = True
   print('Running in debug mode')

config = ConfigReader()
config.printConfig()

# create system (eg backlight controller)
system = System(config.get())

root = tk.Tk()
win = Window(root, system, config.get())

# init ir-remote
remote = RemoteIR(system, config, win)

# init mopidy interface
Mopidy = IF_Mopidy(config.get())

# init spotiy-connect-web interface
SpotConnWeb = IF_SpotifyConnectWeb(config.get())

coverLoader = CoverLoader(config.get())


#############################################################################
# main loops

def pollPlayer():
   
   bPlay = False

   # get active player
   if Mopidy.isPlaying() == True:
      player = Mopidy
      bPlay = True
   elif SpotConnWeb.isPlaying() == True:
      player = SpotConnWeb
      bPlay = True

   if bPlay:
      onPlay(player)
      return

   root.after(2000, pollPlayer)


def onPlay(player):
   print(player.getPlayerName() + ': Start playing')
   win.InitFinished()  # for playing first time after start-up
   win.onPlay(player)
   if 'remote' in globals():
      remote.setPlayer(player)
   system.backlightON()
   playing(player)

def onStop(player):
   print(player.getPlayerName() + ': Stop playing')
   win.onPause()
   system.backlightOffTimer()
   pollPlayer()


lastSongName = ""
lastAlbumName = ""
updatePlayerTimeId = None
playerTime = 0

def playing(player):

   global lastSongName, lastAlbumName
   global updatePlayerTimeId
   global playerTime

   # still playing ?
   if player.isPlaying() != True:
      if updatePlayerTimeId != None:
         root.after_cancel(updatePlayerTimeId)
         updatePlayerTimeId = None
      onStop(player)
      return

   # get song attributes
   artistName, albumName, songName, songLength_ms = player.getSongAttributes()

   # new song playing -> update display
   if songName != lastSongName:
      lastSongName = songName
      songLengthStr = getTimeString(songLength_ms)
      print( ' *** New song: ' + artistName +', '+ albumName +', '+ songName +', '+ songLengthStr + '(' + str(songLength_ms) + ')' )

      win.SetArtist(artistName)
      win.SetAlbum(albumName)
      win.SetSong(songName)
      win.SetSongLength(songLengthStr)
      win.OnNewSong()

      # start player time
      playerTime = 0
      if updatePlayerTimeId != None:
         root.after_cancel(updatePlayerTimeId)
      updatePlayerTime(songLength_ms, time.time()*1000)
   elif updatePlayerTimeId == None:
      # restart player time after pause
      updatePlayerTime(songLength_ms, time.time()*1000)

   # update cover for new album
   if albumName != lastAlbumName:
      lastAlbumName = albumName
      win.SetCoverImage(coverLoader.loading())
      # call after short break, to load other window elements first
      root.after(20, setCover, player)

   win.SetActiveTicker()
   root.after(500, playing, player)


def setCover(player):
   image = player.getCoverImage(coverLoader)
   win.SetCoverImage(image)

def updatePlayerTime(songLength_ms, lastTime):
   global updatePlayerTimeId
   global playerTime
   now = time.time()*1000
   playerTime = playerTime + (now - lastTime)
   win.SetSongPosition(getTimeString(playerTime))
   if songLength_ms != 0:
      win.SetSongPositionPercent((playerTime/songLength_ms)*100)
   updatePlayerTimeId = root.after(100, updatePlayerTime, songLength_ms, now)

def getTimeString( length_ms ):
    minutes = length_ms / 60000
    seconds = length_ms % 60000 / 1000
    timeString = str(int(minutes)).zfill(2) + ':' + str(int(seconds)).zfill(2)
    return timeString


print(' *** Start main loop *** ')
pollPlayer()

root.mainloop()
