import numpy as np
import scipy.signal as signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Función para crear el filtro pasabanda
def create_bandpass_filter(fs, center_freq, bandwidth, num_multiples=3):
    # Generar las frecuencias de corte de los filtros
    freqs = []
    for i in range(1, num_multiples + 1):
        low = center_freq * i - bandwidth / 2
        high = center_freq * i + bandwidth / 2
        freqs.append((low, high))
    
    # Combinar los filtros en uno solo
    b, a = signal.butter(4, [f[0] / (fs / 2) for f in freqs] + [f[1] / (fs / 2) for f in freqs], btype='bandpass')
    
    return b, a

# Función para aplicar el filtro a la señal de audio
def apply_filter(audio_data, fs, filter_b, filter_a):
    # Si el audio es estéreo (tiene más de un canal), aplicamos el filtro por separado a cada canal
    if audio_data.ndim > 1:
        filtered_signal = np.zeros_like(audio_data)
        for i in range(audio_data.shape[1]):  # Para cada canal
            filtered_signal[:, i] = signal.filtfilt(filter_b, filter_a, audio_data[:, i])
    else:
        filtered_signal = signal.filtfilt(filter_b, filter_a, audio_data)
    
    return filtered_signal

# Leer archivo WAV
def read_wav(filename):
    fs, data = wavfile.read(filename)
    return fs, data

# Guardar archivo WAV
def save_wav(filename, fs, data):
    # Si el audio es estéreo, convertimos a 16 bits
    wavfile.write(filename, fs, data.astype(np.int16))

# Función para calcular la FFT y la frecuencia correspondiente
def compute_fft(signal, fs):
    n = len(signal)
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(n, d=1/fs)
    return fft_freq[:n//2], np.abs(fft_result)[:n//2]  # Devolver solo la parte positiva de la FFT

# Principal
if __name__ == "__main__":
    input_file = 'nota_musical_1.wav'  # Ruta del archivo de entrada
    output_file = 'nota_musical_1_filtrada.wav'  # Ruta del archivo de salida
    
    # Leer archivo de audio
    fs, audio_data = read_wav(input_file)
    
    # Parámetros del filtro
    center_freq = 369  # Frecuencia central en Hz
    bandwidth = 10  # Ancho de banda en Hz (de 364 Hz a 374 Hz)
    
    # Crear el filtro pasabanda
    b, a = create_bandpass_filter(fs, center_freq, bandwidth)
    
    # Aplicar el filtro a la señal
    filtered_data = apply_filter(audio_data, fs, b, a)
    
    # Guardar la señal filtrada
    save_wav(output_file, fs, filtered_data)
    
    print(f"Filtro aplicado y archivo guardado en: {output_file}")

    # Calcular FFT de las señales (tomamos un solo canal para la FFT si es estéreo)
    if audio_data.ndim > 1:
        fft_freq, fft_original = compute_fft(audio_data[:, 0], fs)  # Tomamos el primer canal
        fft_filtered = compute_fft(filtered_data[:, 0], fs)  # Tomamos el primer canal de la señal filtrada
    else:
        fft_freq, fft_original = compute_fft(audio_data, fs)
        fft_filtered = compute_fft(filtered_data, fs)

    # Mostrar la señal original y filtrada en el dominio del tiempo
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(audio_data[:1000, 0] if audio_data.ndim > 1 else audio_data[:1000], label='Original')
    plt.title('Señal Original')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    
    plt.subplot(2, 2, 2)
    plt.plot(filtered_data[:1000, 0] if filtered_data.ndim > 1 else filtered_data[:1000], label='Filtrada', color='r')
    plt.title('Señal Filtrada')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    
    # Mostrar FFT de la señal original y filtrada
    plt.subplot(2, 2, 3)
    plt.plot(fft_freq, fft_original, label='FFT Original')
    plt.title('FFT de la Señal Original')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    
    plt.subplot(2, 2, 4)
    plt.plot(fft_freq, fft_filtered, label='FFT Filtrada', color='r')
    plt.title('FFT de la Señal Filtrada')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    
    plt.tight_layout()
    plt.show()

