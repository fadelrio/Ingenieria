import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

omega1 = 0.22*np.pi
omega2 = 0.38*np.pi
omega3 = 0.12*np.pi
omega4 = 0.4*np.pi
omega5 = 0.25*np.pi

N = 100

N_fft = 4092

n = np.arange(0,N)

X_1 = np.sin(omega1*n) + np.sin(omega2*n) + np.sin(omega3*n) + np.sin(omega4*n) + np.sin(omega5*n)

S_1 = (1/N)*np.abs(sp.fft.fft(X_1, N_fft))**2

frec = np.arange(0, 2*np.pi, 2*np.pi/N_fft)

real_f = np.array([omega1,omega2,omega3,omega4,omega5,-omega1 + 2*np.pi,-omega2 + 2*np.pi,-omega3 + 2*np.pi,-omega4 + 2*np.pi,-omega5 + 2*np.pi])
real_m = np.array([30, 30, 30, 30, 30, 30, 30, 30, 30 ,30])

plt.figure()
plt.plot(frec,S_1)
plt.stem(real_f,real_m, linefmt = "m")
#plt.xlim([0.3*np.pi, 0.5*np.pi])
plt.show()

