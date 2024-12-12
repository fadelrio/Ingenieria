import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

sample_rate = 400
tiempo = np.arange(0, 1, 1/sample_rate)

senal_1 = np.cos(2*np.pi*100*tiempo)
senal_2 = (1 + np.cos(2*np.pi*10*tiempo))*np.cos(2*np.pi*100*tiempo)
senal_3 = np.cos(2*np.pi*100*tiempo*tiempo)

senales = [senal_1, senal_2, senal_3]

nperseg=50
noverlap=25
nfft=50

for senal in senales:
    frequencies, times, Sxx = spectrogram(senal, fs=sample_rate, window='hann', nperseg=nperseg, noverlap=noverlap,nfft=nfft)

    # nperseg: resolucion en tiempo y recuencia. Achicarlo me sube la resolucion en tiempo porque achica el tamaño de las ventanas No puede ser mas grande que la señal
    # noverlap: cuanto (en general en porcentaje) se solapan las ventanas. Suaviza la señal
    # nfft: resolucion en frecuencia (debe ser mas grande que nperseg para que surta efecto).
    # zero padding: nfft - nperseg. Cuantos 0s agregue en frecuenca para subirle la resolucion, no es un parametro pero sirve para saber que estas haciendo con los valores

    # Graficar el espectrograma
    fig4 = plt.figure()
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud', vmin=-120, vmax=-20)
    plt.colorbar(label='Intensidad [dB]')
    plt.title(f"Espectrograma de señal")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frecuencia [Hz]")
    #plt.ylim([0, 900])  # Limitar a el eje d frec para mejor visualización

plt.show()