import numpy as np
import matplotlib.pyplot as plt

# Definimos los polos y ceros de un sistema
#zeros = np.array([-2 + 1j, -2 - 1j])  # Ejemplo: dos ceros complejos conjugados
poles = np.array([-2516.5+182.79j, -2516.5-182.79j])  # Ejemplo: tres polos, dos complejos conjugados y uno real


# Definir los parámetros de la circunferencia
h, k = 0, 0  # Centro de la circunferencia (h, k)
w = 2523.13        # Radio

# Generar puntos de la circunferencia
theta = np.linspace(0, 2 * np.pi, 500)  # Ángulos desde 0 a 2π
x = h + w * np.cos(theta)               # Coordenadas x
y = k + w * np.sin(theta)               # Coordenadas y
# Crear el plano complejo
plt.figure(figsize=(8, 6))
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')  # Eje real
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')  # Eje imaginario



plt.plot(x, y, label=f'$\omega$={w}', color='green', linestyle='--')


# Graficar polos y ceros
#plt.scatter(zeros.real, zeros.imag, s=100, color='blue', label='Ceros', marker='o', edgecolors='black')
plt.scatter(poles.real, poles.imag, s=100, color='red', label='Polos (-2516.5 $\pm$ 182.79j)', marker='x')

# Configuraciones del gráfico
plt.title('Diagrama de Polos y Ceros', fontsize=14)
plt.xlabel('Parte Real', fontsize=12)
plt.ylabel('Parte Imaginaria', fontsize=12)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.grid(alpha=0.5)
plt.legend(fontsize=12)
plt.axis('equal')  # Misma escala en ambos ejes para simetría
plt.show()

