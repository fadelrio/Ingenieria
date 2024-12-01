import numpy as np
from scipy.io import wavfile as waves
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, butter, filtfilt

def upsample(senal, largo, factor):
    salida = np.zeros(largo*factor)

    for i in range(0,largo):
        salida[i*(factor)] = senal[i]

    print(salida)

    # for i in range(largo):
    #     m = (senal[i]-senal[i])/(factor+1)
    #     for j in range(1,factor+1):
    #         salida[i*(fdata_iasm_upsampleadaactor)+j] = m*j + senal[i]

    return salida

def filtro(senal, f_muestreo, f_corte):
    nyquist = 0.5 * f_muestreo  # Frecuencia de Nyquist
    normal_cutoff = f_corte / nyquist  # Frecuencia de corte normalizada porque la funcion butter usa valores entre 0 y 1, siendo 1 la frec de nyquist
    b, a = butter(4, normal_cutoff, btype='low', analog=False)

    # Usamos filtfilt para filtrar la señal en ambas direcciones y evitar desfase
    filtered_signal = filtfilt(b, a, senal)

    return filtered_signal


def downsample(senal, factor):

    salida = senal[::factor]

    return salida

def resample(senal, f_muestreo, largo, factor):

    factores = factor.as_integer_ratio()

    salida = upsample(senal,largo,factores[1])

    if(factores[1]>factores[0]):
        salida = filtro(salida,f_muestreo,f_muestreo/(2*factores[1]))
    else:
        salida = filtro(salida,f_muestreo,f_muestreo/(2*factores[0]))


    salida = downsample(salida,factores[0])

    return salida


def plot_signals(original_rate, original_signal, modified_rate, modified_signal, factor):
    time_original = np.linspace(0, len(original_signal) / original_rate, len(original_signal))
    time_modified = np.linspace(0, len(modified_signal) / modified_rate, len(modified_signal))

    time_xlim = max(time_original[-1], time_modified[-1])

    if (time_xlim % 10):
        time_xlim = time_xlim + (10 - time_xlim % 10)

    # Graficar señal original
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time_original, original_signal, label="Señal original")
    plt.ylabel("Amplitud")
    plt.xlim(0, time_xlim)
    plt.title("Señal original")
    plt.legend()
    plt.grid()

    # Graficar señal modificada
    plt.subplot(2, 1, 2)
    plt.plot(time_modified, modified_signal, color='orange', label=f"Señal modificada (Factor: {factor})")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.xlim(0, time_xlim)
    plt.title("Señal modificada")
    plt.legend()
    plt.grid()
    plt.show()



audio_iasm = "InASentimentalMood.wav"

# Cargar la data en la matriz, con su frecuencia de muestreo Fs
Fs, data_iasm = waves.read(audio_iasm)

Ts = 1 / Fs  # T sample 1
time_iasm = Ts * np.arange(0, len(data_iasm))


data_iasm_upsampleada = resample(data_iasm,Fs,len(data_iasm),1.25)

plot_signals(Fs,data_iasm, Fs, data_iasm_upsampleada, 1.25)

Tf_senal_upsampleada = np.fft.fft(data_iasm_upsampleada, norm="ortho")
L_primer_nota = len(data_iasm_upsampleada)
M_Tf_senal_original = abs(Tf_senal_upsampleada[:L_primer_nota // 2])
F_senal_original = (Fs / L_primer_nota) * np.arange(0, L_primer_nota // 2)

plt.figure(figsize=(8, 6))
plt.plot(F_senal_original,M_Tf_senal_original, 'g-', label="Señal upsampleada")
plt.legend()

# nyquist = 0.5 * Fs  # Frecuencia de Nyquist
# b, a = butter(4, 0.2, btype='low', analog=False)
#
# # Usamos filtfilt para filtrar la señal en ambas direcciones y evitar desfase
# filtered_signal = filtfilt(b, a, data_iasm_upsampleada)
#
Tf_senal_original = np.fft.fft(data_iasm, norm="ortho")
L_primer_nota = len(data_iasm)
M_Tf_senal_original = abs(Tf_senal_original[:L_primer_nota // 2])
F_senal_original = (Fs / L_primer_nota) * np.arange(0, L_primer_nota // 2)

plt.figure(figsize=(8, 6))
plt.plot(F_senal_original,M_Tf_senal_original, 'g-', label="Señal original")
plt.legend()
plt.show()
#
# Tf_senal_upsampleada = np.fft.fft(filtered_signal, norm="ortho")
# L_primer_nota = len(filtered_signal)
# M_Tf_senal_original = abs(Tf_senal_upsampleada[:L_primer_nota // 2])
# F_senal_original = (Fs / L_primer_nota) * np.arange(0, L_primer_nota // 2)
#
# plt.figure(figsize=(8, 6))
# plt.plot(F_senal_original,M_Tf_senal_original, 'g-', label="Señal upsampleada - filtrada")
# plt.legend()
# plt.show()





