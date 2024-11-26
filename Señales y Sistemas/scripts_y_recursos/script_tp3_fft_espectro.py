import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import spectrogram, butter, filtfilt

# 1. Cargar el archivo de audio
audio_file = "nota_musical_1_filtrada.wav"  # Cambiar por el nombre del archivo
signal, sample_rate = sf.read(audio_file)


# Realizar la FFT
N = len(signal)
fft_signal = np.fft.fft(signal)
frecuencias= np.fft.fftfreq(len(signal), 1 / sample_rate)

# Solo tomamos la mitad positiva del espectro
frecuencias = frecuencias[:N // 2]
fft_signal = np.abs(fft_signal[:N // 2])


# Graficar la FFT
fig3= plt.figure()
#plt.subplot(3, 1, 3)
plt.plot(frecuencias, fft_signal, color= 'green')
plt.title("FFT del primer fragmento")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Amplitud")
plt.grid()
plt.tight_layout()
plt.show()


#cuando se cambian no se puede multiplicar pq te los da en float y se rompe, cambiar con el numero directo
#si queres hacer el de una ventana chica ojo con el nperseg
nperseg=2048
noverlap=1024
nfft=4096

# 5. Realizar el espectrograma de la señal completa
frequencies, times, Sxx = spectrogram(signal, fs=sample_rate, window='hann', nperseg=nperseg, noverlap=noverlap, nfft=nfft)

#nperseg: resolucion en tiempo y recuencia. Achicarlo me sube la resolucion en tiempo porque achica el tamaño de las ventanas No puede ser mas grande que la señal 
#noverlap: cuanto (en general en porcentaje) se solapan las ventanas. Suaviza la señal
#nfft: resolucion en frecuencia (debe ser mas grande que nperseg para que surta efecto).
#zero padding: nfft - nperseg. Cuantos 0s agregue en frecuenca para subirle la resolucion, no es un parametro pero sirve para saber que estas haciendo con los valores

#tiempo_ajustado= times+inicio_segundos #es para que este bien el tiempo en el eje del espectograma

# Graficar el espectrograma
fig4= plt.figure()
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.colorbar(label='Intensidad [dB]')
plt.title("Espectrograma del primer fragmento")
plt.xlabel("Tiempo [s]")
plt.ylabel("Frecuencia [Hz]")
plt.ylim([0, 3000])  # Limitar a el eje d frec para mejor visualización
plt.show()

