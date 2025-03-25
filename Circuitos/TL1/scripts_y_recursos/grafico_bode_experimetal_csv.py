import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo txt
# Asegúrate de reemplazar 'archivo.txt' con la ruta de tu archivo
archivo1 = 'datos_medicion_TL1.txt'
datos1 = np.loadtxt(archivo1, delimiter=",")  # Cambiar delimiter si es necesario (e.g., ',')


# Asignar columnas a variables
frecuencia_hz1 = datos1[:, 0]  # Frecuencia [Hz]
decibeles1 = datos1[:, 1]   # Magnitud [dB]
#fase1 = datos1[:, 2]        # Fase [°]



# Convertir la frecuencia de Hz a radianes por segundo [rad/s] #######################PREGUNTAR SI USAMOS HZ O RAD/S############################
#frecuencia_rad_s1 = 2 * np.pi * frecuencia_hz1


plt.plot(frecuencia_hz1, decibeles1, label="Magnitud experimental [dB]", color='b')
plt.xscale('log')  # Escala logarítmica para el eje x
plt.ylabel('Magnitud [dB]')
plt.title('Diagrama de Bode')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend()

plt.show()
