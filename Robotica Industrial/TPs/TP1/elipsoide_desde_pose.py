import numpy as np
import matplotlib.pyplot as plt
import roboticstoolbox as rtb

# =========================
# 1. Definición del IRB 140
# =========================
class IRB140(rtb.DHRobot):
    def __init__(self):
        super().__init__([
            rtb.RevoluteDH(alpha=-np.pi/2, a=0.07, d=0.352),
            rtb.RevoluteDH(a=0.36, offset=-np.pi/2),
            rtb.RevoluteDH(alpha=np.pi/2, offset=np.pi),
            rtb.RevoluteDH(d=0.38, alpha=-np.pi/2),
            rtb.RevoluteDH(alpha=np.pi/2),
            rtb.RevoluteDH(d=0)
        ], name="IRB140")

# =========================
# 2. Función elipsoide
# =========================
def plot_ellipsoids(ax, robot, q):
    T = robot.fkine(q)
    p = T.t

    J = robot.jacob0(q)
    Jv = J[0:3, :]
    Jw = J[3:6, :]

    def draw_ellipsoid(Jpart, scale, color):
        W = Jpart @ Jpart.T
        U, S, _ = np.linalg.svd(W)
        radii = np.sqrt(S)

        u = np.linspace(0, 2*np.pi, 30)
        v = np.linspace(0, np.pi, 15)

        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones_like(u), np.cos(v))

        sphere = np.stack((x, y, z), axis=0).reshape(3, -1)
        ellipsoid = U @ (np.diag(radii) @ sphere)

        # ESCALADO
        ellipsoid *= scale

        # trasladar
        ellipsoid[0, :] += p[0]
        ellipsoid[1, :] += p[1]
        ellipsoid[2, :] += p[2]

        X = ellipsoid[0, :].reshape(x.shape)
        Y = ellipsoid[1, :].reshape(y.shape)
        Z = ellipsoid[2, :].reshape(z.shape)

        ax.plot_surface(X, Y, Z, alpha=0.3, color=color)

    # posición (grande)
    draw_ellipsoid(Jv, scale=1.0, color='blue')

    # orientación (más chica)
    draw_ellipsoid(Jw, scale=0.2, color='red')

    ax.scatter(p[0], p[1], p[2], color='k', s=50)

# =========================
# 3. Inicializar robot
# =========================
robot = IRB140()

# =========================
# 4. Configuraciones
# =========================
configs = [
    ("Nominal", np.array([0, -np.pi/4, np.pi/4, 0, np.pi/6, 0])),
    ("Límite de alcance", np.array([0, 0, 0, 0, 0, 0])),
    ("Eje base", np.array([0, -np.pi/2, 0, 0, 0, 0]))
]

# =========================
# 5. Loop de gráficos
# =========================
for title, q in configs:
    env = robot.plot(q, block=False)
    ax = env.ax

    plot_ellipsoids(ax, robot, q)

    ax.set_title(f"Manipulabilidad - {title}")
    ax.set_box_aspect([1,1,1])
    plt.show(block=True)

# =========================
# 6. Mostrar todo
# =========================