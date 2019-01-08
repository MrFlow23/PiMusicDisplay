
import urllib.request
import json

from player_if import Player_IF


class IF_SpotifyConnectWeb(Player_IF):

   name = "SpotifyConnectWeb"
   color = "#22B14C"
   useSpotify = False

   def __init__(self, config):
      self.config = config
      self.useSpotify = self.config.getboolean('Player', 'UseSpotifyConnectWeb', fallback=False)
      if self.useSpotify:
         print('Initialise SpotifyConnect interface ... ', end='')
         server = config.get('Player', 'SpotifyServer', fallback="localhost")
         port = config.get('Player', 'SpotifyPort', fallback="4000")
         self.urlPrefix = 'http://' + server + ':' + port + '/api'
         self.activateOnSoundOtherDevice = self.config.getboolean('Player', 'ActivateOnSoundOtherDevice', fallback='False')
         self.coverSource = self.config.get('Cover', 'Spotify', fallback='last.fm')
         print('OK')
      else:
         print('SpotifyConnect not in use')

   def executeCommand(self, command):
      #print('Send to Spotify: ' + self.urlPrefix + command)
      return urllib.request.urlopen(self.urlPrefix + command)

   def isPlaying(self):
      if self.useSpotify:
         try:
            resp = self.executeCommand('/info/status')
         except (urllib.error.URLError, ConnectionResetError) as e:
            #print(__name__, "getStatus", e.reason)
            return 'Exception'
         string = resp.read().decode('utf-8')
         #print(string)
         json_obj = json.loads(string)
         return json_obj['playing'] and (json_obj['active'] or self.activateOnSoundOtherDevice)

   def getMetadata(self):
      try:
         resp = self.executeCommand('/info/metadata')
      except urllib.error.URLError as e:
         print(__name__, "getMetadata", e.reason)
         return 'Exception'
      string = resp.read().decode('utf-8')
      #print(string)
      json_obj = json.loads(string)
      return json_obj

   def getSongAttributes(self):
      json_obj = self.getMetadata()
      songLength_ms = json_obj['duration']
      self.artistName = json_obj['artist_name']
      self.albumName = json_obj['album_name']
      return json_obj['artist_name'], json_obj['album_name'], json_obj['track_name'], songLength_ms

   def getSongPosition(self):
      # getting song position is not available on spotify interface
      return 0


   def getCoverImage(self, coverLoader):
      if self.coverSource == "spotify":
         print('Load cover from Spotify')
         coverImage = coverLoader.getCoverFromUrl(self.getCoverUrl())
      elif self.coverSource == "last.fm":
         coverImage = coverLoader.getCoverFromLastFmOrLocal(self.artistName, self.albumName)
      return coverImage

   def getCoverUrl(self):
      json_obj = self.getMetadata()
      coverUri = json_obj['cover_uri']
      coverUrl = self.urlPrefix + '/info/image_url/large/' + coverUri
      return coverUrl


   def play(self):
      self.executeCommand('/playback/play')

   def pause(self):
      self.executeCommand('/playback/pause')

   def stop(self):
      # no real stop present; use pause
      self.executeCommand('/playback/pause')

   def next(self):
      self.executeCommand('/playback/next')

   def prev(self):
      self.executeCommand('/playback/prev')


   def getPlayImg(self):
       return self.config.get('System','Path') + "/images/play_spot_70.png"

   def getPauseImg(self):
       return self.config.get('System','Path') + "/images/pause_spot_70.png"

   def getColor(self):
      return IF_SpotifyConnectWeb.color

   def getPlayerName(self):
      return IF_SpotifyConnectWeb.name
