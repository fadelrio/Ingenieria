import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

# Cargar el archivo de audio
# Cambia la ruta por la ubicación del archivo "InASentimentalMood.wav"
audio_path = "InASentimentalMood.wav"
signal, sr = librosa.load(audio_path, sr=None)  # signal es la señal de audio, sr es la tasa de muestreo

# Función para modificar la velocidad utilizando phase_vocoder
def cambiar_velocidad_phase_vocoder(signal, factor, sr):
    """
    Cambia la velocidad de una señal de audio sin alterar su tono utilizando phase_vocoder.

    Parámetros:
        signal (array): Señal de audio.
        factor (float): Factor de cambio de velocidad (mayor a 1 acelera, menor a 1 desacelera).
        sr (int): Tasa de muestreo.

    Retorno:
        signal_out (array): Señal de audio con velocidad ajustada.
    """
    D = librosa.stft(signal)
    t_nuevo = librosa.times_like(D)
    k=factor

    d_vocoder = librosa.phase_vocoder(D,rate=k,hop_length=None, n_fft=None)
    signal_out = librosa.istft(d_vocoder)
    """
    # Transformar al dominio del tiempo-frecuencia
    D = librosa.stft(signal)  # Cálculo de la Transformada de Fourier de tiempo corto (STFT)
    D_modificado = librosa.phase_vocoder(D, factor, hop_length = None, n_fft= None)  # Ajustar la velocidad
    signal_out = librosa.istft(D_modificado)  # Convertir de nuevo al dominio temporal
    """
    return signal_out
    
# Cambiar la velocidad de la señal
factor_acelerado = 1.25  # Factor para acelerar
factor_desacelerado = 0.75  # Factor para desacelerar

# Generar señales modificadas
signal_acelerado = cambiar_velocidad_phase_vocoder(signal, factor_acelerado, sr)
signal_desacelerado = cambiar_velocidad_phase_vocoder(signal, factor_desacelerado, sr)


# Graficar señales
def graficar_señales(original, modificada, sr, titulo):
    """
    Genera un gráfico comparativo entre la señal original y la señal modificada.

    Parámetros:
        original (array): Señal original.
        modificada (array): Señal modificada.
        sr (int): Tasa de muestreo.
        titulo (str): Título del gráfico.
    """
    # Convertir señales en numpy.ndarray si no lo son
   # original = np.array(original, dtype=np.float32)
   # modificada = np.array(modificada, dtype=np.float32)
    
    
    plt.subplots(2, 1, figsize=(8, 6), sharex=True)  # 2 filas, 1 columna
    # Señal original
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(original, sr=sr, alpha=0.8)
    plt.title("Señal Original")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()
    
    # Señal modificada
    #fig2 = plt.figure()
    plt.subplot(2, 1, 2)
    librosa.display.waveshow(modificada, sr=sr, alpha=0.8, color = 'orange')
    plt.title(titulo)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()

    plt.tight_layout()

# Graficar resultados
graficar_señales(signal, signal_acelerado, sr, "Señal Acelerada (Factor 1.25)")
graficar_señales(signal, signal_desacelerado, sr, "Señal Desacelerada (Factor 0.75)")


# Función para graficar espectrogramas
def graficar_espectrograma(signal, sr, titulo, cmap="plasma"):
    """
    Grafica el espectrograma de una señal de audio.

    Parámetros:
        signal (array): Señal de audio.
        sr (int): Tasa de muestreo.
        titulo (str): Título del gráfico.
        cmap (str): Mapa de color para el espectrograma.
    """
    plt.figure()
    S = librosa.stft(signal)  # Transformada de Fourier de tiempo corto
    S_db = librosa.amplitude_to_db(np.abs(S), ref= np.max)  # Convertir a escala logarítmica (dB)
    librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="hz", cmap=cmap)
    plt.ylim(0,3000)
    plt.colorbar(format="%+2.0f dB")
    plt.title(titulo)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Frecuencia (Hz)")
    plt.tight_layout()

# Graficar espectrogramas
graficar_espectrograma(signal, sr, "Espectrograma de la Señal Original", cmap="viridis")
graficar_espectrograma(signal_acelerado, sr, "Espectrograma de la Señal Acelerada (Factor 1.25)", cmap="viridis")
graficar_espectrograma(signal_desacelerado, sr, "Espectrograma de la Señal Desacelerada (Factor 0.75)", cmap="viridis")
plt.show()

# Opcional: Guardar las señales modificadas en archivos
# Guardar las señales procesadas
# sf.write("InASentimentalMood_Acelerado.wav", signal_acelerado, sr)
# sf.write("InASentimentalMood_Desacelerado.wav", signal_desacelerado, sr)
