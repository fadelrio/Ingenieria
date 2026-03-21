#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DoublePendulum: modelo didáctico de un doble péndulo basado en DHRobotGT.

Este módulo contiene:
 - Clase DoublePendulum: define la geometría y dinámica (dos revolutas).
 - ikine_a: solución analítica de la cinemática inversa (2R planar).
 - plot_sim: utilidades de trazado para comparar evolución real vs referencia.
 - animate_robot: animación simple para usar en notebooks.

Comentarios de diseño:
 - El código está pensado para docencia: claridad y trazabilidad por encima de
   optimizaciones. Muchas funciones usan aproximaciones (diferencias finitas,
   interpoladores sencillos) suficientes para prácticas y demostraciones.
 - Las funciones gráficas asumen que la trayectoria de referencia ya está en
   self.q_ref, generada por jtraj/ctraj de la clase base DHRobotGT.
"""
#% Importaciones necesarias
import math
import numpy as np                    # numpy para manejar array y algebra lineal
import roboticstoolbox as rtb         # funcionalidad de robótica (DH, dinámica, fk)
import matplotlib.pyplot as plt       # graficos
from IPython.display import HTML
from matplotlib.animation import FuncAnimation

from .DHRobotGT import DHRobotGT       # robot extendido con generador de trayectorias

#% Preparo el modelo de un doble péndulo
class DoublePendulum(DHRobotGT):
    """
    Robot 2R planar simple, orientado a prácticas:

    - Usa dos eslabones con parámetros DH y masas/inercia especificadas.
    - Hereda generación de trayectorias y simuladores de DHRobotGT.
    - Provee una ikine analítica para convertir poses 2D a q (útil en ctraj).
    """
    def __init__(self):    
        # Definición de los enlaces usando parámetros DH
        eje1 = rtb.RevoluteDH(a=0.2,alpha=0,m=1,
            r=np.array([-0.1, 0, 0]),
            I=np.array([0,0,0,0,0,0,0,0,1E-3]),
            #Jm=1E-4,
            B=0.0, G=1)
        eje2 = rtb.RevoluteDH(a=0.2,alpha=0,m=1.5,
            r=np.array([-0.1, 0, 0]),
            I=np.array([0,0,0,0,0,0,0,0,1E-4]),
            #Jm=1E-4,
            B=0.0, G=1)    

        # Crear la estructura del robot: llamo al constructor de DHRobotGT
        super().__init__([eje1, eje2], name='DoublePendulum',
                         gravity = np.array([0, -9.8, 0]),
                         Ts=1E-3, tacc=0.1, vmax=np.array([2*np.pi,2*np.pi]))

    def ikine_a(self, POSE, conf=1):
        """
        Cinemática inversa analítica para el robot 2R en el plano XY.

        Entrada:
          POSE    : objeto SE3 (usa solo la componente traslacional x,y)
          conf    : elección del codo (+1 ó -1) para seleccionar la solución

        Salida:
          q, status : q es array (q1,q2), status 0 = OK, <0 error

        Notas pedagógicas:
          - Implementa la solución clásica usando ley de cosenos para resolver q2,
            y luego atan2 para q1. Controla alcance y casos degenerados.
        """
        conf = 1 if conf >= 0 else -1
        
        q = np.zeros((2,));
        px, py, pz = POSE.t
        a1 = self.links[0].a
        a2 = self.links[1].a
    
        # Comprobación de alcanzabilidad en el plano
        if (px**2+py**2)>(a1+a2)**2:
            status = -1;
            print(f"El punto ({px:.2f},{py:.2f}) no es alcanzable");
        elif (px**2+py**2)<1E-10:
            # Caso cercano al origen: solución por defecto
            status = 0;
            q[0] = 0;
            q[1] = np.pi;
        else:
            # Ley de cosenos para q2
            c2 = (px**2+py**2-(a1**2+a2**2))/(2*a1*a2);
            s2 = conf * math.sqrt(max(0.0, 1-c2**2))
            q[1] = math.atan2(s2,c2);
            
            # Resolución de q1 por relaciones trigonométricas (evita singularidades)
            s1 = (a2*(py*c2-px*s2)+a1*py)/(px**2+py**2);
            c1 = (a2*(py*s2+px*c2)+a1*px)/(px**2+py**2);
            q[0] = math.atan2(s1,c1);
            status = 0;
            return q,status

    def plot_sim(self,t,q,qd,tau_t=None,tau=None):
        """
        Ploteo de resultados de simulación.

        Entrada:
          t, q, qd : tiempo y señales simuladas (q: Nx2, qd: Nx2)
          tau_t, tau: instantes y valores de torques (opcional)

        Funcionalidad:
          - Dibuja q y q_ref, qd y qd_ref (comparación real vs referencia).
          - Si se pasa tau, añade subgráfica de entradas.
          - Dibuja la trayectoria del extremo final y el error espacio cartesiano.
        """
        num_ejes = q.shape[1]
        colores = plt.rcParams['axes.prop_cycle'].by_key()['color']        
        
        # Ajuste de figuras según si hay señales de torque
        if tau is not None:            
            plt.figure(figsize=(8,6))
            nfigs=3
        else:
            plt.figure(figsize=(8,4))
            nfigs=2

        # Posiciones articulares (real vs referencia)
        plt.subplot(nfigs,1,1)
        for i in range(num_ejes):
            color_eje = colores[i % len(colores)]
            plt.plot(t,q[:, i]*180/np.pi,color=color_eje,linestyle='-',linewidth=1,label=f'$q_{i+1}$')
            plt.plot(self.t_ref,self.q_ref[:, i]*180/np.pi,color=color_eje,linestyle='--',linewidth=1,label=f'$q_{i+1}^{{ref}}$')
        plt.ylabel(r'$q$ [°]')
        plt.legend(loc='upper right')
        plt.title('Evolución del sistema')
        
        # Velocidades articulares (real vs referencia)
        plt.subplot(nfigs,1,2)
        for i in range(num_ejes):
            color_eje = colores[i % len(colores)]
            plt.plot(t,qd[:, i]*180/np.pi,color=color_eje,linestyle='-',linewidth=1,label=f'$\dot{{q}}_{i+1}$')
            plt.plot(self.t_ref,self.qd_ref[:, i]*180/np.pi,color=color_eje,linestyle='--',linewidth=1,label=f'$\dot{{q}}_{i+1}^{{ref}}$')
        plt.ylabel(r'$\dot{q}$ [°/s]')
        plt.legend(loc='upper right')
        
        # Entradas (torques) si se proporcionaron
        if tau is not None:
            plt.subplot(nfigs,1,3)
            for i in range(tau.shape[1]):
                plt.plot(tau_t,tau[:,i],linewidth=1,label=f'$\\tau_{i+1}$')
            plt.xlabel('t [s]')
            plt.ylabel(r'$\tau [Nm]$')
            plt.legend(loc='upper right')
        plt.tight_layout()
                
        # Trayectoria del extremo final (XY) - real vs referencia
        plt.figure(figsize=(5,5))
        trayectoria = self.fkine(q)
        trayectoria_ref = self.fkine(self.q_ref) 
        plt.plot(trayectoria.t[:,0],trayectoria.t[:,1],'b-',linewidth=1,label='real')
        plt.plot(trayectoria_ref.t[:,0],trayectoria_ref.t[:,1],'b--',linewidth=1,label='ref')
        plt.legend(loc='upper right')
        plt.xlabel('X [m]')
        plt.ylabel('Y [m]')
        plt.title('Trayectoria realizada')
        plt.axis([-0.4, 0.4, -0.4, 0.4])	
        plt.tight_layout()
        
        # Error cartesiano (norma) cuando los vectores de tiempo coinciden
        if len(t)==len(self.t_ref):
            plt.figure(figsize=(8,4))
            diferencia = trayectoria_ref.t[:, :2] - trayectoria.t[:, :2]
            error = np.linalg.norm(diferencia, axis=1)
            plt.plot(t,error*1000,linewidth=1)
            plt.xlabel('t [s]')
            plt.ylabel(r'$e [mm]$')
            plt.tight_layout()
        plt.show()
        
    def animate_robot(self, q=None, frame_rate=50, video_file_name=''):
        """
        Crea una animación del doble péndulo (ideal para notebooks).

        - Si q es None, se anima la trayectoria de referencia self.q_ref.
        - Ajusta número de pasos por frame para respetar self.Ts y el frame_rate pedido.
        - Devuelve HTML con el video embebido (ani.to_html5_video()).

        Notas:
         - Renderiza en 2D XY y trazas del extremo. Pensado para demostraciones.
        """
        # ----------------------------------------------------
        # 1. Parámetros y optimización de frames
        # ----------------------------------------------------
        VIDEO_FPS = frame_rate
        
        # Cuántos pasos de simulación hay que saltar para aproximar el FPS pedido
        PASOS_POR_FRAME = max(1, int(1 / (self.Ts * (VIDEO_FPS)))) 

        n_frames_simulacion = len(self.q_ref)
        indices_a_animar = np.arange(0, n_frames_simulacion, PASOS_POR_FRAME)
        interval_ms = 1000 / VIDEO_FPS

        # -----------------------------------------------
        # Preparación del gráfico y de los datos iniciales
        # -----------------------------------------------
        fig, ax = plt.subplots(figsize=(6, 6))
        L = self.a[0]+self.a[1]  # longitud total aproximada para ejes
        ax.set_xlim(-L*1.1, L*1.1) 
        ax.set_ylim(-L*1.1, L*1.1)
        ax.set_aspect('equal') # importante para evitar distorsiones
        ax.grid(True)

        # Línea que representa los dos eslabones y marcadores de masas
        line, = ax.plot([], [], 'o-', lw=3, markersize=8)
        # Trayectoria actual (opcional) y de referencia
        if q is None:
          q = self.q_ref
          path = None
        else:
          path, = ax.plot([], [], 'b:', lw=1, alpha=0.5, label='Trayectoria')
        path_ref, = ax.plot([], [], 'r:', lw=1, alpha=0.5, label='Referencia')

        # Marcar inicio y destino sobre el plano XY
        P = self.fkine(self.q_ref[0]).t
        ax.plot(P[0],P[1],'ro',lw=2,label='Inicio')
        P = self.fkine(self.q_ref[-1]).t
        ax.plot(P[0],P[1],'rx',lw=2,label='Destino')
        ax.legend(loc='upper right')

        # -----------------------------------------------
        # Funciones para la animación (init y update)
        # -----------------------------------------------
        def init():
            # Pone el objeto gráfico en el estado inicial (vacío)
            line.set_data([], [])
            return line,

        def update_plot(frame):
            """
            Actualiza la posición del péndulo para el índice 'frame'.

            - Obtiene transformaciones con fkine_all (lista de SE3 para eslabones).
            - Construye arrays x,y para la línea que une origen-P1-P2.
            - Actualiza trazas si corresponde.
            """
            q_actual = q[frame] # Vector [q1, q2]
            A = self.fkine_all(q_actual)

            # Transformaciones: A[1] es base->joint1, A[2] es base->extremo2
            P2 = A[2].t
            P1 = A[1].t

            # Puntos a dibujar (Origen, articulación intermedia, extremo)
            x = [0, P1[0], P2[0]]
            y = [0, P1[1], P2[1]]
            line.set_data(x, y)
            
            if path is not None:
              # Construye la trayectoria realizada hasta el frame actual
              q_historial = q[:frame + 1, :]            
              T_historial_P2 = self.fkine(q_historial)
              x_path = np.array([T.t[0] for T in T_historial_P2]).ravel()
              y_path = np.array([T.t[1] for T in T_historial_P2]).ravel()
              path.set_data(x_path, y_path)

            # Traza de referencia (siempre usando self.q_ref)
            q_ref_historial = self.q_ref[:frame + 1, :]
            T_historial_P2_ref = self.fkine(q_ref_historial)
            x_path_ref = np.array([T.t[0] for T in T_historial_P2_ref]).ravel()
            y_path_ref = np.array([T.t[1] for T in T_historial_P2_ref]).ravel()
            path_ref.set_data(x_path_ref, y_path_ref)

            if path is None:
                return line, path_ref
            return line, path, path_ref

        # -----------------------------------------------
        # Creación del objeto FuncAnimation y salida
        # -----------------------------------------------
        n_frames = len(q)
        ani = FuncAnimation(
            fig, 
            update_plot, 
            frames=indices_a_animar, 
            init_func=init, 
            blit=True, 
            interval=interval_ms,
            repeat=False 
        )

        # Guardado opcional (ffmpeg debe estar instalado si se pide mp4)
        if len(video_file_name)>0:
            ani.save(video_file_name, writer='ffmpeg', fps=VIDEO_FPS)

        # Cerrar la figura para que no se muestre dos veces en notebooks
        plt.close(fig)
        return HTML(ani.to_html5_video())         

if __name__ == "__main__":
    # Ejemplo rápido de uso / prueba
    dp = DoublePendulum()

    qr = np.array([-np.pi/2,0])
    qz = np.zeros((2,))

    print(dp)
    print(dp.dynamics())
    print(f'Tiempo de muestreo [ms]: {dp.Ts*1000}')

    N_segments = 3
    q_dest = (np.random.rand(N_segments, dp.n))*np.pi
    POSES_dest = dp.fkine(q_dest)
    Tj = np.random.rand(N_segments, )+1

    # Trayectoria JOINT    
    dp.jtraj(q_dest,Tj)

    # Pruebo la simulación PD (ejemplo sencillo, recortado para docencia)
    Kp = 40
    Kd = 4
    def control_PD(robot,t,q,qd):
        _,q_ref,_,_ = dp.get_control_ref(t)
        u = Kp * (q_ref-q) - Kd*qd
        u = np.clip(u,-10,10)
        return u
    tdis,qdis,qd,u = dp.sim_dis_control(control_PD)
    dp.plot_sim(tdis,qdis,qd,u)
    
    #dp.animate_robot(frame_rate=4,video_file_name='dp.mp4')



