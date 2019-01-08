
class Player_IF():

   #def __init__(self, name):
   #   self.name = name

   def isPlaying(self):
      raise NotImplementedError("Subclass must implement abstract method")
   
   def getSongAttributes(self):
      # return artistName, albumName, songName, songLength_ms in this order
      raise NotImplementedError("Subclass must implement abstract method")
   
   # currently not used
   def getSongPosition():
      raise NotImplementedError("Subclass must implement abstract method")

   def getCoverImage(self, coverLoader):
      raise NotImplementedError("Subclass must implement abstract method")      

   def play(self):
      raise NotImplementedError("Subclass must implement abstract method")

   def pause(self):
      raise NotImplementedError("Subclass must implement abstract method")

   def stop(self):
      raise NotImplementedError("Subclass must implement abstract method")

   def next(self):
      raise NotImplementedError("Subclass must implement abstract method")

   def prev(self):
      raise NotImplementedError("Subclass must implement abstract method")

   def getPlayerNamer(self):
      raise NotImplementedError("Subclass must implement abstract method")
