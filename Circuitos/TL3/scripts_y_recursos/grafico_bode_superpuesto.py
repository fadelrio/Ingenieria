import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo txt
# Asegúrate de reemplazar 'archivo.txt' con la ruta de tu archivo
archivo1 = 'valores_medidos_frec_x10.csv'
datos1 = np.loadtxt(archivo1, delimiter=',')  # Cambiar delimiter si es necesario (e.g., ',')

archivo2 = 'valores_simulados_frec_real_formateado.txt'
datos2 = np.loadtxt(archivo2, delimiter=None)  # Cambiar delimiter si es necesario (e.g., ',')

archivo3 = 'valores_medidos_frec_pta_activa.csv'
datos3 = np.loadtxt(archivo3, delimiter=',')  # Cambiar delimiter si es necesario (e.g., ',')


# Asignar columnas a variables
frecuencia_hz1 = datos1[:, 0]  # Frecuencia [Hz]
vi = datos1[:, 1]   # Magnitud [dB]
vo = datos1[:, 2]
decibeles1 = 20*np.log10(vo/vi)

# Asignar columnas a variables
frecuencia_hz3 = datos3[:, 0]  # Frecuencia [Hz]
vi3 = datos3[:, 1]   # Magnitud [dB]
vo3 = datos3[:, 2]
decibeles3 = 20*np.log10(vo3/vi3)

# Asignar columnas a variables
frecuencia_rad_s2 = datos2[:, 0]  # Frecuencia [Hz]
decibeles2 = datos2[:, 1]   # Magnitud [dB]


# Gráfico de magnitud [dB]
#plt.plot(frecuencia_hz1, decibeles1, label="Magnitud experimental [dB] (Punta de osc x10)", color='b')
plt.plot(frecuencia_rad_s2, decibeles2, label="Magnitud simulada [dB]", color='r')
#plt.plot(frecuencia_hz3, decibeles3, label="Magnitud experimental [dB] (Punta activa)", color= 'g')
plt.xscale('log')  # Escala logarítmica para el eje x
plt.ylabel('Magnitud [dB]')
plt.ylim([5,25])
plt.xlim([50,10e8])
plt.title('Diagrama de Bode')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend()

# Mostrar el gráfico
plt.show()

