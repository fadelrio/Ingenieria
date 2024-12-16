import numpy as np
import matplotlib.pyplot as plt

def graficar_respuesta_frecuencia():
    """
    Grafica la magnitud de la respuesta en frecuencia de la transferencia:
    H(z) = (z^{-1} + 1) / ((z^{-1} - (-1 - sqrt(3)/3)i)(z^{-1} - (-1 + sqrt(3)/3)i))
    """
    # Rango de frecuencias [0, π]
    omega = np.linspace(0, np.pi, 500)
    z = np.exp(1j * omega)  # z = e^{jω}

    # Definición de la transferencia H(z)
    numerator = (z**-1 + 1)**2
    pole1 = -1 - (np.sqrt(3)/3) * 1j
    pole2 = -1 + (np.sqrt(3)/3) * 1j
    denominator = (z**-1 - pole1) * (z**-1 - pole2)
    H = numerator / denominator

    # Magnitud de la respuesta en frecuencia
    H_magnitude = np.abs(H)

    numerator_1 = (z**-1 + 1)**2
    pole1_1 = -3/4 - (np.sqrt(3)/4) * 1j
    pole2_1 = -3/4 + (np.sqrt(3)/4) * 1j
    denominator_1 = (z**-1 - pole1) * (z**-1 - pole2)
    H_1 = numerator_1 / denominator_1

    # Magnitud de la respuesta en frecuencia
    H_magnitude_1 = np.abs(H_1)

    # Gráfica
    plt.figure(figsize=(8, 5))
    plt.plot(omega, H_magnitude, label='$|H(e^{j\omega})|$', color='b')
    plt.plot(omega, H_magnitude_1, label='$|H\'(e^{j\omega})|$', color='y', linestyle='--')
    plt.xlabel('$\omega$ (radianes)')
    plt.ylabel('Magnitud')
    plt.title('Magnitud de la respuesta en frecuencia')
    plt.grid(True)
    plt.legend()
    plt.show()

# Llamar a la función para graficar
graficar_respuesta_frecuencia()

