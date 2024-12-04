import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

modo_de_operacion = 0 # 0 para usar la función, 1 para usar una archivo .txt separado por tabs

archivo_csv = 'primer_set.txt'

datos = pd.read_csv(archivo_csv, delimiter='\t')

def funcion(x):
    return -0.84*np.exp(-454.55*x)*(np.sin(2510.72*x))

if (modo_de_operacion == 0):
    x = np.linspace(0, 0.02, 1000)  # Rango para ver el comportamiento de la función
    y = funcion(x)
else:
    x = datos.iloc[:, 0]  # Primera columna
    y = datos.iloc[:, 1]  # Segunda columna

plt.plot(x, y, color='b')
plt.xlabel('t [s]')
plt.ylabel('V [V]')

# Ajustar límites en los ejes
plt.xlim(0, 0.0075)  # Mostrar desde 0 hasta 0.02 en x
plt.ylim(0, 0.055)  # Ajustar el rango en el eje y para ver el pico y el decaimiento

# Agregar líneas horizontales
plt.axhline(y=0.051, color='r', linestyle='--', label='$V_{H_{Max}}$')
plt.axhline(y=0.028, color='g', linestyle='--', label='$V_{H_{Min}}$')
plt.axhline(y=0.035, color='m', linestyle='--', label='$V_{H}$')

# Calcular el 10% y el 90% de 0.035
percent_10 = 0.1 * 0.035
percent_90 = 0.9 * 0.035

# Encontrar los índices donde la función alcanza el 10% y el 90%
x_10 = x[np.where(y >= percent_10)[0][0]]  # Primer índice donde y es mayor o igual a 10%
y_10 = y[np.where(y >= percent_10)[0][0]]  # Valor de la función en x_10

x_90 = x[np.where(y >= percent_90)[0][0]]  # Primer índice donde y es mayor o igual a 90%
y_90 = y[np.where(y >= percent_90)[0][0]]  # Valor de la función en x_90

# Agregar líneas verticales que solo lleguen hasta la función
line_color = 'orange'  # Color común para ambas líneas
plt.plot([x_10, x_10], [0, y_10], color=line_color, linestyle='--', label='10% y 90% de $V_H$')
plt.plot([x_90, x_90], [0, y_90], color=line_color, linestyle='--')

# Calcular la diferencia entre los tiempos
diferencia = x_90 - x_10

# Añadir texto para indicar la diferencia en notación matemática
plt.annotate(f'$t_r = {diferencia:.5f}$ s',
             xy=(0.0025, 0.02),
             fontsize=10, ha='left', color='black',
             bbox=dict(boxstyle='round', edgecolor='lightgray', facecolor='white'))

# Ajustar la cuadrícula en el eje y
#plt.yticks(np.arange(0, 0.056, 0.005))  # Marcas en el eje y con separación de 0.005

# Mostrar leyenda
plt.legend()

plt.grid(True)
plt.show()
