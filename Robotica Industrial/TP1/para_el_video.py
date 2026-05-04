import numpy as np
import matplotlib.pyplot as plt
import spatialmath as sm
import scipy.linalg as sc
import roboticstoolbox as rtb

# =========================
# MODO INTERACTIVO (CLAVE)
# =========================
plt.ion()

# =========================
# ESTADO GLOBAL
# =========================
q_last_global = None


# =========================================================
# ROBOT
# =========================================================
class irb140_clase(rtb.DHRobot):
    def __init__(self, *args, **kwargs):
        super().__init__([
            rtb.RevoluteDH(alpha=-np.pi / 2, a=0.07, d=0.352),
            rtb.RevoluteDH(a=0.36, offset=-np.pi / 2),
            rtb.RevoluteDH(alpha=np.pi / 2, offset=np.pi),
            rtb.RevoluteDH(d=0.38, alpha=-np.pi / 2),
            rtb.RevoluteDH(alpha=np.pi / 2),
            rtb.RevoluteDH(d=0)
        ], name="IRB140")

    def ikine_a(self, POSE, conf=[1, -1, 1], q1_actual=0, q4_actual=0):

        q = np.zeros(6)

        POSE = sm.SE3(0, 0, -self.links[0].d) @ POSE @ sm.SE3(0, 0, -self.links[5].d)
        px, py, pz = POSE.t

        s1 = conf[0] * py
        c1 = conf[0] * px
        q[0] = np.arctan2(s1, c1) if not (px == 0 and py == 0) else q1_actual

        s3 = ((px * np.cos(q[0]) + py * np.sin(q[0]) - self.links[0].a) ** 2 + pz ** 2 - self.links[1].a ** 2 -
              self.links[3].d ** 2) / (2 * self.links[1].a * self.links[3].d)

        if np.abs(s3) > 1:
            print("ERROR: Punto no alcanzable.")
            return np.array([np.nan] * 6)

        c3 = conf[1] * np.sqrt(1 - s3 ** 2)
        q[2] = np.arctan2(s3, c3)

        s2 = (px * np.cos(q[0]) + py * np.sin(q[0]) - self.links[0].a) * (self.links[3].d * np.cos(q[2])) - (
                    self.links[3].d * np.sin(q[2]) + self.links[1].a) * pz
        c2 = (px * np.cos(q[0]) + py * np.sin(q[0]) - self.links[0].a) * (
                    self.links[3].d * np.sin(q[2]) + self.links[1].a) + (self.links[3].d * np.cos(q[2])) * pz
        q[1] = np.arctan2(s2, c2)

        A60 = self.fkine(q - self.offset)
        R_30 = A60.R
        R_63 = R_30.T @ POSE.R

        c5 = np.clip(R_63[2, 2], -1, 1)
        q[4] = np.arctan2(conf[2] * np.sqrt(1 - c5 ** 2), c5)

        if np.abs(R_63[1, 2]) < 1E-9 and np.abs(R_63[0, 2]) < 1E-9:
            q[3] = q4_actual
            q[5] = np.arctan2(R_63[1, 0], R_63[0, 0]) - q4_actual
        else:
            q[3] = np.arctan2(conf[2] * R_63[1, 2], conf[2] * R_63[0, 2])
            q[5] = np.arctan2(conf[2] * R_63[2, 1], -conf[2] * R_63[2, 0])

        q = np.angle(np.exp(1j * (q - self.offset)))
        return q


# =========================================================
# SIMULACION
# =========================================================
def simular_movimiento(robot, POSE_ini, POSE_fin, q0, tiempo_mov=2, n_steps=100):
    dx = (POSE_fin.t - POSE_ini.t) / n_steps
    dx = dx.reshape(3, 1)

    dt = tiempo_mov / n_steps

    q = np.array(q0, dtype=float).copy()

    q_acum = []
    X_acum = []

    q_prev = q.copy()

    for _ in range(n_steps):
        J = robot.jacob0(q)

        Jv = J[0:3, :]
        Jw = J[3:6, :]

        J_full = np.vstack((Jv, Jw))
        V = np.vstack((dx, np.zeros((3, 1)))) / dt

        qp = sc.pinv(J_full) @ V
        qp = np.reshape(qp, (6,))

        qp += 0.1 * (q_prev - q)
        q_prev = q.copy()

        q += qp * dt

        q_acum.append(q.copy())
        X_acum.append(robot.fkine(q).t)

    return np.array(q_acum), np.array(X_acum)


# =========================================================
# CHECK
# =========================================================
def alcanzable(robot, POSE_fin):
    q = robot.ikine_a(POSE_fin)
    return not np.any(np.isnan(q)), q


# =========================================================
# PLOT
# =========================================================
from matplotlib.animation import FFMpegWriter

def plot_trayectoria(robot, q_traj, X_traj):

    plt.clf()
    fig = plt.gcf()
    ax = fig.add_subplot(111, projection='3d')

    lim = 0.8

    u = np.linspace(0, 2*np.pi, 20)
    v = np.linspace(0, np.pi, 10)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    sphere = np.stack((x,y,z), axis=0).reshape(3,-1)

    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor='blue', edgecolor='blue', alpha=0.3, label='Manipulabilidad posición')
    ]

    # 🎥 Writer de video
    writer = FFMpegWriter(
        fps=30,
        codec='mpeg4'
    )
    filename = "trayectoria_irb140.mp4"

    with writer.saving(fig, filename, dpi=150):

        for q, x_tcp in zip(q_traj, X_traj):

            ax.cla()

            ax.set_xlim(-lim, lim)
            ax.set_ylim(-lim, lim)
            ax.set_zlim(0, lim)

            # 🔥 VISTA DESDE ARRIBA
            ax.view_init(elev=90, azim=-90)

            pts = np.array([T.t for T in robot.fkine_all(q)])
            ax.plot(pts[:,0], pts[:,1], pts[:,2], '-o')

            ax.scatter(x_tcp[0], x_tcp[1], x_tcp[2], color='green')

            J = robot.jacob0(q)
            Jv = J[0:3, :]
            Jw = J[3:6, :]

            Uv, Sv, _ = np.linalg.svd(Jv @ Jv.T)
            Uw, Sw, _ = np.linalg.svd(Jw @ Jw.T)

            Sv = np.sqrt(Sv)
            Sw = np.sqrt(Sw)

            eps = 1e-6
            Sv /= (np.max(Sv) + eps)
            Sw /= (np.max(Sw) + eps)

            scale = 0.2

            ell_v = Uv @ (np.diag(Sv) @ sphere)
            ell_v = scale * ell_v + x_tcp.reshape(3,1)

            ell_w = Uw @ (np.diag(Sw) @ sphere)
            ell_w = scale * ell_w + x_tcp.reshape(3,1)

            ax.plot_surface(
                ell_v[0].reshape(x.shape),
                ell_v[1].reshape(y.shape),
                ell_v[2].reshape(z.shape),
                alpha=0.3,
                color='blue'
            )


            ax.legend(handles=legend_elements, loc='upper right')

            plt.draw()
            writer.grab_frame()   # 🎥 guarda frame
            plt.pause(0.001)

    print(f"Video guardado como: {filename}")


# =========================================================
# MAIN LOOP
# =========================================================
if __name__ == "__main__":

    robot = irb140_clase()

    print("\n=== SIMULADOR IRB140 ===\n")

    while True:

        try:
            print("\n--- NUEVA TRAYECTORIA ---")

            xi, yi, zi = map(float, [input("x0: "), input("y0: "), input("z0: ")])
            xf, yf, zf = map(float, [input("xf: "), input("yf: "), input("zf: ")])

            POSE_ini = sm.SE3(xi, yi, zi)
            POSE_fin = sm.SE3(xf, yf, zf)

            q0 = robot.ikine_a(POSE_ini)

            if np.any(np.isnan(q0)):
                print("Pose inicial inválida")
                continue

            ok, _ = alcanzable(robot, POSE_fin)

            if not ok:
                print("Punto final no alcanzable")
                continue

            print("Trayectoria válida\n")

            q_traj, X_traj = simular_movimiento(robot, POSE_ini, POSE_fin, q0)

            q_last_global = q_traj[-1]

            plot_trayectoria(robot, q_traj, X_traj)

        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

