import numpy as np
import matplotlib.pyplot as plt
import librosa as lib
from scipy.io import wavfile as waves
from scipy.signal import spectrogram
import soundfile as sf


audio_iasm = "InASentimentalMood.wav"

# Cargar la data en la matriz, con su frecuencia de muestreo Fs
Fs, data_iasm = waves.read(audio_iasm)

Ts = 1 / Fs  # T sample 1
time_iasm = Ts * np.arange(0, len(data_iasm))

plt.figure()
plt.plot(time_iasm,data_iasm)
plt.title("In a sentimental mood")

# Normalización de la señal
data_iasm_normalizada = data_iasm / np.max(np.abs(data_iasm), axis=0)

data_iasm_harmonic, data_iasm_percussive =lib.effects.hpss(data_iasm_normalizada)

plt.figure()
plt.plot(time_iasm,data_iasm_harmonic)
plt.title("In a sentimental mood - Componentes armónicos")

plt.figure()
plt.plot(time_iasm,data_iasm_percussive)
plt.title("In a sentimental mood - Componentes percusivos")

plt.figure()
f, t_spec, Sxx = spectrogram(data_iasm, fs=Fs, window='hann', nperseg=8192, noverlap=2048)
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
plt.title("Espectograma de In a sentimental mood")
plt.ylim(0, 5000)
plt.ylabel('Frecuencia [Hz]')
plt.xlabel('Tiempo [s]')
plt.colorbar(label='Intensidad [dB]')

plt.figure()
f, t_spec, Sxx = spectrogram(data_iasm_harmonic, fs=Fs, window='hann', nperseg=8192, noverlap=2048)
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
plt.title("Espectograma de In a sentimental mood - Componentes armónicos")
plt.ylim(0, 5000)
plt.ylabel('Frecuencia [Hz]')
plt.xlabel('Tiempo [s]')
plt.colorbar(label='Intensidad [dB]')

plt.figure()
f, t_spec, Sxx = spectrogram(data_iasm_percussive, fs=Fs, window='hann', nperseg=8192, noverlap=2048)
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
plt.title("Espectograma de In a sentimental mood - Componentes percusivos")
plt.ylim(0, 5000)
plt.ylabel('Frecuencia [Hz]')
plt.xlabel('Tiempo [s]')
plt.colorbar(label='Intensidad [dB]')

sf.write("InASentimentalMood_armonicos.wav", data_iasm_harmonic, Fs)
sf.write("InASentimentalMood_percusivos.wav", data_iasm_percussive, Fs)

plt.show()