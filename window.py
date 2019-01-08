
#############################################################################
# create window

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import *
from PIL import Image, ImageTk
from label_ticker import LabelTicker
from enum import Enum
from itertools import cycle
import subprocess
from cover_loader import CoverLoader

import time


class LabelId(Enum):
   eArtist = 1
   eAlbum = 2
   eSong = 3

labelTickerOrder = [LabelId.eSong, LabelId.eAlbum, LabelId.eArtist]


class Window():

   def __init__(self, owner, system, config):

      print('Initialise Window ... ', end='')

      self.btnPlayImgPath = config.get('System','Path') + "/images/play_70.png"
      self.btnPlayClkImgPath = config.get('System','Path') + "/images/play_70_clk.png"
      self.btnPauseImgPath = config.get('System','Path') + "/images/pause_70.png"
      self.btnPauseClkImgPath = config.get('System','Path') + "/images/pause_70_clk.png"
      self.btnPrevImgPath = config.get('System','Path') + "/images/prev_70.png"
      self.btnPrevClkImgPath = config.get('System','Path') + "/images/prev_70_clk.png"
      self.btnNextImgPath = config.get('System','Path') + "/images/next_70.png"
      self.btnNextClkImgPath = config.get('System','Path') + "/images/next_70_clk.png"
      self.btnDispImgPath = config.get('System','Path') + "/images/display_70.png"
      self.btnDispClkImgPath = config.get('System','Path') + "/images/display_70_clk.png"

      self.root = owner
      self.root.geometry("800x480")
      self.root.configure(background='black')
      self.system = system

      self.labelTickerCycle = cycle(labelTickerOrder)
      self.tickerFinished = [False]  # use list as reference in method call

      # create splash screen
      self.splashFrame = tk.Frame(self.root, width=800, height=480, bg='black')
      self.splashFrame.pack_propagate(False)
      self.splashFrame.pack()
      self.nameLabel = tk.Label(self.splashFrame, text="PiMusicDisplay", fg='white', bg='black', font='ariel 80', anchor=tk.CENTER)
      self.nameLabel.place(x=0, y=180, height=120, width=800)
      self.lastFmLabel = tk.Label(self.splashFrame, text="Supported by last.fm", fg='white', bg='black', font='ariel 24', anchor=tk.W)
      self.lastFmLabel.place(x=0, y=440, height=40, width=400)
      self.waitingLabel = tk.Label(self.splashFrame, text="Waiting for song ...", fg='white', bg='black', font='ariel 24', anchor=tk.E)
      self.waitingLabel.place(x=400, y=440, height=40, width=400)

      self.artistLabel = LabelTicker(self.root, 400, 150, 400, 50, 'white', 'black', 'ariel', '36')
      self.albumLabel = LabelTicker(self.root, 400, 200, 400, 50, 'grey', 'black', 'ariel', '36')
      self.songLabel = LabelTicker(self.root, 0, 400, 800, 80, 'white', 'black', 'ariel', '48')

      self.songPositionString = tk.StringVar()
      self.songPositionLabel = tk.Label(self.root, textvariable=self.songPositionString, fg='white', bg='black', font='ariel 24', justify=tk.CENTER)
      self.songPositionLabel.place(x=400, y=300, height=30, width=100)

      self.songLengthString = tk.StringVar()
      self.songLengthLabel = tk.Label(self.root, textvariable=self.songLengthString, fg='white', bg='black', font='ariel 24', justify=tk.CENTER)
      self.songLengthLabel.place(x=700, y=300, height=30, width=100)

      self.songPositionPercent = tk.IntVar()
      self.stylePB = ttk.Style()
      self.stylePB.theme_use('classic')
      self.stylePB.configure("Horizontal.TProgressbar", background="SteelBlue3", troughcolor="grey10", borderwidth=0 )
      self.progressBar = ttk.Progressbar(self.root, variable=self.songPositionPercent, length=380, maximum=100, mode='determinate', style="Horizontal.TProgressbar")
      self.progressBar.place(x=405, y=340, height=15, width=390)

      self.coverImage = tk.PhotoImage()
      self.coverLabel = tk.Label(self.root, image=self.coverImage, bg='black')
      self.coverLabel.place(x=0, y=0, height=400, width=400)

      im = Image.open(self.btnPrevImgPath)
      self.btnPrevImage = ImageTk.PhotoImage(im)
      im.close()
      self.btnPrev = tk.Button(self.root, image=self.btnPrevImage, command=self.Prev, bd=0, highlightthickness=0)
      self.btnPrev.place(x=405, y=5, height=70, width=70)

      im = Image.open(self.btnPauseImgPath)
      self.btnPauseImage = ImageTk.PhotoImage(im)
      im.close()
      self.btnPause = tk.Button(self.root, image=self.btnPauseImage, command=self.Pause, bd=0, highlightthickness=0)
      self.btnPause.place(x=485, y=5, height=70, width=70)

      im = Image.open(self.btnPlayImgPath)
      self.btnPlayImage = ImageTk.PhotoImage(im)
      im.close()
      self.btnPlay = tk.Button(self.root, image=self.btnPlayImage, command=self.Play, bd=0, highlightthickness=0)
      self.btnPlay.place(x=565, y=5, height=70, width=70)

      im = Image.open(self.btnNextImgPath)
      self.btnNextImage = ImageTk.PhotoImage(im)
      im.close()
      self.btnNext = tk.Button(self.root, image=self.btnNextImage, command=self.Next, bd=0, highlightthickness=0)
      self.btnNext.place(x=645, y=5, height=70, width=70)

      im = Image.open(self.btnDispImgPath)
      self.btnDisplayImage = ImageTk.PhotoImage(im)
      im.close()
      self.btnDisplay = tk.Button(self.root, image=self.btnDisplayImage, command=self.Display, bd=0, highlightthickness=0)
      self.btnDisplay.place(x=725, y=5, height=70, width=70)

      #self.btnPlay.bind('<ButtonPress-1>', self.Play())
      #self.btnPlay.bind('<ButtonRelease-1>', self.Play())

      self.splashFrame.tkraise()
      print('OK')


   def Update(self):
      self.root.update()

   def InitFinished(self):
      if self.splashFrame: 
         self.splashFrame.destroy()

   def setImage(self, obj, image):
      #print('setImage: ' + image)
      im = Image.open(image)
      objImage = ImageTk.PhotoImage(im)
      im.close()
      obj.configure(image = objImage)
      return objImage

   def setImageRet(self, obj, image, ret):
      ret = self.setImage(obj, image)


   def SetActiveTicker(self):
      if self.tickerFinished[0]:
         self.tickerFinished[0] = False
         currentTicker = next(self.labelTickerCycle)
         if currentTicker == LabelId.eSong:
            self.songLabel.StartMove(self.tickerFinished)
         elif currentTicker == LabelId.eAlbum:
            self.albumLabel.StartMove(self.tickerFinished)
         elif currentTicker == LabelId.eArtist:
            self.artistLabel.StartMove(self.tickerFinished)

   def ActivateTicker(self):
      if self.songLabel.move or self.albumLabel.move or self.artistLabel.move:
         self.tickerFinished[0] = True
      else:
         self.tickerFinished[0] = False


# update song attributes

   def OnNewSong(self):
      self.ActivateTicker()
      self.resetPrevNextImage()

   def SetArtist(self, artistName):
      self.artistLabel.SetText(artistName)

   def SetAlbum(self, albumName):
      self.albumLabel.SetText(albumName)

   def SetSong(self, songName):
      self.songLabel.SetText(songName)

   def SetSongLength(self, songLength):
      self.songLengthString.set(songLength)

   def SetSongPosition(self, position):
      self.songPositionString.set(position)

   def SetSongPositionPercent(self, position):
      self.songPositionPercent.set(position)

   def SetCoverImage(self, image):
      self.coverImage = image
      self.coverLabel.configure(image = self.coverImage)


# player state actions

   def onPlay(self, player):
      self.player = player
      self.btnPlayImage = self.setImage(self.btnPlay, self.player.getPlayImg())
      self.btnPauseImage = self.setImage(self.btnPause, self.btnPauseImgPath)
      self.stylePB.configure("Horizontal.TProgressbar", background=self.player.getColor())
      self.progressBar = ttk.Progressbar(style="Horizontal.TProgressbar")

   def onPause(self):
      self.btnPauseImage = self.setImage(self.btnPause, self.player.getPauseImg())
      self.btnPlayImage = self.setImage(self.btnPlay, self.btnPlayImgPath)


# button actions

   def Prev(self):
      print('\nButton PREV pressed')
      self.setPrevClkImage()
      self.player.prev()

   def Pause(self):
      print('\nButton PAUSE pressed')
      self.setPauseClkImage()
      self.player.pause()

   def Play(self):
      print('\nButton PLAY pressed')
      self.setPlayClkImage()
      self.player.play()

   def Next(self):
      print('\nButton NEXT pressed')
      self.setNextClkImage()
      self.player.next()

   def Display(self):
      print('\nButton DISPLAY pressed')
      self.system.backlightOFF()


# change button image temporarily to give feedback
# * image will be set back after player state change

   def setPlayClkImage(self):
      self.btnPlayImage = self.setImage(self.btnPlay, self.btnPlayClkImgPath)

   def setPauseClkImage(self):
      self.btnPauseImage = self.setImage(self.btnPause, self.btnPauseClkImgPath)

   def setPrevClkImage(self):
      self.btnPrevImage = self.setImage(self.btnPrev, self.btnPrevClkImgPath)

   def setNextClkImage(self):
      self.btnNextImage = self.setImage(self.btnNext, self.btnNextClkImgPath)

   def setDispClkImage(self):
      self.btnDisplayImage = self.setImage(self.btnDisplay, self.btnDispClkImgPath)
      #self.btnDisplay.after(1000, self.setImageRet, self.btnDisplay, self.btnDispImgPath, self.btnDisplayImage)
      # ^^ not working - why?

   def resetPrevNextImage(self):
      self.btnPrevImage = self.setImage(self.btnPrev, self.btnPrevImgPath)
      self.btnNextImage = self.setImage(self.btnNext, self.btnNextImgPath)
