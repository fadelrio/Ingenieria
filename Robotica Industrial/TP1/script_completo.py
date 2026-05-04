import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Patch
import spatialmath as sm
import scipy.linalg as sc
import roboticstoolbox as rtb

# =========================================================
# ROBOT (IGUAL QUE TU SCRIPT)
# =========================================================
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

# =========================================================
# MODO 1: SLIDERS (ENCAPSULADO SIN CAMBIOS LOGICOS)
# =========================================================
class SliderMode:
    def __init__(self, robot):
        self.robot = robot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.sliders = []
        self.active = True

        plt.subplots_adjust(bottom=0.3)

        for i in range(6):
            ax_s = plt.axes([0.2, 0.05 + i*0.03, 0.6, 0.02])
            self.sliders.append(
                Slider(ax_s, f'q{i+1}', -np.pi, np.pi, valinit=0)
            )

        for s in self.sliders:
            s.on_changed(self.update)

        self.draw(np.zeros(6))

    def fk_points(self, q):
        return np.array([T.t for T in self.robot.fkine_all(q)])

    def ellipsoid(self, J):
        U, S, _ = np.linalg.svd(J @ J.T)
        return U, np.sqrt(S)

    def draw(self, q):

        self.ax.cla()

        pts = self.fk_points(q)
        self.ax.plot(pts[:,0], pts[:,1], pts[:,2], '-o')

        T = self.robot.fkine(q)
        p = T.t
        R = T.R

        J = self.robot.jacob0(q)
        Jv = J[0:3, :]
        Jw = J[3:6, :]

        Uv, Sv = self.ellipsoid(Jv)
        Uw, Sw = self.ellipsoid(Jw)

        u = np.linspace(0, 2*np.pi, 20)
        v = np.linspace(0, np.pi, 10)

        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones_like(u), np.cos(v))

        sphere = np.stack((x,y,z), axis=0).reshape(3,-1)

        scale = 0.2

        ell_v = scale * (Uv @ (np.diag(Sv) @ sphere)) + p.reshape(3,1)
        ell_w = scale * (Uw @ (np.diag(Sw) @ sphere)) + p.reshape(3,1)

        self.ax.plot_surface(*ell_v.reshape(3, *x.shape), alpha=0.3, color='blue')
        self.ax.plot_surface(*ell_w.reshape(3, *x.shape), alpha=0.3, color='red')

        L = 0.1
        self.ax.plot([p[0], p[0]+L*R[0,0]],
                     [p[1], p[1]+L*R[1,0]],
                     [p[2], p[2]+L*R[2,0]], color='r')

        self.ax.plot([p[0], p[0]+L*R[0,1]],
                     [p[1], p[1]+L*R[1,1]],
                     [p[2], p[2]+L*R[2,1]], color='g')

        self.ax.plot([p[0], p[0]+L*R[0,2]],
                     [p[1], p[1]+L*R[1,2]],
                     [p[2], p[2]+L*R[2,2]], color='b')

        legend = [
            Patch(facecolor='blue', label='Posición'),
            Patch(facecolor='red', label='Orientación')
        ]

        self.ax.legend(handles=legend)
        self.ax.set_title("Modo sliders")

        self.fig.canvas.draw_idle()

    def update(self, val):
        q = np.array([s.val for s in self.sliders])
        self.draw(q)

    def show(self):
        self.fig.set_visible(True)

    def hide(self):
        self.fig.set_visible(False)


# =========================================================
# MODO 2: PLACEHOLDER PARA TU OTRO SCRIPT
# (misma idea: encapsular sin tocar lógica interna)
# =========================================================
class TrajectoryMode:
    def __init__(self, robot):
        self.robot = robot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.set_visible(False)

    def run_demo(self):
        self.ax.cla()
        self.ax.set_title("Modo trayectoria (placeholder)")
        self.ax.plot([0,1],[0,1],[0,1])
        self.fig.canvas.draw_idle()

    def show(self):
        self.fig.set_visible(True)
        self.run_demo()

    def hide(self):
        self.fig.set_visible(False)


# =========================================================
# CONTROLLER (TOGGLE REAL SIN QT CRASH)
# =========================================================
class Controller:
    def __init__(self):
        self.slider_mode = SliderMode(robot)
        self.traj_mode = TrajectoryMode(robot)
        self.mode = 0

        self.button_ax = self.slider_mode.fig.add_axes([0.02, 0.85, 0.2, 0.1])
        self.button = Button(self.button_ax, "TOGGLE")

        self.button.on_clicked(self.toggle)

        self.slider_mode.show()
        self.traj_mode.hide()

    def toggle(self, event):

        if self.mode == 0:
            self.slider_mode.hide()
            self.traj_mode.show()
        else:
            self.traj_mode.hide()
            self.slider_mode.show()

        self.mode = 1 - self.mode


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    Controller()
    plt.show()