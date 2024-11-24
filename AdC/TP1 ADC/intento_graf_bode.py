import numpy as np
import matplotlib.pyplot as plt

# Cargar datos del archivo txt
def cargar_datos(archivo):
    try:
        # Leer archivo con 3 columnas: frecuencia, magnitud (dB), fase (grados)
        datos = np.loadtxt(archivo, skiprows=1)  # Omitir encabezado
        frecuencia = datos[:, 0]  # Primera columna: frecuencia (Hz)
        magnitud = datos[:, 1]    # Segunda columna: magnitud (dB)
        fase = datos[:, 2]        # Tercera columna: fase (grados)
        return frecuencia, magnitud, fase
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None, None, None

# Graficar magnitud en escala semilogarítmica
def graficar_magnitud(frecuencia, magnitud):
    plt.figure(figsize=(10, 6))
    plt.semilogx(frecuencia, magnitud, label='Magnitud (dB)', color='b')
    plt.xlabel('Frecuencia (Hz)', fontsize=12)
    plt.ylabel('Magnitud (dB)', fontsize=12)
    plt.title('Diagrama de Bode - Magnitud', fontsize=14)
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Graficar fase en escala semilogarítmica
def graficar_fase(frecuencia, fase):
    plt.figure(figsize=(10, 6))
    plt.semilogx(frecuencia, fase, label='Fase (°)', color='r')
    plt.xlabel('Frecuencia (Hz)', fontsize=12)
    plt.ylabel('Fase (°)', fontsize=12)
    plt.title('Diagrama de Bode - Fase', fontsize=14)
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Archivo .txt con los datos de LTspice (modificar según tu archivo)
archivo = "Draft_tp3.txt"

# Cargar los datos del archivo
frecuencia, magnitud, fase = cargar_datos(archivo)

# Verificar si se cargaron correctamente los datos
if frecuencia is not None and magnitud is not None and fase is not None:
    # Graficar magnitud y fase
    graficar_magnitud(frecuencia, magnitud)
    graficar_fase(frecuencia, fase)
else:
    print("No se pudo cargar y graficar los datos.")

