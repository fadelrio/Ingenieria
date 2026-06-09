#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:38:23 2024

@author: pablo
"""

import numpy as np
import roboticstoolbox as rtb
import matplotlib.pyplot as plt 

dp = rtb.DHRobot(
    [
        rtb.RevoluteDH(a=0.2,m=1.5,
            r=np.array([-0.1, 0, 0]),
            I=np.array([0,0,0,0,0,0,0,0,1e-3]),
            B=1, G=100),
        rtb.RevoluteDH(a=0.2,m=1,
            r=np.array([-0.1, 0, 0]),
            I=np.array([0,0,0,0,0,0,0,0,1e-4]),
            B=1, G=100)
    ],
    gravity = np.array([0, -9.8, 0]), # Ojo con el signo, la gravedad va hacia abajo con signo positivo
    name="dp")

print(dp)
print(dp.dynamics())

# Revisar los siguientes métodos de DHRobot 
# perturb: produce una variación de los parámetros dinámicos y resulta útil para evaluar efecto de incertezas en el modelo
# dp.inertia(q) : obtiene la matriz M en la posición articular q
# dp.coriolis(q, qd) : obtiene la matriz C en la posición articular q con velocidad qd
# dp.gravload(q) : obtiene el vector G para la posición articular q
# tau = rne(q, qd, qdd, grav, fext) : dinámica inversa. Resulta muy útil al momento de calcular la ley Feedforward


# Simulación del sistema dinámico
# De la docu:
# fdyn(T, q0, torque=None, torque_args={}, qd0=None, solver='RK45', solver_args={}, dt=None, progress=False) 
# Integrate forward dynamics
#    Parameters
#            T (float) – integration time
#            q0 (array_like) – initial joint coordinates
#            qd0 (array_like) – initial joint velocities, assumed zero if not given
#            Q – a function that computes torque as a function of time


def control(robot, t, q, qd):
    return 20*([np.pi/2,0]-q)-0.2*qd

tg = dp.nofriction(coulomb=True, viscous=False).fdyn(5, [0,0],Q=control,qd0=np.zeros((2,)),dt=1e-3)

#tg = dp.fdyn(5, np.array([0,0]),qd0=np.array([0,0]))
plt.figure()
plt.plot(tg.t,tg.q)
plt.show()

