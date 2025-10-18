import numpy as np 
import matplotlib.pyplot as plt

N = 100

X = np.random.normal(0, np.sqrt(2), N + 1)

Y = np.empty_like(X)

for i in range(100):
	Y[i] = 0.5*X[i+1] + 0.75*X[i]



R = np.correlate(Y,Y,mode='full')/N

k = np.arange(-N,N+1)

	

plt.figure()
plt.plot(k,R)
plt.xlim([-15,15])
plt.grid(True)
plt.show()
