

###   deprecated   ###


import sys
import time
import dbus

from player_if import Player_IF


class IF_Mopidy(Player_IF):

   color = "#00A2E8"

   def __init__(self, config):
      self.config = config
      if self.config.getboolean('Player', 'UseMopidy', fallback=False):
         print('Initialise Mopidy mpris ... ', end='')
         # init dbus
         if self.config.get('Player', 'MopidyBus', fallback="system") == "system":
            bus = dbus.SystemBus()  # use system bus, because we run as service (start-up on boot)
         else:
            bus = dbus.SessionBus()  # use session bus (local start-up)
         # init mpris dbus interface
         try:
            mopidy_mpris = bus.get_object('org.mpris.MediaPlayer2.mopidy','/org/mpris/MediaPlayer2')
         except dbus.DBusException as e:
            print('EXCEPTION: Mopidy not found: ' + str(e))
            return
         self.PlayerProps = dbus.Interface(mopidy_mpris, dbus_interface='org.freedesktop.DBus.Properties')
         self.PlayerMeths = dbus.Interface(mopidy_mpris, dbus_interface='org.mpris.MediaPlayer2.Player')
         print('OK')
      else:
         print('Mopidy not in use')


   #############################################################################
   # interface

   from subprocess import call

   def getStatus(self):
      if self.config.getboolean('Player', 'UseMopidy', fallback=False) and 'self.PlayerProps' in globals():
         try:
            status = self.PlayerProps.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
            return status
         except dbus.DBusException as e:
            print(__name__, "getSongAttributes", e)
            #call(["sudo service mopidy restart"])  # restart mopidy - check user rights !?!
            return 'Exception'
      return 'Mopidy not in use'


   def getSongAttributes(self):
      # get current song metadata
      try:
         metadata = self.PlayerProps.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
      except dbus.DBusException as e:
         print(__name__, "getSongAttributes", e)
         #call(["sudo service mopidy restart"])  # restart mopidy - check user rights !?!
         return '', '', '', 0
      #print('Mopidy metadata: ' + str(metadata))
      #print('Mopidy metadata: ' + str(metadata['mpris:trackid']))
      artistName = 'unknown'
      albumName = 'unknown'
      songName = 'unknown'
      songLength = 0
      if not 'mpris:trackid' in metadata:
         return '', '', '', 0
      if 'xesam:artist' in metadata:
         artistName = metadata['xesam:artist'][0]
      if 'xesam:album' in metadata:
         albumName = metadata['xesam:album']
      if 'xesam:title' in metadata:
         songName = metadata['xesam:title']
      if 'mpris:length' in metadata:
         songLength = metadata['mpris:length']
      return artistName, albumName, songName, songLength


   def getSongPosition(self):
      position_us = 0
      try:
         position_us = self.PlayerProps.Get('org.mpris.MediaPlayer2.Player', 'Position')
      except dbus.DBusException as e:
         print(__name__, "getSongPosition", e)
         #call(["sudo service mopidy restart"])  # restart mopidy - check user rights !?!
         return 0
      return position_us


   def play(self):
      self.PlayerMeths.Play()

   def pause(self):
      self.PlayerMeths.Pause()

   def stop(self):
      # no real stop present; use pause
      self.PlayerMeths.Pause()

   def next(self):
      self.PlayerMeths.Next()

   def prev(self):
      self.PlayerMeths.Previous()


   def getPlayImg(self):
       return "/home/pi/PiMusicDisplay/Images/play_mopi_70.png"

   def getPauseImg(self):
       return "/home/pi/PiMusicDisplay/Images/pause_mopi_70.png"

   def getColor(self):
      return IF_Mopidy.color
