import scipy.io.wavfile as waves
import librosa as lib
import numpy as np

fragmento = 1 #fragmento del audio, 0 para el que va de 0s a 1.5s y 1 para el que va de 1.5s a 3s
nota = 1 #nota del audio, 0 para la primera y 1 para la segunda

# Importamos los archivos

frecuencia_nota = 0

if(fragmento == 0 & nota == 0):
    frecuencia_nota = 182
elif(fragmento == 0 & nota == 1):
    frecuencia_nota = 230
elif(fragmento == 1 & nota == 0):
    frecuencia_nota = 70
elif(fragmento == 1 & nota == 1):
    frecuencia_nota = 98

audio_notas = f"notas_musicales_filtradas{frecuencia_nota}.wav"

# Cargamos la data en la matriz, con su frecuencia de muestreo Fs
Fs1, data_notas = waves.read(audio_notas)

lib.effects.

