
import os
import configparser

class ConfigReader():

   configFile = "config.ini"

   def __init__(self):
      path = os.path.dirname(os.path.abspath(__file__))
      self.config = configparser.ConfigParser()
      self.config.read(path + '/' + self.configFile)
      self.config.set('System', 'Path', path)

   def get(self):
      return self.config

   def printConfig(self):
      print('From ' + self.config.get('System','Path') + '/' + self.configFile + ':')
      for section in self.config.sections():
         print('  ' + section)
         for key in self.config[section]:
            print('    ' + key + ' = ' + self.config[section][key])
