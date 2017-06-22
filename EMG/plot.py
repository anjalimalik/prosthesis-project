import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import threading
import sys
import os

os.system('defaults write org.python.python ApplePersistenceIgnoreState NO')

WindowSize = 5000
SampleRate = 1000.0
VoltsPerBit = 2.5/256

#Global variables
data = []
displayData = [-2 for i in range(WindowSize)]

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

#Connect the UDP_Port
UDP_PORT = 9000
sock = socket.socket(socket.AF_INET, #Internet
                     socket.SOCK_DGRAM) #UDP

#Setup plot parameters
fig, ax = plt.subplots()
line, = ax.plot([], '-r')
plt.xlim([0,WindowSize/SampleRate])
plt.ylim([-VoltsPerBit*128,VoltsPerBit*128])
plt.xlabel('Time (Seconds)')
plt.ylabel('EMG (mV)')


def animate(i):
  global displayData, data

  newData = list(data)
  data = []
  newDisplay = list(displayData[len(newData):len(displayData)] + newData)
  displayData = list(newDisplay)
  line.set_ydata([i*VoltsPerBit-1.25 for i in displayData])
  return line,


def init():
  line.set_xdata([i/SampleRate for i in range(WindowSize)])
  line.set_ydata([i for i in displayData])
  return line,

print('Connected to ', str(UDP_IP))
print("Listening for incoming messages...")
print('Close Plot Window to exit')

#Creating a new thread to listen for data over UDP
thread = threading.Thread(target=data_listener)
thread.daemon = True
thread.start()

#Creating a new thread to update the plot with acquired data
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init, interval=25, blit=True)


plt.show()
