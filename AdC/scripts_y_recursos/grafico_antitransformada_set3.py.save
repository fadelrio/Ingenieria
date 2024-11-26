import numpy as np
import matplotlib.pyplot as plt

# Definimos la función h(t)
def h(t):
    return 2862.92 * (-np.exp(-10605.2 * t) + np.exp(-761.4 * t))

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

