import numpy as np
import matplotlib.pyplot as plt

# Cantidad de muestras
N = 200

# Generar realizaciones U1 y U2 ~ U(-1, 1)
U1 = np.random.uniform(-1,1,N)
U2 = np.random.uniform(-1,1,N)
# Generar realizaciones X1 y X2
X1 = 0.5*U1-0.3*U2
X2 = .7*U1 +.2*U2
# Generar realizaciones Y1 y Y2
Y1 = 1.2*U1-.1*U2
Y2 = U1 +.1*U2
# Matriz de correlación
corrU = np.corrcoef(U1, U2)[0, 1]
corrX = np.corrcoef(X1, X2)[0, 1]
corrY = np.corrcoef(Y1, Y2)[0, 1]

# Función auxiliar para grafico de dispersión
def plot_vector(v1, v2, title, labels):
    plt.figure(figsize=(4, 4))
    plt.scatter(v1, v2, alpha=0.7)
    plt.xlim([-2, 2])
    plt.ylim([-2, 2])
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.title(title)
    plt.grid(True)
    plt.show()

plot_vector(U1, U2, f"Vector U. Coef. correlación: {corrU:.3f}", ('U1', 'U2'))
plot_vector(X1, X2,  f"Vector X. Coef. correlación: {corrX:.3f}", ('X1', 'X2'))
plot_vector(Y1, Y2,  f"Vector Y. Coef. correlación: {corrY:.3f}", ('Y1', 'Y2'))	
