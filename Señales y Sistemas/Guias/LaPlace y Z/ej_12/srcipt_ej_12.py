import numpy as np
import matplotlib.pyplot as plt

def graficar_dft_idft(N):

    # Índices de frecuencia
    k = np.arange(N)

    # H(k) en la frecuencia discreta (dominio z)
    H_k = 1 - np.exp(-1j * 2 * np.pi * k * 5 / N)  # H(z) = 1 - z^{-5}

    # Transformada inversa discreta de Fourier (IDFT)
    h_n = np.fft.ifft(H_k)  # IDFT de H(k)

    # Calcular el módulo de h[n] e H[k]
    mod_h_n = np.abs(h_n)  # Módulo de la IDFT
    mod_H_k = np.abs(H_k)  # Módulo de la DFT

    # Crear las gráficas
    plt.figure(figsize=(10, 5))

    # Gráfica del módulo de h[n] (IDFT)
    plt.subplot(1, 2, 1)
    plt.stem(np.arange(N), mod_h_n, basefmt=" ", label='$|h[n]|$')
    plt.xlabel('$n$')
    plt.ylabel('$|h[n]|$')
    plt.title(f"Módulo de la IDFT ({N} muestras)")
    plt.legend()
    plt.grid(True)

    # Gráfica del módulo de H[k] (DFT)
    plt.subplot(1, 2, 2)
    plt.stem(np.arange(N), mod_H_k, basefmt=" ", label='$|H[k]|$', linefmt='g-', markerfmt='go')
    plt.xlabel('$k$')
    plt.ylabel('$|H[k]|$')
    plt.title(f'Módulo de la DFT ({N} muestras)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()


muestras = [10, 5, 2]

for muestra in muestras:
	graficar_dft_idft(muestra)

plt.show()

