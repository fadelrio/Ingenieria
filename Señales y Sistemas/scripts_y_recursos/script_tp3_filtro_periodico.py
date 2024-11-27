import scipy.io.wavfile as waves
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

fragmento = 1 #fragmento del audio, 0 para el que va de 0s a 1.5s y 1 para el que va de 1.5s a 3s

# Importamos los archivos
audio_notas = "notas_musicales.wav"

# Cargamos la data en la matriz, con su frecuencia de muestreo Fs
fsamp_notas, data_notas = waves.read(audio_notas)


# Convertimos el audio de estéreo a mono
if len(data_notas.shape) == 2:  # Verifica si hay dos canales (estéreo)
    data_notas = data_notas.mean(axis=1).astype(data_notas.dtype)


longitud_notas = len(data_notas)

# Armo el array de la variable tiempo con las respectivas longitudes
periodo_samp_notas = 1 / fsamp_notas  # T sample 1
tiempo_notas = periodo_samp_notas * np.arange(0, longitud_notas)

# Extraemos el audio
if fragmento == 0:
    inicio_muestra = 0
    fin_muestra = 1.5
elif fragmento == 1:
    inicio_muestra = 1.5
    fin_muestra = 3

samples_to_plot_start = int(inicio_muestra * fsamp_notas)
samples_to_plot_stop = int(fin_muestra * fsamp_notas)
data_nota_recortada = data_notas[samples_to_plot_start:samples_to_plot_stop]
tiempo_nota_recortada = tiempo_notas[samples_to_plot_start:samples_to_plot_stop]

# Graficamos 
plt.figure()
plt.plot(tiempo_nota_recortada, data_nota_recortada, linewidth=0.5)
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud de audio')
plt.title('Gráfico temporal')

# Transformada de Fourier (TTF) 
tf_nota_recortada = np.fft.fft(data_nota_recortada)
long_nota_recortada = len(data_nota_recortada)
modulo_tf_nota_recortada = abs(tf_nota_recortada[:long_nota_recortada // 2])
frecuencias_m_nota_recortada = (fsamp_notas / long_nota_recortada) * np.arange(0, long_nota_recortada // 2)

# Graficamos la Transformada de Fourier 
plt.figure()
plt.plot(frecuencias_m_nota_recortada, modulo_tf_nota_recortada, linewidth=0.5, color='green')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud TTF')
plt.title('Transformada de Fourier - notas_musicales.wav')


# Función para graficar el espectrograma
def graficar_espectrograma(signal, title, fs, fragmento_usado):
    f, t_spec, sxx = spectrogram(signal, fs=fs, window='hann', nperseg=8192, noverlap=2048)
    plt.pcolormesh(t_spec, f, 10 * np.log10(sxx), shading='gouraud')
    plt.title(title)
    plt.ylim(0, 5000)
    plt.ylabel('Frecuencia [Hz]')
    plt.xlabel('Tiempo [s]')
    plt.colorbar(label='Intensidad [dB]')
    if fragmento_usado == 0:
        plt.ylim([0,2000])
    elif fragmento_usado == 1:
        plt.ylim([0,1000])

# Parámetros del filtro
if fragmento == 0:
    f0_list = [182, 230]  # Lista de frecuencias base [Hz]
elif fragmento == 1:
    f0_list = [70, 98]

ancho = 15  # Ancho de cada ventana [Hz] (± la mitad)
num_armonicos = 10  # Número de armónicos a considerar
fsamp_notas = 44100  # Frecuencia de muestreo del archivo
long_nota_recortada = len(tf_nota_recortada)  # Longitud de la señal

# Crear las frecuencias en función de la longitud de la señal
freqs = np.fft.fftfreq(long_nota_recortada, d=1 / fsamp_notas)

# Iterar sobre cada frecuencia f0 en la lista f0_list
for f0 in f0_list:
    # Crear el filtro pasa-banda múltiple
    filtro = np.zeros(long_nota_recortada)

    # Para cada armónico de f0 (n * f0), activamos la ventana alrededor de esa frecuencia
    for n in range(1, num_armonicos + 1):
        centro_f = n * f0
        inicio_f = centro_f - ancho / 2
        fin_f = centro_f + ancho / 2

        # Encuentra los índices de frecuencia en el dominio de Fourier
        indices_banda = np.where((freqs >= inicio_f) & (freqs <= fin_f))[0]
        
        # Activamos las bandas
        filtro[indices_banda] = 1
        filtro[-indices_banda] = 1  # Reflejar en la parte negativa de frecuencias

    # Aplicar el filtro a la transformada de Fourier
    Tf_m_filtrada = tf_nota_recortada * filtro

    # Reconstrucción de la señal filtrada
    data_notas_filtrada = np.fft.ifft(Tf_m_filtrada).real

    # Graficar la señal filtrada en el dominio del tiempo
    plt.figure()
    plt.plot(data_notas_filtrada[:long_nota_recortada], linewidth=0.5, color='red')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title(f'Señal filtrada - Dominio del tiempo ($f_0$ = {f0} Hz)')

    # Graficar el espectro de la señal filtrada
    M_Tf_m_filtrada = np.abs(Tf_m_filtrada[:long_nota_recortada // 2])
    frecuencias_m_nota_recortada = (fsamp_notas / long_nota_recortada) * np.arange(0, long_nota_recortada // 2)

    plt.figure()
    plt.plot(frecuencias_m_nota_recortada, M_Tf_m_filtrada, linewidth=0.5, color='purple')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Amplitud TTF')
    plt.title(f'Transformada de Fourier - Señal filtrada ($f_0$ = {f0} Hz)')
    if fragmento == 0:
        plt.xlim([0,2000])
    elif fragmento == 1:
        plt.xlim([0,1000])

    # Guardar la señal filtrada en un nuevo archivo
    output_path = f"notas_musicales_filtradas{f0}.wav"
    waves.write(output_path, fsamp_notas, data_notas_filtrada.astype(np.int16))

    # Graficar el espectrograma de la señal filtrada
    plt.figure(figsize=(10, 8))
    graficar_espectrograma(data_notas_filtrada, f'Espectrograma de la señal filtrada ($f_0$ = {f0} Hz)', fsamp_notas, fragmento)
plt.show()
