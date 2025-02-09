import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Definir la función de transferencia
# Ejemplo: G(s) = -200s / (s^2 + 150s + 10000)
numerador = [15000,105000]  # Coeficientes del numerador (2,1,0)
denominador = [1, 40, 22800, 225000]  # Coeficientes del denominador (2,1,0)
G = ctrl.TransferFunction(numerador, denominador)

# Calcular el diagrama de Bode (sin graficar automáticamentase) (corregir el omega para que coincida con la zona de interés)
frecuencia, ganancia, fase = ctrl.bode_plot(G,omega=[1,100000] , dB=True, Hz=False, deg=True, plot=True, freq_label = "Frecuencia [rad/s]", magnitude_label = "Magnitud [dB]", phase_label = "Fase [°]", title = "Diagrama de Bode")

fig = plt.gcf()  # Obtener la figura actual
ax_mag, ax_phase = fig.axes  # Los subplots son los ejes en la figura

# Personalizar la grilla y ticks de la magnitud
#ax_mag.grid(which='both', linewidth=0.7, alpha=0.7)  # Personalizar la grilla
#ax_mag.set_yticks([-40,-20,0,20])  # Ajustar ticks principales


plt.show()

