import numpy as np

import matplotlib.pyplot as plt

p = .7

Z = np.random.binomial(1, p, (1000, 100)) 

X = 2*Z-1

Y = np.empty((1000, 100))

n = np.arange(0,100)

suma_actual = 0

for j in range(0,1000):
	for i in range(0,100):
		suma_actual += X[j,i]
		Y[j,i]=suma_actual
	suma_actual = 0

media_estimada = np.mean(Y, axis = 0)

media_teorica = n*(2*p-1)

plt.figure()
plt.step(n,Y[0])
plt.plot(media_teorica, linestyle='-', color = "magenta")
plt.plot(media_estimada, color = "red")

varianza_estimada = np.var(Y,axis = 0)
varianza_teorica = 4*n*p*(1-p)

plt.figure()
plt.step(n,Y[0])
plt.plot(varianza_teorica, linestyle = '-', color = "red")
plt.plot(varianza_estimada, color = "magenta")
plt.show()



