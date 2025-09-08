import numpy as np
import matplotlib.pyplot as plt

#numero de realizaciones 

N = 10000

lamb = .5

U = np.random.uniform(0,1,N)

X = -np.log(1-U)/lamb

#soporte de la densidad teorica

x = np.linspace(0,25,100)

#densidad teorica

expo_pdf = lamb*np.exp(-lamb*x)

esperanza = np.mean(X)

varianza = np.var(X)



print("Esperanza simulada:")
print(esperanza)
print("Esperanza real:")
print(1/lamb)
print("Varianza simulada:")
print(varianza)
print("Varianza real")
print(1/lamb**2)

#numero de bins para el histograma

B = 50
	
plt.figure()
plt.hist(X,B,density=True,label="Histograma",edgecolor = "k",alpha=0.6)
plt.plot(x, expo_pdf,"r",lw=2,label="Densidad teorica")
plt.show()


