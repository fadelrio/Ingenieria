import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

# Función para modificar la velocidad de una señal
def change_speed(file_path, factor):
    # Leer el archivo .wav
    sample_rate, data = wavfile.read(file_path)
    
    # Si la señal es estéreo, convertirla a mono
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    
    # Cambiar la velocidad: nueva longitud basada en el factor
    new_length = int(len(data) / factor)
    modified_signal = resample(data, new_length)
    
    # Calcular el nuevo sample rate
    new_sample_rate = sample_rate
    
    return sample_rate, data, new_sample_rate, modified_signal

# Función para graficar señales antes y después de la modificación
def plot_signals(original_rate, original_signal, modified_rate, modified_signal, factor):
    time_original = np.linspace(0, len(original_signal) / original_rate, len(original_signal))
    time_modified = np.linspace(0, len(modified_signal) / modified_rate, len(modified_signal))

    # Graficar señal original
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time_original, original_signal, label="Señal original")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title("Señal original")
    plt.legend()
    plt.grid()
    
    # Graficar señal modificada
    plt.subplot(2, 1, 2)
    plt.plot(time_modified, modified_signal, color='orange', label=f"Señal modificada (Factor: {factor})")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title("Señal modificada")
    plt.legend()
    plt.grid()
    
    plt.tight_layout()

# Ruta del archivo .wav
file_path = "InASentimentalMood.wav" # Cambia por tu archivo específico

# Aumentar velocidad en un factor de 1.25
original_rate, original_signal, faster_rate, faster_signal = change_speed(file_path, factor=1.25)
print(f"Tasa de muestreo original: {original_rate} Hz, Tasa de muestreo nueva (rápida): {faster_rate} Hz")

# Disminuir velocidad en un factor de 0.75
_, _, slower_rate, slower_signal = change_speed(file_path, factor=0.75)
print(f"Tasa de muestreo original: {original_rate} Hz, Tasa de muestreo nueva (lenta): {slower_rate} Hz")

# Graficar los resultados
print("Señal con velocidad aumentada:")
plot_signals(original_rate, original_signal, faster_rate, faster_signal, factor=1.25)

print("Señal con velocidad disminuida:")
plot_signals(original_rate, original_signal, slower_rate, slower_signal, factor=0.75)

output_path = "senal_acelerada.wav"
wavfile.write(output_path, faster_rate, faster_signal.astype(np.int16))

output_path2 = "senal_ralentizada.wav"
wavfile.write(output_path2, faster_rate, slower_signal.astype(np.int16))

nperseg=2048
noverlap=1024
nfft=4096

# 5. Realizar el espectrograma de la señal completa
frequencies, times, Sxx = spectrogram(original_signal, fs=original_rate, window='hann', nperseg=nperseg, noverlap=noverlap, nfft=nfft)

#nperseg: resolucion en tiempo y recuencia. Achicarlo me sube la resolucion en tiempo porque achica el tamaño de las ventanas No puede ser mas grande que la señal 
#noverlap: cuanto (en general en porcentaje) se solapan las ventanas. Suaviza la señal
#nfft: resolucion en frecuencia (debe ser mas grande que nperseg para que surta efecto).
#zero padding: nfft - nperseg. Cuantos 0s agregue en frecuenca para subirle la resolucion, no es un parametro pero sirve para saber que estas haciendo con los valores

# Graficar el espectrograma
fig4= plt.figure()
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud', vmin = -120, vmax =60)
plt.colorbar(label='Intensidad [dB]')
plt.title("Espectrograma de InASentimentalMood")
plt.xlabel("Tiempo [s]")
plt.ylabel("Frecuencia [Hz]")
plt.ylim([0, 3000])  # Limitar a el eje d frec para mejor visualización

#Realizar el espectograma de la señal acelerada (decimada) en un factor de 1.25
frequencies, times, Sxx = spectrogram(faster_signal, fs=faster_rate, window= 'hann', nperseg=nperseg, noverlap=noverlap, nfft=nfft)


# Graficar el espectrograma de la señal decimada
fig5= plt.figure()
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud',vmin = -120, vmax =60)
plt.colorbar(label='Intensidad [dB]')
plt.title("Espectrograma de InASentimentalMood decimada en un factor de 1.25")
plt.xlabel("Tiempo [s]")
plt.ylabel("Frecuencia [Hz]")
plt.ylim([0, 3000])  # Limitar a el eje d frec para mejor visualización


#Realizar el espectograma de la señal ralentizada (interpolada) en un factor de 0.75
frequencies, times, Sxx = spectrogram(slower_signal, fs=slower_rate, window= 'hann', nperseg=nperseg, noverlap=noverlap, nfft=nfft)


# Graficar el espectrograma de la señal interpolada
fig5= plt.figure()
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud',vmin = -120, vmax =60)
plt.colorbar(label='Intensidad [dB]')
plt.title("Espectrograma de InASentimentalMood interpolada en un factor de 0.75")
plt.xlabel("Tiempo [s]")
plt.ylabel("Frecuencia [Hz]")
plt.ylim([0, 3000])  # Limitar a el eje d frec para mejor visualización
plt.show()

