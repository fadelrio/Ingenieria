import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo txt
# Asegúrate de reemplazar 'archivo.txt' con la ruta de tu archivo
archivo1 = 'datos_medicion_TL1.txt'
datos1 = np.loadtxt(archivo1, delimiter=',')  # Cambiar delimiter si es necesario (e.g., ',')

archivo2 = 'datos_simulacion_formateado_TL1.txt'
datos2 = np.loadtxt(archivo2, delimiter=None)  # Cambiar delimiter si es necesario (e.g., ',')

# Asignar columnas a variables
frecuencia_hz1 = datos1[:, 0]  # Frecuencia [Hz]
decibeles1 = datos1[:, 1]   # Magnitud [dB]

# Asignar columnas a variables
frecuencia_rad_s2 = datos2[:, 0]  # Frecuencia [Hz]
decibeles2 = datos2[:, 1]   # Magnitud [dB]


# Gráfico de magnitud [dB]
plt.plot(frecuencia_hz1, decibeles1, label="Magnitud experimental [dB]", color='b')
plt.plot(frecuencia_rad_s2, decibeles2, linestyle="--", label="Magnitud simulada [dB]", color='r')
plt.xscale('log')  # Escala logarítmica para el eje x
plt.ylabel('Magnitud [dB]')
plt.title('Diagrama de Bode')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend()

# Mostrar el gráfico
plt.show()

