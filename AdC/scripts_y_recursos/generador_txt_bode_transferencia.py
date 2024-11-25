import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

# Definir un sistema de ejemplo (puedes reemplazar esto con el sistema que quieras)
# Por ejemplo, un sistema de primer orden: G(s) = 1 / (s + 1)
num = [28181982]
den = [1, 11366.664, 8075065]
system = ctrl.TransferFunction(num, den)

# Generar las frecuencias en radianes por segundo entre 100 y 150000 rad/s
frequencies = np.logspace(np.log10(100), np.log10(150000), num=1000)  # Frecuencias entre 100 y 150k rad/s

# Realizar el análisis de Bode utilizando bode_plot
mag, phase, omega = ctrl.bode_plot(system, omega=[100,150000] , dB=True, Hz=False, deg=True, plot=False)

# Convertir la magnitud de Bode a dB
mag_db = 20 * np.log10(mag)

# Convertir la fase a grados
phase_deg = np.degrees(phase)

# Crear el archivo .txt y escribir los datos
with open('bode_teorico_set3.txt', 'w') as file:
    file.write('Frecuencia (rad/s)\tMagnitud (dB)\tFase (grados)\n')
    for i in range(len(omega)):
        file.write(f'{omega[i]}\t{mag_db[i]}\t{phase_deg[i]}\n')

print("Análisis de Bode guardado en 'bode_analysis.txt'.")


