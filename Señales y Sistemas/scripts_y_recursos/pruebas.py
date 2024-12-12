#fft de distintas funciones¿

import numpy as np
import matplotlib.pyplot as plt

sample_rate = 100
tiempo = np.arange(0, 1, 1/sample_rate)
#
f_1 = 30

alpha = [0, 0.5, 1, 1.5]

n_f = 1000

for alpha in alpha:

    f_2 = f_1 + alpha / ((1/sample_rate)*n_f)

    senal = np.cos(2*np.pi*f_1*tiempo) + np.cos(2*np.pi*f_2*tiempo)

    fft = np.fft.fft(senal, n_f)
    f_fft = np.fft.fftfreq(len(senal), 1/n_f)

    frecuencias = f_fft[:len(senal) // 2]
    fft_signal = np.abs(fft[:len(senal) // 2])

    plt.figure()
    plt.plot(frecuencias, fft_signal, "o")
    plt.title(f"$f_1$ = {f_1:.2f} Hz $f_2$ = {f_2:.2f} Hz")

    #plt.figure()

    #plt.plot(tiempo, senal, "o")

plt.show()


#u(t)
#senal = np.concatenate([np.zeros(40000), np.ones(100), np.zeros(40000)])

#sample_rate=48000

#tiempo = np.arange(len(senal))/sample_rate

#fft = np.fft.fft(senal)
#f_fft = np.fft.fftfreq(len(senal), 1/sample_rate)

#frecuencias = f_fft[:len(senal) // 2]
#fft_signal = np.abs(fft[:len(senal) // 2])

#plt.figure()
#plt.plot(frecuencias, fft_signal)



plt.show()
