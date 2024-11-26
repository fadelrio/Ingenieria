import scipy.io.wavfile as waves
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fourier
from scipy.signal import spectrogram


fragmento = 1 #fragmento del audio, 0 para el que va de 0s a 1.5s y 1 para el que va de 1.5s a 3s

# Importamos los archivos
audio_notas = "notas_musicales.wav"

# Cargamos la data en la matriz, con su frecuencia de muestreo Fs
Fs1, data_notas = waves.read(audio_notas)


# Convertimos el audio de estéreo a mono
if len(data_notas.shape) == 2:  # Verifica si hay dos canales (estéreo)
    data_notas = data_notas.mean(axis=1).astype(data_notas.dtype)


L_m = len(data_notas)

# Armo el array de la variable tiempo con las respectivas longitudes
Ts1 = 1 / Fs1  # T sample 1
t_m = Ts1 * np.arange(0, L_m)

# Transformada de Fourier (TTF)
Tf_m = np.fft.fft(data_notas)
M_Tf_m = abs(Tf_m[:L_m // 2])
F_m = (Fs1 / L_m) * np.arange(0, L_m // 2)

# Extraemos el audio



if fragmento == 0:
    inicio_muestra = 0
    fin_muestra = 1.5
    samples_to_plot_start = int(inicio_muestra * Fs1)
    samples_to_plot_stop = int(fin_muestra * Fs1)
    data_notas_primer_nota = data_notas[samples_to_plot_start:samples_to_plot_stop]
    t_m_primer_nota = t_m[samples_to_plot_start:samples_to_plot_stop]
elif fragmento == 1:
    inicio_muestra = 1.5
    fin_muestra = 3
    samples_to_plot_start = int(inicio_muestra * Fs1)
    samples_to_plot_stop = int(fin_muestra * Fs1)
    data_notas_primer_nota = data_notas[samples_to_plot_start:samples_to_plot_stop]
    t_m_primer_nota = t_m[samples_to_plot_start:samples_to_plot_stop]


# Graficamos 
fig3 = plt.figure()
plt.plot(t_m_primer_nota, data_notas_primer_nota, linewidth=0.5)
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud de audio')
plt.title('notas_musicales.wav gráfico temporal')
fig3.savefig('Audio1_11-15')

# Transformada de Fourier (TTF) 
Tf_m_primer_nota = np.fft.fft(data_notas_primer_nota)
L_primer_nota = len(data_notas_primer_nota)
M_Tf_m_primer_nota = abs(Tf_m_primer_nota[:L_primer_nota // 2])
F_m_primer_nota = (Fs1 / L_primer_nota) * np.arange(0, L_primer_nota // 2)

# Graficamos la Transformada de Fourier 
fig5 = plt.figure()
plt.plot(F_m_primer_nota, M_Tf_m_primer_nota, linewidth=0.5, color='green')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud TTF')
plt.title('Transformada de Fourier - notas_musicales.wav')
fig5.savefig('Transf1_11-15')


# Función para graficar el espectrograma
def graficar_espectrograma(signal, title, fs, fragmento_usado):
    f, t_spec, Sxx = spectrogram(signal, fs=fs, window='hann', nperseg=8192, noverlap=2048)
    plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.title(title)
    plt.ylim(0, 5000)
    plt.ylabel('Frecuencia [Hz]')
    plt.xlabel('Tiempo [s]')
    plt.colorbar(label='Intensidad [dB]')
    if fragmento_usado == 0:
        plt.ylim([0,2000])
    elif fragmento_usado == 1:
        plt.ylim([0,1000])

# Filtro modular periódico
def filtro_modular_periodico(f0, ancho, freqs):
    filtro = np.ones_like(freqs)
    ancho_mitad = ancho / 2
    for k in range(0, 10):  # Ajustar la periodicidad del filtro
        f_centro = k * f0
        atenuadas = (np.abs(freqs - f_centro) <= ancho_mitad)
        filtro[atenuadas] = 0  # Atenuar
    return filtro

# Parámetros del filtro
if fragmento == 0:
    f0_list = [182, 230]  # Lista de frecuencias base [Hz]
elif fragmento == 1:
    f0_list = [70, 98]
ancho = 15  # Ancho de cada ventana [Hz] (± la mitad)
num_armonicos = 10  # Número de armónicos a considerar
Fs1 = 44100  # Frecuencia de muestreo, ajusta según tu archivo
L_primer_nota = len(Tf_m_primer_nota)  # Longitud de la señal, ajusta según tu archivo

# Crear las frecuencias en función de la longitud de la señal
freqs = np.fft.fftfreq(L_primer_nota, d=1 / Fs1)

# Iterar sobre cada frecuencia f0 en la lista f0_list
for f0 in f0_list:
    # Crear el filtro pasa-banda múltiple
    filtro = np.zeros(L_primer_nota)

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
    Tf_m_filtrada = Tf_m_primer_nota * filtro

    # Reconstrucción de la señal filtrada
    data_notas_filtrada = np.fft.ifft(Tf_m_filtrada).real

    # Graficar la señal filtrada en el dominio del tiempo
    plt.figure()
    plt.plot(data_notas_filtrada[:L_primer_nota], linewidth=0.5, color='red')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title(f'Señal filtrada - Dominio del tiempo (f0 = {f0} Hz)')

    # Graficar el espectro de la señal filtrada
    M_Tf_m_filtrada = np.abs(Tf_m_filtrada[:L_primer_nota // 2])
    F_m_primer_nota = (Fs1 / L_primer_nota) * np.arange(0, L_primer_nota // 2)

    plt.figure()
    plt.plot(F_m_primer_nota, M_Tf_m_filtrada, linewidth=0.5, color='purple')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Amplitud TTF')
    plt.title(f'Transformada de Fourier - Señal filtrada (f0 = {f0} Hz)')
    if fragmento == 0:
        plt.xlim([0,2000])
    elif fragmento == 1:
        plt.xlim([0,1000])


    # Guardar la señal filtrada en un nuevo archivo
    output_path = f"notas_musicales_filtradas{f0}.wav"
    waves.write(output_path, Fs1, data_notas_filtrada.astype(np.int16))

    # Graficar el espectrograma de la señal filtrada
    plt.figure(figsize=(10, 8))
    graficar_espectrograma(data_notas_filtrada, f'Espectrograma de la señal filtrada (f0 = {f0} Hz)', Fs1, fragmento)
plt.show()
