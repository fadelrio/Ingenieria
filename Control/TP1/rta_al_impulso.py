import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import sympy as sp

# ----------------------------
# PARTE 1: RESPUESTA AL IMPULSO (NUMÉRICA)
# ----------------------------
numerador = [1]
denominador = [11, 165, 400e6, 2000e6]
G = ctrl.TransferFunction(numerador, denominador)

# Calcular la respuesta al impulso
t, y = ctrl.impulse_response(G)

# Graficar la respuesta al impulso
plt.plot(t, y, label='Respuesta al impulso', color='blue')
plt.title('Respuesta al Impulso')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()

# ----------------------------
# PARTE 2: FORMULA SIMBÓLICA DE LA RESPUESTA
# ----------------------------
s, t_sym = sp.symbols('s t', real=True, positive=True)

# Función de transferencia simbólica
G_s = 1 / (11*s**3 + 165*s**2 + 400e6*s + 2000e6)

# Transformada inversa de Laplace
respuesta_impulso_t = sp.inverse_laplace_transform(G_s, s, t_sym)
respuesta_impulso_t = sp.simplify(respuesta_impulso_t)

# Mostrar la expresión analítica
print("Respuesta al impulso en el dominio del tiempo:")
sp.pprint(respuesta_impulso_t, use_unicode=True)

