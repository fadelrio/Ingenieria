from cProfile import label

import numpy as np
import matplotlib.pyplot as plt
import librosa as lib
from scipy.io import wavfile as waves

def procesar_y_graficar(fragmento, nota):
    # Determinar la frecuencia de la nota en función de fragmento y nota
    if fragmento == 0 and nota == 0:
        frecuencia_nota = 182
    elif fragmento == 0 and nota == 1:
        frecuencia_nota = 230
    elif fragmento == 1 and nota == 0:
        frecuencia_nota = 70
    elif fragmento == 1 and nota == 1:
        frecuencia_nota = 98

    # Nombre del archivo de audio
    audio_notas = f"notas_musicales_filtradas{frecuencia_nota}.wav"


    # Cargar la data en la matriz, con su frecuencia de muestreo Fs
    Fs1, data_notas = waves.read(audio_notas)

    # Normalización de la señal
    data_notas_normalizada = data_notas / np.max(np.abs(data_notas), axis=0)

    # Transformada de Fourier (FFT) de la señal original
    Tf_senal_original = np.fft.fft(data_notas_normalizada, norm="ortho")
    L_primer_nota = len(data_notas_normalizada)
    M_Tf_senal_original = abs(Tf_senal_original[:L_primer_nota // 2])
    F_senal_original = (Fs1 / L_primer_nota) * np.arange(0, L_primer_nota // 2)


    # Desplazamiento de la nota (pitch shift)
    datos_shifteados = lib.effects.pitch_shift(data_notas_normalizada, sr=Fs1, n_steps=1)

    datos_shifteados_normalizados = datos_shifteados / np.max(np.abs(datos_shifteados), axis=0)

    # FFT de la señal desplazada
    Tf_senal_shifteada = np.fft.fft(datos_shifteados_normalizados, norm="ortho")
    L_primer_nota = len(datos_shifteados_normalizados)
    M_Tf_senal_shifteada = abs(Tf_senal_shifteada[:L_primer_nota // 2])
    F_senal_shifteada = (Fs1 / L_primer_nota) * np.arange(0, L_primer_nota // 2)


    plt.figure(figsize=(8, 6))

    plt.plot(F_senal_original,M_Tf_senal_original, 'g-', label="Señal original")
    plt.title(f"Desplazamiento de nota de {frecuencia_nota}Hz")
    plt.grid()
    plt.plot(F_senal_shifteada, M_Tf_senal_shifteada, "b-", label= "Señal desplazada")

    if fragmento == 0:
        plt.xlim([0, 1000])
    elif fragmento == 1:
        plt.xlim([0, 650])

    plt.legend()


    # DESCOMENTAR PARA GRAFICAR LAS DOS SEÑALES EN GRAFICOS DISTINTOS

    # Crear la figura y los subgráficos (2 filas, 1 columna)
    #fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # 2 filas, 1 columna

    # # Graficar la primera función en el primer subgráfico (arriba)
    # ax1.plot(F_senal_original, M_Tf_senal_original, 'g-', label='Señal original')
    # ax1.set_title(f"Desplazamiento de nota de {frecuencia_nota}Hz")
    # if fragmento == 0:
    #     ax1.set_xlim([0, 2000])
    # elif fragmento == 1:
    #     ax1.set_xlim([0, 1000])
    # ax1.legend()
    #
    # # Graficar la segunda función en el segundo subgráfico (abajo)
    # ax2.plot(F_senal_shifteada, M_Tf_senal_shifteada, 'b-', label='Señal desplazada')
    # if fragmento == 0:
    #     ax2.set_xlim([0, 2000])
    # elif fragmento == 1:
    #     ax2.set_xlim([0, 1000])
    # ax2.set_xlabel("Frecuencia [Hz]")
    # ax2.legend()
    #
    # # Ajustar el espacio entre los subgráficos
    # plt.tight_layout()

# Ejecutar con todas las combinaciones de fragmento y nota (0 o 1)
for fragmento in [0, 1]:
    for nota in [0, 1]:
        procesar_y_graficar(fragmento, nota)
plt.show()