import numpy as np
import matplotlib.pyplot as plt

# Parámetro de la simulación
bins = 10
N = 100    # Número de realizaciones

# Parámetro de la Rayleigh
b = 0.5

# Definición de la densidad teórica
x = np.linspace(0, 3, 300)  # soporte para la densidad teórica
rayleigh_pdf = (x/(b**2))*np.exp(-x**2/(2*b**2))

# Realizaciones de la VA
data = np.random.rayleigh(scale = b,size = N)

plt.figure(figsize=(6, 4))
# Histograma normalizado (densidad=True)
plt.hist(data, bins=bins, density=True, alpha=0.6, label="Histograma", edgecolor="k")
# Densidad teórica
plt.plot(x, rayleigh_pdf, "r", lw=2, label="Densidad teórica")
plt.title(f"Rayleigh (N={N}, bins={bins})")
plt.xlabel("x")
plt.ylabel("Densidad")
plt.legend()
plt.show()
