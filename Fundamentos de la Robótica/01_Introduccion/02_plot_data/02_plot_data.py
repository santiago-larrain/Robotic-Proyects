"""
02_plot_data.py
Plots the data stored in data_01.npy or data_01.csv 
 
Miguel Torres-Torriti (c) 2016.07.01
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

from numpy import *

print("Loading data...")
data = loadtxt("data_01.csv")
#data = load("data_01.npy")
#savetxt("data_01.csv",data)  # Uncomment this line if you want to convert from npy to csv file format
print(data)

rows = data.shape[0]
cols = data.shape[1]
t = data[:,0]
x = data[:,1:13]
ref = data[:,13]
mv  = data[:,14]

print("Drawing plot 1...")
fig1 = plt.figure()
fig1.canvas.set_window_title('State variables: x_1, x_2, x_3')
print(type(t), t)
print(type(x), x)
plt.plot(t, x[:,0], t, x[:,1], t, x[:,2])
plt.xlabel('t [s]')
plt.ylabel('x_1, x_2, x_3 [m]')

print("Drawing plot 2...")
fig2 = plt.figure()
fig2.canvas.set_window_title('State variables: x_4, x_5, x_6')
plt.plot(t, degrees(x[:,3]), t, degrees(x[:,4]), t, degrees(x[:,5]))
plt.xlabel('t [s]')
plt.ylabel('x_4, x_5, x_6 [grad]')

print("Drawing plot 3...")
fig3 = plt.figure()
fig3.canvas.set_window_title('State variables: x_7, x_8, x_9')
plt.plot(t, x[:,6], t, x[:,7], t, x[:,8])
plt.xlabel('t [s]')
plt.ylabel('x_7, x_8, x_9 [m/s]')

print("Drawing plot 4...")
fig4 = plt.figure()
fig4.canvas.set_window_title('State variables: x_10, x_11, x_12')
plt.plot(t, x[:,9], t, x[:,10], t, x[:,11])
plt.xlabel('t [s]')
plt.ylabel('x_10, x_11, x_12 [rad/s]')

print("Drawing plot 5...")
fig5 = plt.figure()
fig5.canvas.set_window_title('Manipulated variables')
plt.plot(t, mv, t, ref-x[:,2], t, ref)
plt.xlabel('t [s]')
plt.ylabel('MV, error [m], ref [m]')

print("Drawing plot 6...")
mpl.rcParams['legend.fontsize'] = 10
fig3 = plt.figure()
fig3.canvas.set_window_title('Robot trajectory')
ax = fig3.gca(projection='3d')
ax.plot(x[:,0], x[:,1], x[:,2], label='Robot trajectory')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')
ax.legend()

plt.show()