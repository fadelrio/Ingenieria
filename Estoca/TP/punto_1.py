import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
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



def plot_lpc_vs_periodogram(filename, P, es_vocal=True, fs_exc=200):
    #señal desde archivo WAV
    fs, xs = wavfile.read(filename)
    xs = xs.astype(float)
    N = len(xs)
    #coeficientes LPC y ganancia G
    a, G = lpc(xs, P)
    print(a)
    print(G)
    #estimar el periodograma usando correctamente la funcion
    Pxx = 1/N*np.abs(np.fft.fft(xs))**2
    f = np.fft.fftfreq(N, 1/fs)

    #PSD estimada por el modelo LPC (sin fuente aún)
    w = 2 * np.pi * f / fs  # frecuencia angular
    A_w = np.ones_like(w, dtype=np.complex64)  # vector de unos para armar el denominador del AR(P)

    #Armo el denominador 1 - a_1 * e^(-1wk) - .... -a_p . e^(-pwk)
    for k, ak in enumerate(a):
        A_w -= ak * np.exp(-1j * w * (k + 1))

    #|H(W)|^2
    PSD_LPC = (G**2) / (np.abs(A_w)**2)

    # Modelo de excitación (fonema sonoro o sordo)
    if es_vocal:
        # Fuente: tren de impulsos (frecuencia fundamental fs_exc)
        periodo = int(fs / fs_exc)
        tren_impulsos = np.zeros(N)
        tren_impulsos[::periodo] = np.sqrt(fs/fs_exc)
        S_u = 1/N*np.abs(np.fft.fft(tren_impulsos))**2 #Estimar el periodograma del tren de pulsos usando correctamente la funcion
        PSD_LPC *= S_u  # |H(W)|^2 * S_u = S_x (PSD teorica por LPC)
    else:
        pass ##|H(W)|^2 * 1(ruido blanco) = S_x

    #se grafican las frecuencias positivas
    mascara = f >= 0
    f = f[mascara]
    Pxx = Pxx[mascara]
    PSD_LPC = PSD_LPC[mascara]

    #Graficar resultados en escala dB
    plt.figure(figsize=(10, 4))
    plt.plot(f, 10 * np.log10(Pxx + 1e-12), label="Periodograma real")
    plt.plot(f, 10 * np.log10(PSD_LPC + 1e-12), label="PSD LPC estimada")
    plt.title(f"{filename} — Orden P = {P}")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Potencia (dB)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#subir los archivos localmente
# Para fonemas sonoros
P_order = [5,10,30]
for P in P_order:
  plot_lpc_vs_periodogram("a.wav", P, es_vocal=True)
  plot_lpc_vs_periodogram("e.wav", P, es_vocal=True)

  # Para fonemas sordos
  plot_lpc_vs_periodogram("s.wav", P, es_vocal=False)
  plot_lpc_vs_periodogram("sh.wav", P, es_vocal=False)
