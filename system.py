
from threading import Timer
import subprocess

class System():

   def __init__(self, config):
      # create initial timer instance
      self.timeout = config.getint('System', 'DisplayOffTimeout', fallback=300)
      if self.timeout == -1:
         print('No display control')
         return
      self.timer = Timer(2 * self.timeout, self.backlightOFF)
      self.backlightOn = False

   def backlightON(self):
      if self.timeout == -1:
         return
      if self.timer.is_alive():
         self.timer.cancel()
      if not self.backlightOn:
         print('Turn backlight ON')
         #f = open('/sys/class/backlight/rpi_backlight/bl_power', 'w')
         #f.write('0')
         #f.close()
         subprocess.call(["xset","dpms","force","on"])
         self.backlightOn = True

   def backlightOFF(self):
      if self.timeout == -1:
         return
      if self.timer.is_alive():
         self.timer.cancel()
      print('Turn backlight OFF')
      #f = open('/sys/class/backlight/rpi_backlight/bl_power', 'w')
      #f.write('1')
      #f.close()
      #subprocess.call(["xset","dpms","force","off"])
      subprocess.Popen("sleep 1; xset dpms force off", shell=True)
      self.backlightOn = False

   def backlightOffTimer(self):
      if self.timeout == -1:
         return
      if self.timeout == 0:
         self.backlightOFF()
         return
      if self.timer.is_alive():
         self.timer.cancel()
      print('Set backlight OFF timer: ' + str(self.timeout) + " sec")
      self.timer = Timer(self.timeout, self.backlightOFF)
      self.timer.start()
      self.backlightOn = False

