import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# === PARÁMETROS DE ENTRADA ===
ganancia = 0.35
ceros = [-0.05 + 0.74j, -0.05 - 0.74j]
polos = [-1, 0, -0.03 + 0.706j, -0.03 - 0.706j]

# === CREAR FUNCIÓN DE TRANSFERENCIA ===
num = ganancia * np.poly(ceros)
den = np.poly(polos)

sistema = signal.TransferFunction(num, den)

# === FRECUENCIA PARA EL BODE ===
w = np.logspace(np.log10(1), np.log10(100), 1000)  # De 1 a 100 rad/s

# Calcular respuesta en frecuencia
w, mag, phase = signal.bode(sistema, w)

# === GRAFICAR BODE ===
plt.figure(figsize=(10, 6))

# Módulo
plt.subplot(2, 1, 1)
plt.semilogx(w, mag)
plt.title('Diagrama de Bode')
plt.ylabel('Magnitud (dB)')
plt.grid(True, which='both')

# Fase
plt.subplot(2, 1, 2)
plt.semilogx(w, phase)
plt.ylabel('Fase (°)')
plt.xlabel('Frecuencia (rad/s)')
plt.grid(True, which='both')

plt.tight_layout()
plt.show()

