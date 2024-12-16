import numpy as np
import matplotlib.pyplot as plt

# Parámetros de muestreo
T = 1/100  # Periodo de muestreo
N = 100    # Número de muestras
t = np.arange(N) * T  # Vector de tiempo

# Función para calcular la DFT y graficar
def calcular_dft(f1, f2, Nf, alpha, caso):
    # Definición de la señal en el dominio del tiempo
    x = np.cos(2 * np.pi * f1 * t) + np.cos(2 * np.pi * f2 * t)
    
    # Zero-padding si Nf > N
    if Nf > N:
        x = np.concatenate((x, np.zeros(Nf - N)))
    
    # Calcular la DFT de tamaño Nf
    Xf = np.fft.fft(x, Nf)
    freqs = np.fft.fftfreq(Nf, T)  # Frecuencias de la DFT
    
    # Graficar
    plt.figure(figsize=(10, 6))
    plt.stem(freqs[:Nf // 2], np.abs(Xf)[:Nf // 2])  # Eliminado use_line_collection
    plt.title(f'Caso {caso}: DFT de tamaño Nf = {Nf}, f1 = {f1} Hz, f2 = {f2} Hz')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('|X(f)|')
    plt.grid()

# Definición de los casos
alpha_values = [0, 0.5, 1, 5]  # Valores de alpha para cada caso

# Caso (a)
for alpha in alpha_values:
    f1 = 30.0
    f2 = f1 + alpha / (N * T)
    Nf = N
    calcular_dft(f1, f2, Nf, alpha, caso="a")

# Caso (b)
for alpha in alpha_values:
    f1 = 30.5
    f2 = f1 + alpha / (N * T)
    Nf = N
    calcular_dft(f1, f2, Nf, alpha, caso="b")

# Caso (c)
for alpha in alpha_values:
    f1 = 30.0
    f2 = f1 + alpha / (N * T)
    Nf = 10 * N  # Nf = 1000
    calcular_dft(f1, f2, Nf, alpha, caso="c")

# Caso (d)
for alpha in alpha_values:
    f1 = 30.5
    f2 = f1 + alpha / (N * T)
    Nf = 10 * N  # Nf = 1000
    calcular_dft(f1, f2, Nf, alpha, caso="d")

plt.show()
