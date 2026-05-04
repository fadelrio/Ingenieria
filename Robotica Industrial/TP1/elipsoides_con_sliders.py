import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import roboticstoolbox as rtb
from matplotlib.patches import Patch

# =========================
# Robot IRB140
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

robot = IRB140()

# =========================
# Funciones
# =========================
def robot_points(robot, q):
    Ts = robot.fkine_all(q)
    return np.array([T.t for T in Ts])

def ellipsoid(J):
    U, S, _ = np.linalg.svd(J @ J.T)
    return U, np.sqrt(S)

# =========================
# Plot
# =========================
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.3)

def draw(q):
    ax.cla()

    # ===== Robot =====
    pts = robot_points(robot, q)
    ax.plot(pts[:,0], pts[:,1], pts[:,2], '-o', label="Robot")

    # ===== TCP =====
    T = robot.fkine(q)
    p = T.t
    R = T.R

    # ===== Jacobiano =====
    J = robot.jacob0(q)
    Jv = J[0:3, :]
    Jw = J[3:6, :]

    Uv, rv = ellipsoid(Jv)
    Uw, rw = ellipsoid(Jw)

    # ===== Esfera base =====
    u = np.linspace(0, 2*np.pi, 20)
    v = np.linspace(0, np.pi, 10)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    sphere = np.stack((x,y,z), axis=0).reshape(3,-1)

    # ===== Elipsoide posición (azul) =====
    ell_v = Uv @ (np.diag(rv) @ sphere) + p.reshape(3,1)
    ax.plot_surface(
        ell_v[0].reshape(x.shape),
        ell_v[1].reshape(y.shape),
        ell_v[2].reshape(z.shape),
        alpha=0.3,
        color='blue'
    )

    # ===== Elipsoide orientación (rojo) =====
    ell_w = Uw @ (np.diag(rw) @ sphere)
    ell_w = 0.2*ell_w + p.reshape(3,1)

    ax.plot_surface(
        ell_w[0].reshape(x.shape),
        ell_w[1].reshape(y.shape),
        ell_w[2].reshape(z.shape),
        alpha=0.3,
        color='red'
    )

    # ===== TCP point =====
    ax.scatter(p[0], p[1], p[2], color='k')

    # ===== Terna TCP =====
    L = 0.1
    ax.plot([p[0], p[0]+L*R[0,0]], [p[1], p[1]+L*R[1,0]], [p[2], p[2]+L*R[2,0]], color='r')
    ax.plot([p[0], p[0]+L*R[0,1]], [p[1], p[1]+L*R[1,1]], [p[2], p[2]+L*R[2,1]], color='g')
    ax.plot([p[0], p[0]+L*R[0,2]], [p[1], p[1]+L*R[1,2]], [p[2], p[2]+L*R[2,2]], color='b')

    # ===== Legend (PROXY) =====
    legend_elements = [
        Patch(facecolor='blue', edgecolor='blue', alpha=0.3, label='Manipulabilidad posición'),
        Patch(facecolor='red', edgecolor='red', alpha=0.3, label='Manipulabilidad orientación')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_box_aspect([1,1,1])
    ax.set_title("Manipulabilidad IRB140")

    plt.draw()

# =========================
# Sliders
# =========================
sliders = []

for i in range(6):
    ax_s = plt.axes([0.2, 0.05 + i*0.035, 0.6, 0.02])
    s = Slider(ax_s, f'q{i+1}', -np.pi, np.pi, valinit=0)
    sliders.append(s)

def update(val):
    q = np.array([s.val for s in sliders])
    draw(q)

for s in sliders:
    s.on_changed(update)

# =========================
# Inicial
# =========================
draw(np.zeros(6))
plt.show()

