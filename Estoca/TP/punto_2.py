from scipy.io import wavfile
from scipy.signal import lfilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import toeplitz
from scipy import linalg
from scipy.signal import periodogram

def lpc(xs, P):

    N = len(xs)

    # Estimar autocorrelación hasta orden P
    r_simetrica = np.correlate(xs, xs, mode='full') / N #R(-N+1), ... R(N-1)
    mid = len(r_simetrica) // 2 ## obtengo el indice de R(0)
    r = r_simetrica[mid:mid+P+1]  # r[0], r[1], ..., r[P]

    # Construir matriz de Toeplitz R y vector r
    R = toeplitz(r[:-1])  # R es P x P
    r_vec = r[1:]         # Vector r para el lado derecho

    # Resolver sistema lineal: R a = r_vec
    a = np.linalg.solve(R, r_vec)

    # Calcular la ganancia G
    G2 = r[0] - np.dot(a, r[1:]) #armo G^2 teoricamente
    G = np.sqrt(G2) if G2 > 0 else 0 # Tomo la raiz de los terminos positivos

    return a, G

def pitch_lpc(xs, a, alpha, fs, graficar=True, nombre_audio = ""):

    P = len(a)
    N = len(xs)

    # Calculo el error
    e = np.zeros(N)
    for n in range(P, N):
        predictor = np.dot(a, xs[n - P:n][::-1])  # X_predictor = X(n - 1), ..., X(n - P)
        e[n] = xs[n] - predictor #definicion del error de prediccion

    # Autocorrelación
    r = np.correlate(e, e, mode='full') #autocorrelacion del error R_e
    r = r[len(r)//2:]  # tomo los con k >= 0 (como es simetrico solo me interesa sus k>0)

    # Normalizo la autocorrelacion con sus varianza para acotar el rango entre 0 y 1
    r /= r[0] if r[0] != 0 else 1

    # grafico en cada caso al autocorrelacion del error de estimacion para verificar el calculo
    if graficar:
        lags = np.arange(len(r))
        plt.figure(figsize=(8, 4))
        plt.plot(lags, r)
        plt.title(f"Autocorrelación del error LPC ({nombre_audio})")
        plt.xlabel("k")
        plt.ylabel(r"$r_e[k]$")
        plt.grid(True)
        plt.axhline(y=alpha, color='r', linestyle='--', label=f'Umbral α = {alpha}')
        plt.legend()
        plt.tight_layout()
        plt.show()

    #Para una convergencia mas rapida tomo un rango de frecuencias para las excitaciones sonoras
    # Busco el 2do pico para calcular el periodo y frecuencia fundamental
    #A priori se sabe que el rango del pitch debe estar entre 80 y 400hz por lo que para evitar falsos picos se acota el rango
    kmin = int(fs / 400)  # Ignoro tonos demasiado altos (> 400 Hz)
    kmax = int(fs / 80)   # Ignoro tonos muy bajos (< 80 Hz)
    region = r[kmin:kmax] # defino la region a analizar

    segundo_pico = np.argmax(region) + kmin #busco el K para el r_e(k) mas alto dentro de la region
    valor_pico = r[segundo_pico]

    if valor_pico >= alpha:       #hago un barrido hasta el primero que supere
        return fs / segundo_pico
    else:
        return 0


fs_a, xs_a = wavfile.read("a.wav")
xs_a = xs_a.astype(float)

fs_e, xs_e = wavfile.read("e.wav")
xs_e = xs_e.astype(float)

fs_s, xs_s = wavfile.read("s.wav")
xs_s = xs_s.astype(float)

fs_sh, xs_sh = wavfile.read("sh.wav")
xs_sh = xs_sh.astype(float)


#Ajustar P
a_a, G_a = lpc(xs_a, P=30)
a_e, G_e = lpc(xs_e, P=30)
a_s, G_s = lpc(xs_s, P=30)
a_sh, G_sh = lpc(xs_sh, P=30)


#Ajustar alpha a partir del grafico
fp_a = pitch_lpc(xs_a, a_a, alpha=0.4, fs=fs_a, graficar=True, nombre_audio = "a.wav")
fp_e = pitch_lpc(xs_e, a_e, alpha=0.4, fs=fs_e, graficar=True, nombre_audio = "e.wav")
fp_s = pitch_lpc(xs_s, a_s, alpha=0.4, fs=fs_s, graficar=True, nombre_audio = "s.wav")
fp_s = pitch_lpc(xs_sh, a_sh, alpha=0.4, fs=fs_sh, graficar=True, nombre_audio = "sh.wav")



print(f"Frecuencia de pitch de a.wav estimada: {fp_a:.2f} Hz")
print(f"Frecuencia de pitch de e.wav estimada: {fp_e:.2f} Hz")
print(f"Frecuencia de pitch de s.wav estimada: {fp_s:.2f} Hz")

"""EJERCICIO 2B a chequear"""

def sintetizar_fonema(a, G, fs, N, tipo='vocal', fp=200):

    # Defino la señal sintetizada segun si es una vocal o sonido sordo
    if tipo == 'vocal':
        periodo = int(fs / fp)
        u = np.zeros(N)
        u[::periodo] = np.sqrt(fs / fp)  # armo el tren de impulsos normalizado a partir del pitch
    elif tipo == 'sordo':
        u = np.random.randn(N) #lo describo como ruido blanco de longitud N


    # Filtro LPC con e^-jm -> z^-1 : H(z) = G / (1 - a1*z^-1 - a2*z^-2 - ...)
    # Implementamos como filtro IIR, a = [1, a1, a2, ...]
    a_filtro = np.concatenate([[1], -a])
    x_sintetizado = lfilter(G, a_filtro, u) ##nose si se puede usar directamente lfilter

    return x_sintetizado

##EN CASO QUE SEA UNA VOCAL
fs, xs = wavfile.read("a.wav")
xs = xs.astype(float)
N = len(xs)


#Estimo lPC y Pitch
a, G = lpc(xs, P=30)
fp = pitch_lpc(xs, a, alpha=0.4, fs=fs, graficar=True)

# Sintetizo la señal
x_sintetizado = sintetizar_fonema(a, G, fs, N, tipo='vocal', fp=fp)

# Graficar PSD original vs. sintetizada
f = np.fft.fftfreq(N, 1/fs)
Pxx_real = np.abs(np.fft.fft(xs))**2 / N
Pxx_sintetizado = np.abs(np.fft.fft(x_sintetizado))**2 / N

#se grafican las frecuencias positivas
mascara = f >= 0
f = f[mascara]
Pxx_real = Pxx_real[mascara]
Pxx_sintetizado = Pxx_sintetizado[mascara]

plt.figure(figsize=(10, 4))
plt.plot(f, 10 * np.log10(Pxx_real + 1e-12), label='Señal original a.wav')
plt.plot(f, 10 * np.log10(Pxx_sintetizado + 1e-12), label='Señal sintetizada a.wav')
plt.title("Comparación PSD — Fonema Vocal")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Potencia [dB]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#EN CASO QUE SEA UN FONEMA
fs_s, xs_s = wavfile.read("s.wav")
xs_s = xs_s.astype(float)
N_s = len(xs_s)

#Estimo lPC y Pitch
a_s, G_s = lpc(xs_s, P=30)
fp_s = pitch_lpc(xs_s, a_s, alpha=0.4, fs=fs_s, graficar=True)

# Sintetizo la señal
x_sintetizado_s = sintetizar_fonema(a_s, G_s, fs_s, N_s, tipo='sordo', fp=fp_s)

# Graficar PSD original vs. sintetizada
f_s = np.fft.fftfreq(N_s, 1/fs_s)
Pxx_real_s = np.abs(np.fft.fft(xs_s))**2 / N_s
Pxx_sintetizado_s = np.abs(np.fft.fft(x_sintetizado_s))**2 / N_s

#se grafican las frecuencias positivas
mascara_s = f_s >= 0
f_S = f_s[mascara_s]
Pxx_real_s = Pxx_real_s[mascara_s]
Pxx_sintetizado_s = Pxx_sintetizado_s[mascara_s]

plt.figure(figsize=(10, 4))
plt.plot(f, 10 * np.log10(Pxx_real_s + 1e-12), label='Señal original s.wav')
plt.plot(f, 10 * np.log10(Pxx_sintetizado_s + 1e-12), label='Señal sintetizada s.wav')
plt.title("Comparación PSD — Fonema sordo")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Potencia [dB]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

