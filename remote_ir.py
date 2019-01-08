
import lirc
import time
from threading import Thread
import subprocess


class RemoteIR():

   def __init__(self, system, config, window):
      if config.get().getboolean('Remote', 'UseLirc', fallback=False):
         print('Initialise IR remote ... ', end='')
         sockid=lirc.init(config.get().get('Remote','LircProgramName'), blocking = False, verbose = True)
         self.system = system
         self.config = config
         self.window = window
         self.player = 0
         thread = Thread(target=self.run)
         thread.start()
         print('OK')

   def run(self):
      while True:
         codeIR = lirc.nextcode()
         if codeIR != [] and not self.player == 0:
            if codeIR[0] == self.config.get().get('LircButtonNames','Play', fallback='KEY_PLAY'):
               print('Remote PLAY pressed')
               self.window.setPlayClkImage()
               self.player.play()
            if codeIR[0] == self.config.get().get('LircButtonNames','Stop', fallback='KEY_STOP'):
               print('Remote STOP pressed')
               self.window.setPauseClkImage()
               self.player.pause()
               self.system.backlightOFF()
            if codeIR[0] == self.config.get().get('LircButtonNames','Pause', fallback='KEY_PAUSE'):
               print('Remote PAUSE pressed')
               self.window.setPauseClkImage()
               self.player.pause()
            if codeIR[0] == self.config.get().get('LircButtonNames','NextSong', fallback='KEY_NEXT'):
               print('Remote NEXT pressed')
               self.window.setNextClkImage()
               self.player.next()
            if codeIR[0] == self.config.get().get('LircButtonNames','PrevSong', fallback='KEY_PREVIOUS'):
               print('Remote PREVIOUS pressed')
               self.window.setPrevClkImage()
               self.player.prev()
         time.sleep(0.05)

   def setPlayer(self, player):
      self.player = player
