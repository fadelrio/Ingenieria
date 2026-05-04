import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import threading
import roboticstoolbox as rtb
from spatialmath import SE3

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
# PARAMETROS
# =========================
step = 0.05
eps = 1e-3

mode = "manual"
traj_q = None
traj_index = 0
playing = False
computing = False
waiting_click = False

# =========================
# LIMITES ARTICULARES
# =========================
joint_limits = np.array([
    [-np.pi, np.pi],
    [-np.pi/2, np.pi/2],
    [-2.6, 2.6],
    [-np.pi, np.pi],
    [-2.0, 2.0],
    [-np.pi, np.pi],
])

def clamp_q(q):
    return np.clip(q, joint_limits[:,0], joint_limits[:,1])

# =========================
# CINEMATICA
# =========================
def robot_points(robot, q):
    Ts = robot.fkine_all(q)
    return np.array([T.t for T in Ts])

def compute_cartesian_trajectory(robot, q_init, p_goal):
    q = q_init.copy()
    traj = [q.copy()]

    while True:
        T = robot.fkine(q)
        p = T.t

        delta = p_goal - p
        norm = np.linalg.norm(delta)

        if norm < eps:
            break

        direction = delta / norm
        dp = direction * step

        J = robot.jacob0(q)
        dq = np.linalg.pinv(J[0:3, :]) @ dp

        q = clamp_q(q + dq)
        traj.append(q.copy())

    return np.array(traj)

# =========================
# PLOT
# =========================
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.35)

def draw(q):
    ax.cla()

    pts = robot_points(robot, q)
    ax.plot(pts[:,0], pts[:,1], pts[:,2], '-o')

    T = robot.fkine(q)
    p = T.t
    R = T.R

    ax.scatter(p[0], p[1], p[2], color='k')

    L = 0.1
    ax.plot([p[0], p[0]+L*R[0,0]], [p[1], p[1]+L*R[1,0]], [p[2], p[2]+L*R[2,0]], 'r')
    ax.plot([p[0], p[0]+L*R[0,1]], [p[1], p[1]+L*R[1,1]], [p[2], p[2]+L*R[2,1]], 'g')
    ax.plot([p[0], p[0]+L*R[0,2]], [p[1], p[1]+L*R[1,2]], [p[2], p[2]+L*R[2,2]], 'b')

    ax.set_box_aspect([1,1,1])
    ax.set_title("IRB140")

    plt.draw()

# =========================
# SLIDERS
# =========================
sliders = []

for i in range(6):
    ax_s = plt.axes([0.2, 0.05 + i*0.035, 0.6, 0.02])
    sliders.append(Slider(ax_s, f'q{i+1}', -np.pi, np.pi, valinit=0))

def update(val):
    if mode == "manual":
        q = np.array([s.val for s in sliders])
        draw(q)

for s in sliders:
    s.on_changed(update)

# =========================
# THREAD (solo cálculo)
# =========================
def worker(q_init, p_goal):
    global traj_q, computing, mode, playing, traj_index

    traj_q = compute_cartesian_trajectory(robot, q_init, p_goal)

    traj_index = 0
    playing = True
    computing = False
    mode = "trajectory"

# =========================
# CLICK HANDLER (3D pick simple)
# =========================
def on_click(event):
    global waiting_click, computing

    if not waiting_click:
        return

    if event.inaxes != ax:
        return

    x, y = event.xdata, event.ydata
    p_goal = np.array([x, y, 0.3])

    print(f"✔ Punto seleccionado: {p_goal}")

    q_init = np.array([s.val for s in sliders])

    # IK solo como seed
    try:
        sol = robot.ikine_LM(SE3.Trans(p_goal), q0=q_init)
        if sol.success:
            q_seed = sol.q
            print("✔ IK encontró seed buena")
        else:
            q_seed = q_init
            print("⚠ IK falló, usando configuración actual")
    except:
        q_seed = q_init
        print("⚠ IK error, usando seed actual")

    waiting_click = False
    computing = True
    mode = "computing"

    thread = threading.Thread(
        target=worker,
        args=(q_seed, p_goal),
        daemon=True
    )
    thread.start()

fig.canvas.mpl_connect('button_press_event', on_click)

# =========================
# BOTONES
# =========================
ax_btn = plt.axes([0.82, 0.2, 0.15, 0.05])
btn = Button(ax_btn, "Go To")

def on_go(event):
    global waiting_click
    print("👉 Click en el gráfico para seleccionar objetivo")
    waiting_click = True

btn.on_clicked(on_go)

ax_btn2 = plt.axes([0.82, 0.12, 0.15, 0.05])
btn_manual = Button(ax_btn2, "Manual")

def set_manual(event):
    global mode
    mode = "manual"

btn_manual.on_clicked(set_manual)

# =========================
# TIMER (ANIMACIÓN)
# =========================
def tick():
    global traj_index, playing

    if mode == "trajectory" and playing and traj_q is not None:
        q = traj_q[traj_index]
        traj_index += 1

        if traj_index >= len(traj_q):
            traj_index = len(traj_q) - 1
            playing = False

        draw(q)

timer = fig.canvas.new_timer(interval=30)
timer.add_callback(tick)
timer.start()

# =========================
# INIT
# =========================
draw(np.zeros(6))
plt.show()