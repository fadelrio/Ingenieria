import numpy as np
import matplotlib.pyplot as plt

# Cargar datos desde el archivo
archivo = "PAM4_set2.txt"
datos = np.loadtxt(archivo, skiprows = 1)

# Separar columnas en x e y
x = datos[:, 0]  # Primera columna
y = datos[:, 1]  # Segunda columna

# Graficar
plt.plot(x, y, linestyle='-', color='b', label='Señal codificada en PAM4')

# Personalización de la gráfica
plt.xlabel('Tiempo [s]')
plt.ylabel('Tensión [V]')
plt.title('Respuesta a código en PAM4')
plt.legend()
plt.grid(True)

# Mostrar la gráfica
plt.show()
