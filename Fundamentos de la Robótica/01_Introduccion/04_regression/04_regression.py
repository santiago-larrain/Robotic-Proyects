#------------------------------------------------------------------------------#
# 07_regression.py
# This code shows a basic nonlinear regression to solve the parameter
# estimation and data fitting problem.
#
# Remarks:
# See also the matrix_intro.py example, for matrix and vector operations,
# and references to basic numerical functions of numPy and sciPy.
#
# Miguel Torres Torriti (c) 2016.07.01
#------------------------------------------------------------------------------#

#import numpy as np
from numpy import *
#from scipy.integrate import odeint
import matplotlib.pyplot as plt


def clear(j):
    print(' \n' * j)

#------------------------------------------------------------------------------#
clear(100)
print("\n--- Nonlinear regression ---")

ti = 0.0    # Initial time
tf = 2.0    # Final time
Ts = 0.1   # Sampling time
Ns = (tf-ti)/Ts+1   # Number of samples
t1 = linspace(ti, tf, Ns)
t2 = arange(ti, tf+Ts, Ts)
print("t1: ", t1)
print("t2: ", t2)

sigma = 0.5
mu = 0
noise = sigma*random.randn(Ns)+mu
print("noise: \n", noise)

m = 3.0
c = 2.0
y = m*t1**3 + c 
z = m*t1**3 + c + noise
print("y = m*t^3 + c: \n", y)
print("z = m*t^3 + c + noise: \n", z)

# y_k = [t_k^3 1]*[m c]^T
# [m c]^T = [t_k 1]^{+}*y_k
A = c_[t1**3, ones(Ns)]
#print("A:\n", A)
ms, cs = linalg.lstsq(A,z)[0]
print("ms, cs:\n", ms, cs)

ye = ms*t1**3 + cs

fig1 = plt.figure()
fig1.canvas.set_window_title('Regression example')
plt.plot(t1,  y, 'g', label='Real Data')
#plt.plot(t1,  z, 'b', label='Noisy data')
plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
plt.plot(t1, ye, 'r', label='Fitted line')
plt.legend()
plt.xlabel('t [s]')
plt.ylabel('y, z, y_e [V]')
plt.show()



