"""
01_create_data.py
Creates some data.
 
 
Learn how to:
1. make vectors and arrays:
http://scipy.github.io/old-wiki/pages/NumPy_for_Matlab_Users.html 

2. generate random values:
https://docs.python.org/3/library/random.html
https://docs.scipy.org/doc/numpy-dev/reference/routines.random.html

3. plot data:
http://matplotlib.org/api/pyplot_api.html
 
Miguel Torres-Torriti (c) 2016.07.01
"""

# Load packages
#from numpy import *
import numpy as np

import matplotlib.pyplot as plt

import random

# Create and print variables
# Compare the error of sin(0) and sin(2*pi)
x = np.sin(0)
print("sin(0) = %e" %x)
x = np.sin(2*np.pi)
print("sin(2*pi) = %e" %x)

# Create an array of time samples
# http://scipy.github.io/old-wiki/pages/NumPy_for_Matlab_Users.html
ti = 0.0    # Initial time
tf = 5.0    # Final time
Ts = 0.01   # Sampling time
Ns = (tf-ti)/Ts+1   # Number of samples
t = np.linspace(ti, tf, Ns)
# Create sinusoidal signals
x1 = np.sin(2*np.pi*t)
x2 = np.cos(2*np.pi*t)
print(len(t))
print(t[-1])
print(x1)
plt.plot(t, x1, t, x2) 
plt.xlabel('t [s]')
plt.ylabel('x [V]')
plt.show()


# Create arrays of random values
# https://docs.python.org/3/library/random.html
# https://docs.scipy.org/doc/numpy-dev/reference/routines.random.html
k=0
mu = 1.0
sigma = 0.5
n1 = np.zeros(len(t))
random.seed(0)
for i in t:
    print(k)
    n1[k] = random.normalvariate(mu, sigma)
    k+=1    
    
plt.plot(t, n1)
plt.xlabel('t [s]')
plt.ylabel('x [V]')
plt.show()

np.random.seed(0)
n2 = sigma*np.random.randn(len(t))+mu
plt.plot(t, n1, t, n2)
plt.xlabel('t [s]')
plt.ylabel('x [V]')
plt.show()

# Create an histrogram
# http://matplotlib.org/api/pyplot_api.html
plt.hist(n1,50)
plt.show()

# Save data
data = np.c_[x1,x2] # Concatanate columns
np.save("data.npy",data)
print("File saved to 'data.npy'")
np.savetxt("data.csv",data)
print("File saved to 'data.csv'")