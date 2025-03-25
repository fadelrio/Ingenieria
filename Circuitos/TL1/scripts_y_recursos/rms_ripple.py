import numpy as np
import glob

# Ruta de los archivos (ajusta según sea necesario)
file_pattern = "datos/SDS*.CSV"
files = sorted(glob.glob(file_pattern))  # Obtener lista de archivos CSV

# Archivos específicos que queremos procesar (7, 8 y 11)
indices = [8, 9]  # Python usa índices desde 0
selected_files = [files[i] for i in indices]

# Funciones para calcular RMS y valor medio
def calcular_rms(voltage):
    return np.sqrt(np.mean(np.square(voltage)))

def calcular_valor_medio(voltage):
    return np.mean(voltage)

# Procesar cada archivo seleccionado
for file in selected_files:
    with open(file, "r", encoding="utf-8") as f:
        content = f.readlines()

    # Extraer solo las líneas con datos numéricos
    data_lines = content[10:]

    # Convertir los datos en una matriz NumPy
    data = np.genfromtxt(data_lines, delimiter=",", usecols=[3, 4])
    
    # Separar voltaje (toda la señal)
    voltage = data[:, 1]

    # Calcular el valor medio
    valor_medio = calcular_valor_medio(voltage)

    # Restar el valor medio a toda la señal
    voltage_sin_dc = voltage - valor_medio

    # Calcular el RMS después de eliminar el DC
    rms_value = calcular_rms(voltage_sin_dc)

    # Mostrar resultados
    print(f"Archivo: {file.split('/')[-1]}")
    print(f"  - Valor medio en toda la señal: {valor_medio:.6f} V")
    print(f"  - Valor eficaz (RMS) después de restar el valor medio: {rms_value:.6f} V\n")

