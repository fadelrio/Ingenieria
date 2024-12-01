import numpy as np
import matplotlib.pyplot as plt

# Definimos la función h(t)
def h(t):
    return 2,34 * (np.exp(-(454.55 - 2510.72j) * t) + np.exp(-(454.55 + 2510.72j) * t))

# Rango de t (ajústalo según lo que desees analizar)
t = np.linspace(0, 0.01, 1000)  # Por ejemplo, de 0 a 0.01 segundos
h_values = h(t)

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(t, h_values, color='b')
plt.title('Respuesta al impulso')
plt.grid(True)
plt.legend()
plt.show()

