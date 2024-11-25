import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo txt
# Asegúrate de reemplazar 'archivo.txt' con la ruta de tu archivo
archivo1 = 'bode_ltspice_set2_formateado.txt'
datos1 = np.loadtxt(archivo1, delimiter=None)  # Cambiar delimiter si es necesario (e.g., ',')

archivo2 = 'bode_teorico_set2.txt'
datos2 = np.loadtxt(archivo2, delimiter=None)  # Cambiar delimiter si es necesario (e.g., ',')

# Asignar columnas a variables
frecuencia_hz1 = datos1[:, 0]  # Frecuencia [Hz]
decibeles1 = datos1[:, 1]   # Magnitud [dB]
fase1 = datos1[:, 2]        # Fase [°]

# Convertir la frecuencia de Hz a radianes por segundo [rad/s]
frecuencia_rad_s1 = 2 * np.pi * frecuencia_hz1

# Asignar columnas a variables
frecuencia_rad_s2 = datos2[:, 0]  # Frecuencia [Hz]
decibeles2 = datos2[:, 1]   # Magnitud [dB]
fase2 = datos2[:, 2]        # Fase [°]

# Crear la figura y los ejes
fig, ax1 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Gráfico de magnitud [dB]
ax1[0].plot(frecuencia_rad_s1, decibeles1, label="Magnitud simulada [dB]", color='b')
ax1[0].plot(frecuencia_rad_s2, decibeles2, linestyle="--", label="Magnitud teórica [dB]", color='r')
ax1[0].set_xscale('log')  # Escala logarítmica para el eje x
ax1[0].set_ylabel('Magnitud [dB]')
ax1[0].set_title('Diagrama de Bode')
ax1[0].grid(True, which="both", linestyle='--', linewidth=0.5)
ax1[0].legend()

# Gráfico de fase [°]
ax1[1].plot(frecuencia_rad_s1, fase1, label="Fase simulada [°]", color='b')
ax1[1].plot(frecuencia_rad_s2, fase2, linestyle="--", label="Fase teórica [°]", color='r')
ax1[1].set_xscale('log')  # Escala logarítmica para el eje x
ax1[1].set_xlabel('Frecuencia [rad/s]')
ax1[1].set_ylabel('Fase [°]')
ax1[1].grid(True, which="both", linestyle='--', linewidth=0.5)
ax1[1].legend()

# Ajustar espaciado
plt.tight_layout()

# Mostrar el gráfico
plt.show()

