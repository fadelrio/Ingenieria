import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Definir la función de transferencia
# Ejemplo: G(s) = (s + 2) / (s^2 + 3s + 2)
# G = Numerador / Denominador
numerador = [1-(3**(0.5))/2, 1]   # Coeficientes del numerador
denominador = [1, 1, 1]  # Coeficientes del denominador

# Crear la función de transferencia
G = ctrl.TransferFunction(numerador, denominador)

# Respuesta al escalón
time, response = ctrl.step_response(G)

# Graficar la respuesta al escalón
plt.plot(time, response)
plt.title('Respuesta al Escalón de la Función de Transferencia')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()

