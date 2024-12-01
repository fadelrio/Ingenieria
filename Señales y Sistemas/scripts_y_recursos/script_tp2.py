import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import spectrogram, butter, filtfilt

# 1. Cargar el archivo de audio
audio_file = r"C:\Users\martu\OneDrive\Documentos\Tpsys\InASentimentalMood.wav"  # Cambiar por el nombre del archivo
signal, sample_rate = sf.read(audio_file)

# Información básica del audio
print(f"Frecuencia de muestreo: {sample_rate} Hz")
#print(f"Duración: {len(signal) / sample_rate:.2f} segundos")

# 2. Definir una ventana para seleccionar una porción del audio
inicio_segundos = 12   # Tiempo de inicio de la ventana en segundos
duracion_segundos = 1   # Duración de la ventana en segundos
inicio_muestra = int(inicio_segundos * sample_rate)
fin_muestra = int(inicio_muestra + duracion_segundos * sample_rate)

# Extraer la porción de la señal utilizando la ventana
ventana_signal = signal[inicio_muestra:fin_muestra]

# 3. Graficar la señal completa y la sección seleccionada
tiempo_total = np.arange(len(signal)) / sample_rate
tiempo_ventana = np.arange(len(ventana_signal)) / sample_rate + inicio_segundos
""""
fig1 = plt.figure()
#plt.subplot(3, 1, 1) esto te las graficaba todas en el mismo grafico
plt.plot(tiempo_total, signal)
plt.title("Señal de Audio Completa")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.grid()

"""
fig2= plt.figure()
#plt.subplot(3, 1, 2)
plt.plot(tiempo_ventana, ventana_signal, color='darkorange')
plt.title("Una nota")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.grid()

# 4. Calcular la FFT de la sección seleccionada
N = len(ventana_signal)
fft_signal = np.fft.fft(ventana_signal)
frecuencias = np.fft.fftfreq(N, d=1/sample_rate)

# Solo tomamos la mitad positiva del espectro
frecuencias = frecuencias[:N // 2]
fft_signal = np.abs(fft_signal[:N // 2])

"""
# Graficar la FFT
fig3= plt.figure()
#plt.subplot(3, 1, 3)
plt.plot(frecuencias, fft_signal, color= 'green')
plt.title("Espectro de frecuencias del saxofón")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Amplitud")
plt.grid()
plt.tight_layout()
plt.show()
 """
#cuando se cambian no se puede multiplicar pq te los da en float y se rompe, cambiar con el numero directo
#si queres hacer el de una ventana chica ojo con el nperseg
nperseg=2048
noverlap=1024
nfft=4096

# 5. Realizar el espectrograma de la señal completa
frequencies, times, Sxx = spectrogram(ventana_signal, fs=sample_rate, window='hann', nperseg=nperseg, noverlap=noverlap, nfft=nfft)

#nperseg: resolucion en tiempo y recuencia. Achicarlo me sube la resolucion en tiempo porque achica el tamaño de las ventanas No puede ser mas grande que la señal 
#noverlap: cuanto (en general en porcentaje) se solapan las ventanas. Suaviza la señal
#nfft: resolucion en frecuencia (debe ser mas grande que nperseg para que surta efecto).
#zero padding: nfft - nperseg. Cuantos 0s agregue en frecuenca para subirle la resolucion, no es un parametro pero sirve para saber que estas haciendo con los valores

tiempo_ajustado= times+inicio_segundos #es para que este bien el tiempo en el eje del espectograma

# Graficar el espectrograma
fig4= plt.figure()
plt.pcolormesh(tiempo_ajustado, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.colorbar(label='Intensidad [dB]')
plt.title("Espectrograma del saxofón en InASentimentalMood")
plt.xlabel("Tiempo [s]")
plt.ylabel("Frecuencia [Hz]")
plt.ylim([0, 3000])  # Limitar a el eje d frec para mejor visualización
plt.show()


# 1. Función para aplicar un filtro Butterworth usando filtfilt
def butter_lowpass_filter(data, cutoff, fs, order=4):
    
    """"
    Aplica un filtro pasabajos Butterworth a una señal usando filtfilt para evitar el desfase.
    
    Parámetros:
    - data: La señal de entrada.
    - cutoff: Frecuencia de corte del filtro (en Hz).
    - fs: Frecuencia de muestreo de la señal (en Hz).
    - order: Orden del filtro Butterworth.
    
    Retorna:
    - Señal filtrada sin desfase.
    """

    nyquist = 0.5 * fs  # Frecuencia de Nyquist
    normal_cutoff = cutoff / nyquist  # Frecuencia de corte normalizada porque la funcion butter usa valores entre 0 y 1, siendo 1 la frec de nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    
    # Usamos filtfilt para filtrar la señal en ambas direcciones y evitar desfase
    filtered_signal = filtfilt(b, a, data)
    return filtered_signal

filtered_signal = butter_lowpass_filter(ventana_signal, cutoff=500, fs=sample_rate)

#grafica en tiempo la señal filtrada
#tiempo = np.arange(len(ventana_signal)) / sample_rate no sirve lol
fig5=plt.figure()
plt.plot(tiempo_ventana, filtered_signal, color='orange')
plt.title('Señal de una Nota Filtrada con Filtro Butterworth (Corte = 500 Hz)')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid()
plt.show()

#calcula el espectograma de la señal filtrada
frequencies, times, Sxx = spectrogram(filtered_signal, fs=sample_rate, window='hann', nperseg=nperseg, noverlap=noverlap, nfft=nfft)

#grafica el espectograma filtrado    
fig6=plt.figure()
plt.pcolormesh(tiempo_ajustado, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.colorbar(label='Intensidad [dB]')
plt.title('Espectrograma de la Nota Filtrada (Corte = 500 Hz)')
plt.xlabel('Tiempo [s]')
plt.ylabel('Frecuencia [Hz]')
plt.ylim([0, 3000])  # Limitar el eje d frec para mejor visualización
plt.show()