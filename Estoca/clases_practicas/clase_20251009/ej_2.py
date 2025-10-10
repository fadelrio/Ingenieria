import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

omega1 = 0.42*np.pi
omega2 = 0.43*np.pi

N = 100

N_fft = 4092

n = np.arange(0,N)

X_1 = np.sin(omega1*n)


X_2 = np.sin(omega2*n)


S_1 = (1/N)*np.abs(sp.fft.fft(X_1, N_fft))**2

frec = np.arange(0, 2*np.pi, 2*np.pi/N_fft)

plt.figure()
plt.plot(frec,S_1)
plt.xlim([0.3*np.pi, 0.5*np.pi])


S_suma = (1/N)*np.abs(sp.fft.fft(X_1 + X_2,N_fft))**2

frec = np.arange(0, 2*np.pi, 2*np.pi/N_fft)

plt.figure()
plt.plot(frec,S_suma)
plt.xlim([0.3*np.pi, 0.5*np.pi])



N = 200

n = np.arange(0,N)

X_1 = np.sin(omega1*n)


X_2 = np.sin(omega2*n)


S_suma = (1/N)*np.abs(sp.fft.fft(X_1 + X_2,N_fft))**2

frec = np.arange(0, 2*np.pi, 2*np.pi/N_fft)

plt.figure()
plt.plot(frec,S_suma)
plt.xlim([0.3*np.pi, 0.5*np.pi])

plt.show()
