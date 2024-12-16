import matplotlib.pyplot as plt #type: ignore
import numpy as np #type: ignore
import librosa #type: ignore


audio_file = 'interstellar.wav'
y, sr = librosa.load(audio_file)


NFFT = int(20480)       # Tamaño de la ventana
overlap = 0.9      # Solapamiento

noverlap = int(NFFT*overlap)
figsize = (10, 6)
plt.figure(figsize=figsize)
plt.specgram(y, Fs=sr, NFFT=NFFT, noverlap=noverlap, cmap='viridis', vmin=-110, vmax=-30)
plt.ylim(0, 500)
plt.colorbar(label='Intensidad (dB)')
plt.title('Espectrograma')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.tight_layout()
plt.show()
