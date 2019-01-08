

import urllib.request
import json
import getpass
import configparser

from player_if import Player_IF


class IF_Mopidy(Player_IF):

   name = "Mopidy"
   color = "#00A2E8"
   useMopidy = False

   artistName = ""
   albumName = ""

   def __init__(self, config):
      self.config = config
      self.useMopidy = self.config.getboolean('Player', 'UseMopidy', fallback=False)
      if self.useMopidy:
         print('Initialise Mopidy interface ... ', end='')
         server = config.get('Player', 'MopidyServer', fallback="localhost")
         port = config.get('Player', 'MopidyPort', fallback="6680")
         self.url = 'http://' + server + ':' + port + '/mopidy/rpc'
         self.SaveCoverInSongFolder = config.getboolean('Cover', 'SaveCoverInSongFolder', fallback=False)
         self.initMopidyConfig()
         print('OK')
      else:
         print('Mopidy not in use')

   def initMopidyConfig(self):
      username = getpass.getuser()
      if username == "root":
         mopidyConfigFile = "/etc/mopidy/mopidy.conf"
      else:
         mopidyConfigFile = "/home/" + username + "/.config/mopidy/mopidy.conf"
      self.mopidyConfig = configparser.ConfigParser()
      self.mopidyConfig.read(mopidyConfigFile)


   def executeCommand(self, command):
      #print('Send to Mopidy: ' + self.url + ' ' + command)
      value_bytes = str.encode(command)
      return urllib.request.urlopen(self.url, value_bytes)


   def isPlaying(self):
      if self.useMopidy:
         try:
            resp = self.executeCommand('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_state"}')
         except urllib.error.URLError as e:
            #print(__name__, "getStatus", e.reason)
            return 'Exception'  # working in main?
         string = resp.read().decode('utf-8')
         #print(string)
         json_obj = json.loads(string)
         return json_obj['result'] == "playing"

   def getSongAttributes(self):
      try:
         resp = self.executeCommand('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_current_track"}')
      except urllib.error.URLError as e:
         print(__name__, "getSongAttributes", e.reason)
         return 'Exception'
      string = resp.read().decode('utf-8')
      #print(string)
      json_obj = json.loads(string)
      artist = ''
      album = ''
      track = ''
      uri = ''
      songLength_ms = 0
      if 'result' in json_obj and json_obj['result'] is not None:
         if 'artists' in json_obj['result'] and 'name' in json_obj['result']['artists'][0]:
            artist = json_obj['result']['artists'][0]['name']
         if 'album' in json_obj['result'] and  'name' in json_obj['result']['album']:
            album = json_obj['result']['album']['name']
         if 'name' in json_obj['result']:
            track = json_obj['result']['name']
         if 'length' in json_obj['result']:
            songLength_ms = json_obj['result']['length']
         if 'uri' in json_obj['result']:
            uri = json_obj['result']['uri']
      self.artistName = artist
      self.albumName = album
      self.uri = uri
      return artist, album, track, songLength_ms

   def getSongPosition(self):
      # not implemented yet
      return 0

   def getCoverImage(self, coverLoader):
      if self.SaveCoverInSongFolder:
         return coverLoader.getCoverFromLastFmOrLocal(self.artistName, self.albumName, self.getSongPath())
      else:
         return coverLoader.getCoverFromLastFmOrLocal(self.artistName, self.albumName)

   def getSongPath(self):
      # get media directory path from mopidy config
      mediaPath = self.mopidyConfig.get('local', 'media_dir')
      startIdx = self.uri.rfind(':')
      endIdx = self.uri.rfind('/')
      if startIdx == -1:
         startIdx = 0
      if endIdx == -1:
         endIdx = 0
      # create complete song path from media path and album path from URI from song attributes
      songPath = mediaPath + '/' + self.uri[startIdx+1:endIdx]
      # remove song file name
      songPath = self.transAllHexToCharacter(songPath)
      return songPath

   # transform all hex codes in string to according character (eg %20 = space)
   def transAllHexToCharacter(self, str):
      i = 0
      while i < len(str):
         if str[i] == '%':
            hex = str[i+1:i+3]
            if hex[0] is not None and hex[0].isdigit() and hex[1] is not None and hex[1].isdigit():
               char = bytearray.fromhex(hex).decode()
               str = str.replace('%'+hex, char)
         i += 1
      return str


   def play(self):
      self.executeCommand('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}')

   def pause(self):
      self.executeCommand('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.pause"}')

   def stop(self):
      self.executeCommand('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.stop"}')

   def next(self):
      self.executeCommand('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.next"}')

   def prev(self):
      self.executeCommand('{"jsonrpc": "2.0", "id": 1, "method": "core.playback.previous"}')


   def getPlayImg(self):
       return self.config.get('System','Path') + "/images/play_mopi_70.png"

   def getPauseImg(self):
       return self.config.get('System','Path') + "/images/pause_mopi_70.png"

   def getColor(self):
      return IF_Mopidy.color

   def getPlayerName(self):
      return IF_Mopidy.name
