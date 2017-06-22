#Electromyography Brain-Machine Interface (EMG BMI)

import pyglet
import matplotlib
matplotlib.use('TkAgg')
import numpy as np  #Importing numpy for use
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import threading
import sys
import os
import statistics #Importing Average Function
import math #Importing Math Functionality
from math import sqrt #Importing Square Root Function


os.system('defaults write org.python.python ApplePersistenceIgnoreState NO')

WindowSize = 5000
SampleRate = 1000.0
VoltsPerBit = 2.5/256

#Global variables
Fs = 1000
FlexWindowSize = 0.25
data = []
displayData = [-2 for i in range(WindowSize)]
flexing = True

#To read from a socket
def data_listener():
  global data
  UDP_PORT = 9000
  sock = socket.socket(socket.AF_INET, #Internet
                      socket.SOCK_DGRAM) #UDP
  sock.bind((UDP_IP, UDP_PORT))
  while True:
    newdata, addr = sock.recvfrom(1024) #buffer size - 1024 bytes
    data.extend(list(newdata))

#Handle command line arguments to get IP address
if (len(sys.argv) == 2):
    try:
        UDP_IP = sys.argv[1]
        socket.inet_aton(UDP_IP)
    except:
        sys.exit('Invalid IP address, Try again')
else:
    sys.exit('EMG_Acquire <Target IP Address>')

#To connect the UDP_Port
UDP_PORT = 9000
sock = socket.socket(socket.AF_INET, #Internet
                     socket.SOCK_DGRAM) #UDP

print('Connected to ', str(UDP_IP))
print("Listening for incoming messages...")
print('Close Window to exit')

#Creating a new thread to listen for data over UDP
thread = threading.Thread(target=data_listener)
thread.daemon = True
thread.start()

#Load and place image resources
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()
ForeArm_image = pyglet.resource.image("forearm.png")
Bicep_image = pyglet.resource.image("Bicep.png")
ForeArm_image.anchor_x = 7
ForeArm_image.anchor_y = ForeArm_image.height-150
Bicep_image.anchor_x = Bicep_image.width/2
Bicep_image.anchor_y = Bicep_image.height/2

#Moving ForeArm class
class ForeArm(pyglet.sprite.Sprite):
  def __init__(self, *args, **kwargs):
    super(ForeArm,self).__init__(img=ForeArm_image,*args, **kwargs)
    self.rotate_speed = 100.0
    self.rotation_upper_limit = -10
    self.rotation_lower_limit = -100
    self.rotation = self.rotation_upper_limit
    self.key_handler = pyglet.window.key.KeyStateHandler()

  def update(self, dt):
    if flexing:
      if not ((self.rotation-self.rotate_speed*dt) <=  self.rotation_lower_limit):
        self.rotation -= self.rotate_speed*dt
      else:
        self.rotation = self.rotation_lower_limit
    else:
      if not((self.rotation+self.rotate_speed*dt) >= self.rotation_upper_limit):
        self.rotation += self.rotate_speed*dt
      else:
        self.rotation = self.rotation_upper_limit


#To setup the main window
main_window = pyglet.window.Window(1000,600)
main_batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
bicep = pyglet.sprite.Sprite(img=Bicep_image,x=350,y=150,batch=main_batch,group=background)
forearm = ForeArm(x=510, y=115,batch=main_batch,group=foreground)
pyglet.gl.glClearColor(1, 1, 1, 1)
main_window.push_handlers(forearm)
main_window.push_handlers(forearm.key_handler)


def update(dt):
  global displayData, data, flexing

  newData = list(data)
  data = []
  newDisplay = list(displayData[len(newData):len(displayData)] + newData)
  displayData = list(newDisplay)


  DataWindow = list(displayData[4549:4999]) #Data array of last 450 points
  maximum = max(DataWindow) #Maximmum value in window array
  square = np.power(DataWindow, 2)
  newsquare = list(square)
  average = statistics.mean(newsquare)
  rms = int(math.sqrt(average))
  print(rms, maximum)

  #Flex when maximum value in window array is greater than rms+error
  if maximum > (rms + 11):
    flexing = True
  else:
    flexing = False


  forearm.update(dt)

@main_window.event
def on_draw():
    main_window.clear()
    main_batch.draw()

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
