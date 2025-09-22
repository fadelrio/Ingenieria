import numpy as np

import matplotlib.pyplot as plt

p = .7

Z = np.random.binomial(1, p, (1000, 100)) 

X = 2*Z-1

media_estimada = np.mean(X, axis = 0)

media_teorica = 2*p-1

plt.figure()
plt.stem(X[0])
plt.hlines(y =[ media_teorica], xmin = 0, xmax = 100, linestyles=['-'], color = "magenta")
plt.plot(media_estimada, color = "red")

varianza_estimada = np.var(X,axis = 0)
varianza_teorica = 4*p*(1-p)

plt.figure()
plt.stem(X[0])
plt.hlines(y = [varianza_teorica],xmin = 0, xmax = 100, linestyles = ['-'], color = "red")
plt.plot(varianza_estimada, color = "magenta")
plt.show()



