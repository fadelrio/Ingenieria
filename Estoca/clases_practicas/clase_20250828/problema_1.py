import numpy as np
import matplotlib.pyplot as plt

# Cantidad de muestras
N = 1000

# Angulo de roatción
tita = np.pi/4

# Generar realizaciones X1 y X2 ~ U(-1, 1)
X1 = np.random.uniform(-1,1,(N))
X2 = np.random.uniform(-1.5,1.5,(N))

X = np.array([X1,X2])
#defino la matriz de rotación

R = np.array([[np.cos(tita),-np.sin(tita)],[np.sin(tita),np.cos(tita)]])

#defino la variable Y

Y = np.dot(R,X)

def plot_vector(v1, v2, title, labels):
    plt.figure(figsize=(4, 4))
    plt.scatter(v1, v2, alpha=0.7)
    plt.xlim([-2, 2])
    plt.ylim([-2, 2])
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.title(title)
    plt.grid(True)

corrY = np.corrcoef(Y)
corrX = np.corrcoef(X)

plot_vector(Y[0], Y[1], f"grafico de dispersion de Y",('Y1','Y2'))
plot_vector(X[0],X[1], "grafico de dispersion de X",('X1','X2'))


print(f"Matriz de autocorr de Y:")
print(corrY)
print("Matriz de autocorr de X:")
#esto esta mal, se buscaba la matriz de autocovarianza
print(corrX)
print(f"Matriz de autocov de Y:")
print(np.cov(Y))
print(f"Matriz de autocov de X:")
print(np.cov(X))
plt.show()
