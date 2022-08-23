import serial

import math
import numpy as np
import time
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyUSB0')

# GUI

plt.ion()

#  Plot


x_values = [0] * 40
t_values = [i for i in range(0, 40)]

# here we are creating sub plots
figure, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 40)
ax.set_ylim(0,120)

line1, = ax.plot(t_values, x_values)

bt_values = [np.mean(t_values[i*10:i*10+10]) for i in range(0,4)]
bx_values = [np.mean(x_values[i*10:i*10+10]) for i in range(0,4)]
bars = ax.bar(bt_values, bx_values)

# Labels

plt.xlabel("t",fontsize=18)
plt.ylabel("Acelerometro",fontsize=18)


t = 0

gravedad = 0
g_steps = 100
for i in range(g_steps):
    line=ser.readline().decode('utf-8')
    x,y,z = [int(i) for i in line.replace('\r\n','').split(',')]
    mag = math.sqrt(x*x+y*y+z*z)
    gravedad += mag
gravedad /= g_steps

while True:
    t+=1
    line=ser.readline().decode('utf-8')
    x,y,z = [int(i) for i in line.replace('\r\n','').split(',')]
    #print(x,y,z)
    mag = math.sqrt(x*x+y*y+z*z) - gravedad
    mag /= 100

    if t > 100:
        if mag > 20:
            t = 0
            x_values = [0] * 40
    
    if t >= 40:
        continue 
    
    x_values[t] = mag
        
    line1.set_ydata(x_values)

    first = np.max(x_values[0:10])
    for  i, rect in enumerate(bars):
        cur = np.max(x_values[i*10:i*10+10])
        rect.set_height(100*cur/first)

    figure.canvas.draw()
    figure.canvas.flush_events()
    #time.sleep(0.1)
    

