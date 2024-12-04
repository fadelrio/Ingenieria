#fft de distintas funciones¿

import numpy as np
import matplotlib.pyplot as plt

# sample_rate = 100
#
# tiempo = np.arange(-5, 5, 1/sample_rate)
#
# w = 2*np.pi
#
# #senal = np.cos(w*tiempo)
#
# long_escalon = int(len(tiempo)/3)
# long_padding = int(len(tiempo)/3)
#
# senal = np.concatenate(np.zeros(long_padding),np.ones(long_escalon),np.zeros(long_padding))
#
# fft = np.fft.fft(senal)
# f_fft = np.fft.fftfreq(len(senal), 1/sample_rate)
#
# frecuencias = f_fft[:len(senal) // 2]
# fft_signal = np.abs(fft[:len(senal) // 2])
#
# plt.figure()
# plt.plot(frecuencias, fft_signal)
#
#
# plt.figure()
#
# plt.plot(tiempo, senal)
#
# plt.show()


#u(t)
senal = np.concatenate([np.zeros(40000), np.ones(100), np.zeros(40000)])

sample_rate=48000

tiempo = np.arange(len(senal))/sample_rate

fft = np.fft.fft(senal)
f_fft = np.fft.fftfreq(len(senal), 1/sample_rate)

frecuencias = f_fft[:len(senal) // 2]
fft_signal = np.abs(fft[:len(senal) // 2])

plt.figure()
plt.plot(frecuencias, fft_signal)


plt.figure()

plt.plot(tiempo, senal)

plt.show()