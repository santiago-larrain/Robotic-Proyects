#------------------------------------------------------------------------------#
# 08_fft.py
# This code shows a FFT computation.
#
# Remarks:
# See also the matrix_intro.py example, for matrix and vector operations,
# and references to basic numerical functions of numPy and sciPy.
#
# Miguel Torres Torriti (c) 2016.07.01
#------------------------------------------------------------------------------#

import numpy as np
#from numpy import *
#from scipy.integrate import odeint
import matplotlib.pyplot as plt


def clear(j):
    print(' \n' * j)

#------------------------------------------------------------------------------#
clear(100)
print("\n--- FFT computaiton ---")

ti = 0.0    # Initial time
tf = 2.0    # Final time
Ts = 0.01   # Sampling time
Ns = (tf-ti)/Ts+1   # Number of samples
t1 = np.linspace(ti, tf, Ns)  # Two different ways to get time samples
t2 = np.arange(ti, tf+Ts, Ts)
#print("t1: ", t1)
#print("t2: ", t2)

f1 = 1/(0.25)
y1 = np.sin(2.*np.pi*f1*t1)
Y1 = np.fft.fft(y1)
Y1 = np.fft.fftshift(Y1)
freq1 = np.fft.fftfreq(t1.shape[-1], Ts)
freq1 = np.fft.fftshift(freq1)
# Note: 'fftshift' shifts the zero-frequency component to the center
# of the spectrum. Note that the output of y = fftshift(x) contains the
# Nyquist component in the first position 'y[0]' only if the length of
# the input len(x) is even.
# It is useful to apply this function in general because sometimes
# phase plots can weird looking discontinuities when data is not
# sorted correctly in the default way fft outputs the result.
print(freq1)

fig1 = plt.figure()
fig1.canvas.set_window_title('FFT example: y1 vs. t')
plt.plot(t1,  y1, 'g', label='Real Data')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
plt.legend()
plt.xlabel('t [s]')
plt.ylabel('y1 [V]')


fig2 = plt.figure()
fig2.canvas.set_window_title('FFT example: F(y1) vs. freq')
plt.plot(freq1,  Y1.real, freq1, Y1.imag) # 'g', label='Real')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('Y1 (real, imag) [V]')

fig3 = plt.figure()
fig3.canvas.set_window_title('FFT example: Magnitude[F(y1)] vs. freq')
plt.plot(freq1,  np.absolute(Y1), 'g', label='|Y1(f)|')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$\|Y1(f)\|$ [V]')

fig4 = plt.figure()
fig4.canvas.set_window_title('FFT example: Phase[F(y1)] vs. freq')
plt.plot(freq1, np.angle(Y1, deg=True), 'g', label='Y1(f)')
#plt.plot(freq1, np.arctan2(Y1.imag,Y1.real), 'g', label='Y1(f)')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$Y1(f)$ [V]')

# Now let's do some special FFTs.
# Pulse train
y2 = y1>=0.
y2 = y2.astype(float)  # 1.*y2
Y2 = np.fft.fft(y2)
Y2 = np.fft.fftshift(Y2)

fig5 = plt.figure()
fig5.canvas.set_window_title('FFT example: F(y2) vs. freq')
plt.subplot(3, 1, 1)
plt.plot(t1, y2, 'b', label='y2')
plt.xlabel('t [s]')
plt.ylabel('y2 [V]')
#
plt.subplot(3, 1, 2)
plt.plot(freq1,  np.absolute(Y2), 'g', label='|Y2(f)|')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$\|Y2(f)\|$ [V]')
#
plt.subplot(3, 1, 3)
plt.plot(freq1, np.angle(Y2, deg=True), 'g', label='Y2(f)')
#plt.plot(freq1, np.arctan2(Y1.imag,Y1.real), 'g', label='Y1(f)')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$Y2(f)$ [V]')

# Pure noise
sigma = 0.5
mu = 0
np.random.seed(0)
y3 = sigma*np.random.randn(*y1.shape)+mu  # Note the '*' is used for tuple unpacking
Y3 = np.fft.fft(y3)
Y3 = np.fft.fftshift(Y3)

fig6 = plt.figure()
fig6.canvas.set_window_title('FFT example: F(y3) vs. freq')
plt.subplot(3, 1, 1)
plt.plot(t1, y3, 'b', label='y3')
plt.xlabel('t [s]')
plt.ylabel('y3 [V]')
#
plt.subplot(3, 1, 2)
plt.plot(freq1,  np.absolute(Y3), 'g', label='|Y2(f)|')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$\|Y3(f)\|$ [V]')
#
plt.subplot(3, 1, 3)
plt.plot(freq1, np.angle(Y3, deg=True), 'g', label='Y2(f)')
#plt.plot(freq1, np.arctan2(Y1.imag,Y1.real), 'g', label='Y1(f)')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$Y3(f)$ [V]')

# Noisy sine wave
y4 = y1+0.1*y3
Y4 = np.fft.fft(y4)
Y4 = np.fft.fftshift(Y4)

fig7 = plt.figure()
fig7.canvas.set_window_title('FFT example: F(y4) vs. freq')
plt.subplot(3, 1, 1)
plt.plot(t1, y3, 'b', label='y4')
plt.xlabel('t [s]')
plt.ylabel('y4 [V]')
#
plt.subplot(3, 1, 2)
plt.plot(freq1,  np.absolute(Y4), 'g', label='|Y2(f)|')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$\|Y4(f)\|$ [V]')
#
plt.subplot(3, 1, 3)
plt.plot(freq1, np.angle(Y4, deg=True), 'g', label='Y2(f)')
#plt.plot(freq1, np.arctan2(Y1.imag,Y1.real), 'g', label='Y1(f)')
#plt.plot(t1,  z, 'b', label='Noisy data')
#plt.plot(t1,  z, 'bo-', label='Noisy data', markersize=3)
#plt.plot(t1, ye, 'r', label='Fitted line')
#plt.legend()
plt.xlabel('f [Hz]')
plt.ylabel('$Y4(f)$ [V]')


plt.show()
