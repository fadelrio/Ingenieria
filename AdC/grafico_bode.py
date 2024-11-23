import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Definir la función de transferencia
# Ejemplo: G(s) = 10 / (s^2 + 2s + 10)
numerador = [28181980]  # Coeficientes del numerador
denominador = [1, 11366.664, 8075065]  # Coeficientes del denominador
G = ctrl.TransferFunction(numerador, denominador)

# Calcular el diagrama de Bode (sin graficar automáticamente)
frecuencia, ganancia, fase = ctrl.bode_plot(G,omega=[50,1000000] , dB=True, Hz=False, deg=True, plot=True, freq_label = "Frecuencia [rad/s]", magnitude_label = "Magnitud [dB]", phase_label = "Fase [°]", title = "Diagrama de Bode")

fig = plt.gcf()  # Obtener la figura actual
ax_mag, ax_phase = fig.axes  # Los subplots son los ejes en la figura

# Personalizar la grilla y ticks de la magnitud
ax_mag.grid(which='both', linewidth=0.7, alpha=0.7)  # Personalizar la grilla
ax_mag.set_yticks([-100, -80, -60, -40, -20, 0, 20])  # Ajustar ticks principales


plt.show()

