import tkinter as tk
import tkinter.font as tkFont
import time


class LabelTicker():

   def __init__(self, owner, x, y, width, height, fg, bg, font, size):
      self.text = tk.StringVar()
      self.font = tkFont.Font(family=font,size=size)
      self.x_init = x
      self.width = width
      self.field = tk.Label(owner, textvariable=self.text, fg=fg, bg=bg, font=self.font)
      self.field.place(x=x, y=y, height=height, width=width)

      self.move = False
      self.move_id = None
      self.distance = -3
      self.move_delay = 50  # ms
      self.dir_delay = 2000
      self.start_delay = 4000
      self.dir_switched = False


   def Move(self, finished):
      # move ticker
      self.x = self.x + self.distance
      self.field.place(x=self.x)
      
      # ticker at line end? - switch direction
      if not self.dir_switched and self.x <= self.x_init + self.x_limit or self.x > self.x_init:
         self.distance = -self.distance
         # do not switch distance again in very next loop
         self.dir_switched = True
         if self.distance < 0:
            # when switched back to negative, one cycle is finished
            finished[0] = True  # use list as reference
         else:
            # set longer waiting time for direction switch
            sleepTime = self.dir_delay
      else:
         self.dir_switched = False
         sleepTime = self.move_delay
         
      if not finished[0]:
         self.move_id = self.field.after(sleepTime, self.Move, finished)


   def StartMove(self, finished):
      if self.move:
         self.move_id = self.field.after(self.start_delay, self.Move, finished)
      else:
         finished[0] = True


   def SetText(self, text):
      if self.move_id != None:
         self.field.after_cancel(self.move_id)
         self.move_id = None
      textWidth = self.font.measure(text)
      self.x = self.x_init
      self.x_limit = self.width - textWidth
      self.text.set(text)
      # move text, if length is bigger then field width
      if textWidth > self.width:
         self.field.place(x=self.x, width=textWidth)
         self.move = True
         #self.field.after(self.delay, self.Move)
      else:
         self.field.place(x=self.x+(self.x_limit/2), width=textWidth)
         self.move = False

