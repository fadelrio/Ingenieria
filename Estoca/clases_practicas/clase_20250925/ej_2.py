import numpy as np

import matplotlib.pyplot as plt

realizaciones = 5000

ene = 100

tita = np.random.uniform(0, 2*np.pi, (realizaciones))

A = 1

w_o = .5 

n = np.arange(0,ene)

X = np.empty((realizaciones, ene))

for j in range(0,realizaciones):
	for i in range(0,ene):
		X[j,i] = A*np.cos(w_o*n[i]+tita[j])


media_estimada = np.mean(X, axis = 0)

media_teorica = 0;

plt.figure()
plt.step(n,X[0])
plt.hlines(y =[ media_teorica], xmin = 0, xmax = 100, linestyles=['-'], color = "magenta")
plt.plot(media_estimada, color = "red")

varianza_estimada = np.var(X,axis = 0)
varianza_teorica = A*A/2

plt.figure()
plt.step(n,X[0])
plt.hlines(y = [varianza_teorica],xmin = 0, xmax = 100, linestyles = ['-'], color = "red")
plt.plot(varianza_estimada, color = "magenta")
plt.show()
