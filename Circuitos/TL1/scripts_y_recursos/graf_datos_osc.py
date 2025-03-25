import numpy as np
import matplotlib.pyplot as plt
import glob

# Ruta de los archivos (ajusta según sea necesario)
file_pattern = "datos/SDS*.CSV"  
files = sorted(glob.glob(file_pattern))  # Obtener lista de archivos CSV

# Verificar si se encontraron archivos
if not files:
    print("No se encontraron archivos CSV.")
    exit()


# Procesar cada archivo
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        content = f.readlines()

    # Extraer solo las líneas con datos numéricos
    data_lines = content[10:]
    
    # Convertir los datos en una matriz NumPy
    data = np.genfromtxt(data_lines, delimiter=",", usecols=[3, 4])
    
    # Separar en vectores de tiempo y voltaje
    time = data[:, 0]
    voltage = data[:, 1]

    plt.figure(figsize=(10, 5))  # Configurar la figura

    # Graficar cada señal
    plt.plot(time, voltage, label=file.split("/")[-1])  

# Configurar la gráfica
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señales capturadas por el osciloscopio")
plt.legend(loc="upper right", fontsize="small")  # Muestra el nombre de cada archivo
plt.grid()

# Mostrar la gráfica
plt.show()

