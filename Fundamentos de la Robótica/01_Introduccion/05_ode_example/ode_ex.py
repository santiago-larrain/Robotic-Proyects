import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
vo = 10
k1 = 0.5
k2 = 0.35

# Declare the model
def ode_ex_fun(y, t):
   yd0 = vo - k1*y[0]
   yd1 = k1*y[0] - k2*y[1]
   return [yd0, yd1]

   
t = np.linspace(0.0, 20.0, 100)
yinit = np.array([5.0, 0.0])
ti = time.perf_counter()
y = odeint (ode_ex_fun, yinit, t)
tf = time.perf_counter()
print("Elapsed time is %f seconds.\n" %(tf-ti))
plt.plot(t, y[:,0], t, y[:,1]) # y[:,0] is the first column of y
plt.xlabel('t')
plt.ylabel('y')
plt.show()