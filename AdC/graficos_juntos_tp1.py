import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Modo de operación:
# 0 - Graficar ambas funciones
# 1 - Graficar ambos sets de archivos .txt
# 2 - Graficar la función 1 con el primer set de archivo .txt
# 3 - Graficar la función 2 con el segundo set de archivo .txt
modo_de_operacion = 2

# Archivos de datos
archivo_csv1 = 'primer_set.txt'
archivo_csv2 = 'segundo_set.txt'

# Funciones para cada conjunto de datos
def funcion1(x):
    return np.exp(-2500*x)*(-0.035*np.cos(400*np.pi*x) - 0.0696*np.sin(400*np.pi*x)) + 0.035

def funcion2(x):
    return np.exp(-2500*x)*(-0.035*np.cos(12*np.pi*x) - 2.32*np.sin(12*np.pi*x)) + 0.035

# Graficar según el modo de operación
if modo_de_operacion == 0:
    # Graficar usando ambas funciones
    x1 = np.linspace(0, 0.02, 1000)  # Rango para la función 1
    x2 = np.linspace(0, 0.02, 1000)  # Rango para la función 2
    y1 = funcion1(x1)
    y2 = funcion2(x2)
elif modo_de_operacion == 1:
    # Graficar usando ambos sets de archivos .txt
    datos1 = pd.read_csv(archivo_csv1, delimiter='\t')
    datos2 = pd.read_csv(archivo_csv2, delimiter='\t')
    
    x1 = datos1.iloc[:, 0]  # Primera columna del primer set
    y1 = datos1.iloc[:, 1]  # Segunda columna del primer set
    
    x2 = datos2.iloc[:, 0]  # Primera columna del segundo set
    y2 = datos2.iloc[:, 1]  # Segunda columna del segundo set
elif modo_de_operacion == 2:
    # Graficar la función 1 con el primer set del archivo .txt
    x1 = np.linspace(0, 0.02, 1000)  # Rango para la función 1
    y1 = funcion1(x1)
    
    datos1 = pd.read_csv(archivo_csv1, delimiter='\t')
    x2 = datos1.iloc[:, 0]  # Primera columna del primer set
    y2 = datos1.iloc[:, 1]  # Segunda columna del primer set
elif modo_de_operacion == 3:
    # Graficar la función 2 con el segundo set del archivo .txt
    x1 = np.linspace(0, 0.02, 1000)  # Rango para la función 2
    y1 = funcion2(x1)
    
    datos2 = pd.read_csv(archivo_csv2, delimiter='\t')
    x2 = datos2.iloc[:, 0]  # Primera columna del segundo set
    y2 = datos2.iloc[:, 1]  # Segunda columna del segundo set

# Graficar ambos conjuntos en el mismo gráfico
if modo_de_operacion == 0:
    plt.plot(x1, y1, color='b', label='Función set 1')
    plt.plot(x2, y2, color='r', label='Función set 2')
elif modo_de_operacion == 1:
    plt.plot(x1, y1, color='b', label='Función set 1')
    plt.plot(x2, y2, color='r', label='Función set 2')
elif modo_de_operacion == 2:
    plt.plot(x1, y1, color='b', label='Función hipotética')
    plt.plot(x2, y2, color='r', label='Función simulada')
elif modo_de_operacion == 3:
    plt.plot(x1, y1, color='b', label='Función hipotética')
    plt.plot(x2, y2, color='r', label='Función simulada')

# Líneas horizontales
plt.axhline(y=0.035, color='g', linestyle='--', label='$V_{H}$')

# Etiquetas y configuración
plt.xlabel('t [s]')
plt.ylabel('V [V]')
plt.xlim(0.0005, 0.003)
plt.ylim(0.015, 0.04)

# Ajustar la cuadrícula en el eje y
plt.yticks(np.arange(0.015, 0.041, 0.005))  # Marcas en el eje y con separación de 0.005

# Mostrar leyenda
plt.legend(loc='lower right')

# Mostrar cuadrícula
plt.grid(True)

# Mostrar gráfico
plt.show()
