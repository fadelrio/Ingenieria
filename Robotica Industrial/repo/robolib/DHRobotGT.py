import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm 

# la funcionalidad específica de robótica está en el toolbox
# spatialmath tiene define los grupos de transformaciones especiales: rotación SO3 y eculideo SE3
import spatialmath as sm

# Extiendo la clase DHRobot para que incluya el generador de trayectorias joint y cartesiano
from roboticstoolbox import DHRobot


class DHRobotGT(DHRobot):
    """
    Extensión de DHRobot con herramientas para generación de trayectorias y simulación.
    
    Propósito didáctico: concentrar generación de referencias (joint/cartesiano) y
    simulación (continuo y discreto) en la misma clase para facilitar prácticas.
    
    Notas:
      - Algunas funciones usan aproximaciones numéricas sencillas (diff) para velocidad/
        aceleración articular; son suficientes para ejercicios pero no reemplazan
        métodos más robustos para sistemas reales.
      - Los valores por defecto (Ts, tacc, vmax) son configurables al instanciar.
    """
    def __init__(self, *args, tacc=0.1, Ts=1E-3, vmax=np.array([2*np.pi,2*np.pi]), **kwargs):
        # Inicializa DHRobot y agrega parámetros para generación de trayectorias
        super().__init__(*args, **kwargs)
        self.tacc = tacc    # tiempo de aceleración (zonas trapezoidales)
        self.Ts = Ts        # periodo de muestreo / integración
        self.vmax = vmax    # velocidades máximas por articulación (vector)
        # Vectores que almacenan la referencia y la simulación para uso posterior / plotting
        self.q_sim = []
        self.qd_sim = []
        self.qd_sim_f = []
        self.q_ref = []
        self.qd_ref = []
        self.qdd_ref = []
        self.t_ref = []
        self.u = []

        self.Nr = np.diag([link.G for link in self.links])


    def get_control_ref(self, t):
        """
        Devuelve la referencia (posición, velocidad, aceleración) en el instante t.
        Busca la muestra más cercana hacia la izquierda en t_ref.

        Lanza ValueError si no hay referencias definidas.
        """
        if len(self.t_ref) == 0:
            raise ValueError("No hay trayectorias deseadas definidas")
        # busca el índice dentro del vector
        k = np.searchsorted(self.t_ref, t, side='right') - 1

        # Dejo al índice dentro del rango
        if k < 0:
            k = 0
        elif k >= len(self.t_ref):
            k = len(self.t_ref) - 1
            
        return self.t_ref[k], self.q_ref[k], self.qd_ref[k], self.qdd_ref[k]

    def interp_trap(self, A, B, C, Tj):
        """
        Interpolador trapezoidal (zonas 1 y 2) para un segmento definido por tres puntos.
        
        Entradas:
          A, B, C: vectores de estado (por ejemplo posiciones articulares o vector
                   [x,y,z,rotvec...] para poses).
          Tj: duración del segmento (tiempo entre B->C en la parametrización usada).
        
        Salidas:
          q_aux, qd_aux, qdd_aux: matrices donde cada columna es la muestra en el
                                 tiempo correspondiente dentro del segmento.
        
        Comentarios:
          - Implementación simple que construye dos zonas: la rampa de aceleración
            (de -tacc a +tacc) y la fase central con velocidad constante.
          - Asume que A, B, C son arrays con la misma dimensión; las operaciones
            están vectorizadas por componente.
          - Devuelve matrices con filas = dimensiones del espacio (n articulaciones
            o n componentes de pose) y columnas = muestras temporales.
        """
        DA = A - B
        DC = C - B

        # Zona 1: desde -tacc a +tacc (fase de aceleración)
        tseg = np.arange(-self.tacc + self.Ts, self.tacc + self.Ts, self.Ts)
    
        # aceleración constante en zona 1 (vectorizada por componente)
        qdd_aux = np.outer((DC / Tj + DA / self.tacc) / (2 * self.tacc), np.ones(len(tseg)))
        # velocidad y posición integradas sobre tseg (formas vectorizadas)
        qd_aux = (DC / Tj)[:, np.newaxis] * (tseg + self.tacc) / (2 * self.tacc) + \
                 (DA / self.tacc)[:, np.newaxis] * (tseg - self.tacc) / (2 * self.tacc)
        q_aux = (DC / Tj)[:, np.newaxis] * (tseg + self.tacc)**2 / (4 * self.tacc) + \
                (DA / self.tacc)[:, np.newaxis] * (tseg - self.tacc)**2 / (4 * self.tacc) + \
                np.outer(B, np.ones(len(tseg)))
    
        # Zona 2: fase central con velocidad aproximadamente constante
        # construyo otro tseg desde +tacc hasta Tj - tacc
        tseg = np.arange(self.tacc + self.Ts, Tj - self.tacc + 0.5 * self.Ts, self.Ts)
    
        # concateno la zona 2 (aceleración nula, velocidad = DC/Tj, posición lineal)
        qdd_aux = np.hstack([qdd_aux, np.zeros((len(B), len(tseg)))])
        qd_aux = np.hstack([qd_aux, np.outer(DC / Tj, np.ones(len(tseg)))])
        q_aux = np.hstack([q_aux, np.outer(DC / Tj, tseg) + np.outer(B, np.ones(len(tseg)))])
        return q_aux, qd_aux, qdd_aux

    def jtraj(self, q_dest, Td):
        """
        Genera una trayectoria conjunta (por articulación) a partir de puntos de paso.

        Entradas:
          q_dest: matriz donde cada fila es un punto de paso (configuración articular).
          Td: vector con tiempos deseados para cada movimiento entre puntos.
        
        Salidas:
          t, q, qd, qdd: referencias temporales (t) y señales (q, qd, qdd).
        
        Comentarios:
          - Usa interp_trap para cada segmento. Calcula Tj como máximo entre
            límite por vmax, Td y 2*tacc para garantizar suficiente tiempo.
          - La salida q tiene forma (N_muestras, n_links) guardada en self.q_ref.
          - La cinemática directa se evalúa sobre la trayectoria articular para obtener
            POSES, útil para visualización. Aquí se guarda la referencia en atributos.
          - Atención: Td se puede modificar en el proceso (cuando el último Td se
            fuerza a 0 si no hay movimiento siguiente).
        """
        q = np.empty((self.nlinks, 0)); qd = np.empty((self.nlinks, 0)); qdd = np.empty((self.nlinks, 0))
        A = q_dest[0, :];
        for i in range(len(q_dest)):
          B = q_dest[i, :]
          if i < len(q_dest) - 1:
            C = q_dest[i+1, :]
          else:
            C = B
            Td[i] = 0
          # decisión de duración según velocidades máximas y tiempos pedidos
          Tj = np.max((np.max(np.abs(C - B) / self.vmax), Td[i], 2 * self.tacc))
          q_aux, qd_aux, qdd_aux = self.interp_trap(A, B, C, Tj)
          q = np.hstack([q, q_aux]); qd = np.hstack([qd, qd_aux]); qdd = np.hstack([qdd, qdd_aux]);
          A = q[:, -1]
        t = np.linspace(0, q.shape[1], num=q.shape[1]) * self.Ts
    
        # Calculo la trayectoria cartesiana deseada (lista de SE3)
        POSES = self.fkine(q.transpose())  # devuelve una lista/array de SE3
        # guardo referencias en la clase para uso posterior en control/simulación
        self.t_ref = t; self.q_ref = q.T; self.qd_ref = qd.T; self.qdd_ref = qdd.T
        return self.t_ref, self.q_ref, self.qd_ref, self.qdd_ref

    def ctraj(self, POSE_dest, Td):
        """
        Genera una trayectoria en el espacio cartesiano entre POSES deseadas.
        
        Estrategia:
          - Interpola en el espacio de parámetros (posición + EulerVec) usando interp_trap.
          - Reconstruye las SE3 intermedias y calcula la cinemática inversa (ikine_a)
            para obtener las configuraciones articulares correspondientes.
          - Deriva numéricamente para obtener velocidades y aceleraciones articulares.
        
        Observaciones importantes:
          - La parametrización rota con EulerVec puede inducir discontinuidades si las
            orientaciones están lejos; es adecuada para ejercicios, pero no robusta para
            trayectorias de orientación complejas (usar slerp o splines en SO(3) para eso).
          - ikine_a debe converger en cada paso; si falla, la rutina necesita manejo de errores.
        """
        POSEA = POSE_dest[0]
        POSES = []
        for i in range(len(POSE_dest)):
          POSEB = POSE_dest[i]
          if i < len(POSE_dest) - 1:
            POSEC = POSE_dest[i+1]
          else:
            POSEC = POSEB
            Td[i] = 0
          # Concateno traslación + vector de Euler para interpolar en R^6 (o similar)
          A = np.concatenate((POSEA.t, POSEA.eulervec())) if False else np.concatenate((POSEA.t, POSEA.eulervec()))
          # las dos líneas previas eran redundantes en versiones anteriores; usar B y C correctamente
          A = np.concatenate((POSEA.t, POSEA.eulervec()))
          B = np.concatenate((POSEB.t, POSEB.eulervec()))
          C = np.concatenate((POSEC.t, POSEC.eulervec()))
          Tj = np.max([Td[i], 2 * self.tacc])
        
          pos, _, _ = self.interp_trap(A, B, C, Tj)
          # Reconstruyo SE3 a partir de cada columna de 'pos' (posición + EulerVec)
          POSES.extend([sm.SE3(pos[0:3, j]) * sm.SE3.EulerVec(pos[3:, j]) for j in range(pos.shape[1])])
        
          POSEA = POSES[-1]
        
        # Para cada pose calculo la cinemática inversa (solución articular)
        q = np.zeros((len(POSES), self.nlinks))
        for i in range(len(POSES)):
          q[i, :], _ = self.ikine_a(POSES[i])
        
        # Obtengo la velocidad articular derivando numéricamente (diferencias finitas)
        qd = np.diff(q, axis=0) / self.Ts
        # Ajustar la longitud de qd para que coincida con q (última muestra cero)
        qd = np.vstack([qd, np.zeros(self.nlinks,)])
        
        # Obtengo la aceleración articular derivando numéricamente
        qdd = np.diff(qd, axis=0) / self.Ts
        # Ajustar la longitud de qdd para que coincida con qd (última muestra cero)
        qdd = np.vstack([qdd, np.zeros(self.nlinks,)])
        
        t = np.linspace(0, len(q), num=len(q)) * self.Ts
        self.t_ref = t; self.q_ref = q; self.qd_ref = qd; self.qdd_ref = qdd
        return self.t_ref, self.q_ref, self.qd_ref, self.qdd_ref

    def sim_cont_control(self, control_law_func, solver_kwargs=None):
      """
      Simulación continua usando el solver interno fdyn de roboticstoolbox.
      
      control_law_func: función que será llamada por el integrador para calcular
                        el control en tiempo continuado.
                        Debe tener la firma aceptada por fdyn (ver toolbox).
      Retorna: tiempo, q, qd, None (el cuarto valor puede extenderse si se quiere)
      
      Comentarios:
        - Aquí se construye un sistema sin fricción (nofriction) y se integra hasta
          t_ref[-1] usando la condición inicial tomada de la primera muestra de referencia.
        - El uso de fdyn permite integrar con RK45 y usar tolerancias configurables.
      """
      # Parámetros del solver RK45
      if solver_kwargs is None:
        solver_kwargs = {
            'rtol': 1e-6     # Tolerancia relativa
        #    'atol': 1e-8     # Tolerancia absoluta (opcional)
        #    'max_step': 0.1   # Tamaño máximo del paso de integración (opcional)
        }

      # La condición inicial sale de la primera muestra de las referencias
      tg = self.nofriction(coulomb=True, viscous=False).fdyn(self.t_ref[-1], 
                                                             self.q_ref[0],                                                             
                                                             control_law_func, 
                                                             qd0=self.qd_ref[0],
                                                             solver_args=solver_kwargs,
                                                             progress=True)
      return tg.t, tg.q , tg.qd, None      


    def sim_dis_control(self, control_law_func, omega_f=None, solver_kwargs=None):
      """
      Simulación discreta por integración por pasos de tamaño Ts.
      
      control_law_func: función (robot, t, q, qd) -> tau (vector de torques) que
                        devuelve la entrada a aplicar en cada paso.
      omega_f: ancho de banda del filtro pasa bajos de la velocidad
      
      Estrategia:
        - Itera sobre muestras en self.t_ref. En cada paso calcula la ley de control
          con el estado simulado anterior y aplica esa entrada durante un intervalo
          Ts resolviendo un fdyn corto para obtener el siguiente estado.
        - Almacena históricos de entradas, q_sim y qd_sim.
      
      Comentarios:
        - Es una manera simple y didáctica de simular control discreto contra un
          modelo dinámico; asume que control_law_func es computable con los estados.
        - El integrador fdyn se usa para propagar el estado durante un intervalo Ts.
      """
      # Parámetros del solver RK45
      if solver_kwargs is None:
        solver_kwargs = {
            'rtol': 1e-6     # Tolerancia relativa
        }

      if omega_f is None:
         alpha = 0
      else:
         alpha = np.exp(-omega_f*self.Ts)
      # Inicializo vectores para simulacion
      self.u = np.zeros_like(self.q_ref)
      self.q_sim = np.zeros_like(self.q_ref)
      self.qd_sim = np.zeros_like(self.qd_ref)
      self.qd_sim_f = np.zeros_like(self.qd_ref)

      # La condición inicial sale de la primera muestra de las referencias
      self.q_sim[0, :] = self.q_ref[0, :]
      self.qd_sim[0, :] = self.qd_ref[0, :]
      self.qd_sim_f[0, :] = self.qd_ref[0, :]


      # Realizo la simulación por pasos
      for idx in tqdm(range(1, len(self.t_ref))):        
        # Calculo la ley de control discreta usando el estado simulado anterior
        self.u[idx, :] = control_law_func(self, self.t_ref[idx], self.q_sim[idx-1], self.qd_sim_f[idx-1])

        # Integro durante Ts partiendo del último estado simulado y aplicando u constante
        tg = self.nofriction(coulomb=True, viscous=False).fdyn(self.Ts, 
                                                                self.q_sim[idx-1],
                                                                qd0=self.qd_sim_f[idx-1],
                                                                Q=lambda r, t, q, qd: self.u[idx],                                                          
                                                                solver_args=solver_kwargs)
        # Tomo la última muestra devuelta por el integrador como nuevo estado
        self.q_sim[idx] = tg.q[-1, :]
        self.qd_sim[idx] = tg.qd[-1, :]
        # Filtro la medición de velocidad
        self.qd_sim_f[idx] = alpha * self.qd_sim_f[idx-1] + (1-alpha) * self.qd_sim[idx]

      return self.t_ref, self.q_sim, self.qd_sim, self.u


