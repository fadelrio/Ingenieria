import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Definir la función de transferencia: G(s) = 1 / (s^2 + s + 1)
numerador = [1]
denominador = [11, 165, 400e6, 2000e6]
G = ctrl.TransferFunction(numerador, denominador)

# Obtener respuesta al escalón con control
time, response_ctrl = ctrl.impulse_response(G)

# Definir la función analítica de la respuesta al escalón
def respuesta_analitica(x):
    respuesta = np.zeros_like(x)
    # Solo calcular para x > 0
    x_pos = x[x > 0]
    # respuesta[x > 0] = -11 + 2*x_pos +11.1*np.exp(-0.173*x_pos) + (1/2)* np.exp(-0.16*x_pos)*(-0.196*np.cos(1.19*x_pos) + 0.156*np.sin(1.19*x_pos))
    # respuesta[x > 0] = 4*(1 - 1.02*np.exp(-0.173*x_pos) + np.exp(-0.163*x_pos)*(0.00188*np.cos(1.19*x_pos)-0.1456*np.sin(1.19*x_pos)))
    respuesta[x > 0] = (2.5e-9)*np.exp(-5*x_pos)*(1-np.cos(6030*x_pos))
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

