
import os
import urllib
import urllib.request
from xml.dom.minidom import parse, parseString
from io import BytesIO
import tkinter as tk
from PIL import Image, ImageTk

#import requests
from xml.etree import ElementTree


class CoverLoader():

   def __init__(self, config):
      self.config = config
      # create cover path
      self.lastfmapikey = config.get('Cover', 'LastFmApiKey', fallback='b665dad6fb8d30c2b734f9a573d7246f')
      self.maxSavedCovers = config.getint('Cover', 'MaxSaveCoverCount', fallback=100)
      self.savedCovers = []
      # should we save covers?
      if not self.maxSavedCovers == 0:
         self.coverPath = config.get('Cover', 'SaveCoverPath', fallback=self.config.get('System','Path')+"/cover")
         self.coverFileName = config.get('Cover', 'CoverFileName', fallback='Cover')
         print('Save cover path: ' + self.coverPath)
         if not os.path.exists(self.coverPath):
            os.makedirs(self.coverPath)
      # get all current covers for later clean up
      if self.maxSavedCovers > 0:
         for filename in os.listdir(self.coverPath):
            if filename.endswith(".png"):
               filenamepath = self.coverPath + '/' + filename
               self.savedCovers.append(filenamepath)


   def getLocalImage(self, file):
      # open local image and resize
      im = Image.open(file)
      im = im.resize((400, 400), Image.NEAREST)  # faster?: Image.NEAREST; better?: ANTIALIAS
      image = ImageTk.PhotoImage(im)
      im.close()
      return image


   # If albumPath is set, the cover will be loaded and saved from the folder specified by albumPath.
   # Otherwise it will be taken from the configured folder (SaveCoverPath)
   def getCoverFromLastFmOrLocal(self, artistName, albumName, songPath=None):

      # first try to take local cover
      if not self.maxSavedCovers == 0:
         # take/save cover from album folder or configured general folder
         if not songPath == None:
            if self.coverFileName == "ArtistAlbum":
               coverFileName = artistName + " - " + albumName + ".png"
            else:
               coverFileName = self.coverFileName + ".png"
            coverPathFile = songPath + "/" + coverFileName
         else:
            coverFileName = artistName + " - " + albumName + ".png"
            coverPathFile = self.coverPath + "/" + coverFileName
         if os.path.exists(coverPathFile):
            print('Load local cover: ' + coverPathFile)
            return self.getLocalImage(coverPathFile)

      try:
         coverUrl = self.getCoverUrlFromLastFm(artistName, albumName)
      except urllib.error.HTTPError as e:
          print('Bad last.fm urlopen http return! -> No cover!')
          print(e)
          return self.noCover()

      # save image for later use
      if coverUrl and not self.maxSavedCovers == 0:
         try:
            print('Save cover for later use: ' + coverPathFile)
            urllib.request.urlretrieve(coverUrl, coverPathFile)
            if not songPath == None:
               self.savedCovers.append(coverPathFile)
               self.cleanupSavedCovers()
         except (FileNotFoundError, PermissionError) as e:
            print(e)

      image = self.getCoverFromUrl(coverUrl)
      return image


   def getCoverUrlFromLastFm(self, artistName, albumName):

      # get album information in XML format from last.fm
      lastfmUrl  = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist='
      lastfmUrl += urllib.parse.quote(artistName)
      lastfmUrl += '&album='
      lastfmUrl += urllib.parse.quote(albumName)
      lastfmUrl += '&autocorrect=1'
      lastfmUrl += '&api_key='
      lastfmUrl += self.lastfmapikey
      print('Last.fm URL: ' + lastfmUrl)
      try:
          xmlurl = urllib.request.urlopen(lastfmUrl)
      except urllib.error.HTTPError:
          raise
      xmldoc = parse(xmlurl)
      xmlurl.close()
      #print('Last.fm XML info: ' + xmldoc.toxml())
   
      # get cover URL from XML
      coverUrl = ''
      images = xmldoc.getElementsByTagName("image")
      for image in images:
          if image.getAttribute('size') == "mega" or image.getAttribute('size') == "extralarge" or image.getAttribute('size') == "large":
              if len(image.childNodes) > 0:
                  coverUrl = image.childNodes[0].data
      print('Cover URL: ' + coverUrl)

      return coverUrl


   def getCoverFromUrl(self, coverUrl):
      image = tk.PhotoImage()
      if not coverUrl:
          print('Empty coverUrl -> No cover!')
          return self.noCover()
      try:
          u = urllib.request.urlopen(coverUrl)
          raw_data = u.read()
          u.close()
      except Exception as e:
          print('EXCEPTION: Could not open coverUrl: ' + str(e))
          return self.noCover()
      im = Image.open(BytesIO(raw_data))
      im = im.resize((400, 400), Image.ANTIALIAS)  # faster?: Image.NEAREST
      image = ImageTk.PhotoImage(im)
      im.close()
      return image


   def noCover(self):
      return self.getLocalImage(self.config.get('System','Path') + "/images/no_cover.jpg")
   
   def loading(self):
      return self.getLocalImage(self.config.get('System','Path') + "/images/loading.jpg")
   
   
   def cleanupSavedCovers(self):
      if self.maxSavedCovers > 0:
         # delete the latest saved covers, if total number exceeded maxSavedCovers
         while len(self.savedCovers) > self.maxSavedCovers:
            filePathName = self.savedCovers.pop(0)
            os.remove(filePathName)
            print('Deleted cover for clean up (max ' + str(self.maxSavedCovers) + '): ' + filePathName)

