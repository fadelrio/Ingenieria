import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Definir la función de transferencia: G(s) = 1 / (s^2 + s + 1)
numerador = [1, 1/2, 1]
denominador = [2, 1, 3, 1/2, 0]
G = ctrl.TransferFunction(numerador, denominador)

# Obtener respuesta al escalón con control
time, response_ctrl = ctrl.step_response(G)

# Definir la función analítica de la respuesta al escalón
def respuesta_analitica(x):
    respuesta = np.zeros_like(x)
    # Solo calcular para x > 0
    x_pos = x[x > 0]
    # respuesta[x > 0] = -11 + 2*x_pos +11.1*np.exp(-0.173*x_pos) + (1/2)* np.exp(-0.16*x_pos)*(-0.196*np.cos(1.19*x_pos) + 0.156*np.sin(1.19*x_pos))
    respuesta[x > 0] = 3 + 2*x_pos +(8/3)*np.exp(-0.5*x_pos) - 4*np.cos(0.5*x_pos) + 8*np.sin(0.5*x_pos)
    return respuesta

# Calcular respuesta analítica
response_analytic = respuesta_analitica(time)

# Graficar ambas respuestas
plt.plot(time, response_ctrl, label='Respuesta (control.step_response)', linewidth=2)
plt.plot(time, response_analytic, '--', label='Respuesta (función analítica)', linewidth=2)

plt.title('Comparación de Respuesta al Escalón')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.show()

