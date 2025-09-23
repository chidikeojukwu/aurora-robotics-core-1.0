# two_link_3d_sliders.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)

# --------- link lengths (units) ----------
L1 = 1.5
L2 = 1.0

def Rz(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c,-s,0],
                     [s, c,0],
                     [0, 0,1]])

def Ry(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[ c,0, s],
                     [ 0,1, 0],
                     [-s,0, c]])

def fk_3d(q_yaw, q_sh, q_el):
    """Return 3D points (base, joint, ee) for a 2-link arm with
       base-yaw (about z), then shoulder pitch (about y), then elbow pitch (about y)."""
    R0 = Rz(q_yaw)
    R1 = R0 @ Ry(q_sh)
    p0 = np.zeros(3)
    p1 = R1 @ np.array([L1, 0, 0])
    p2 = p1 + (R1 @ Ry(q_el)) @ np.array([L2, 0, 0])
    return p0, p1, p2

# --------- figure/axes ----------
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("3D 2-Link Arm (yaw, shoulder, elbow)")
ax.set_box_aspect((1,1,1))
lim = L1 + L2 + 0.3
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')

# initial angles (deg -> rad)
yaw0, sh0, el0 = 30.0, 20.0, 40.0
yaw = np.deg2rad(yaw0); sh = np.deg2rad(sh0); el = np.deg2rad(el0)

# plot initial arm
b, j, e = fk_3d(yaw, sh, el)
(line,) = ax.plot([b[0], j[0], e[0]],
                  [b[1], j[1], e[1]],
                  [b[2], j[2], e[2]],
                  marker='o', linewidth=3)
txt = ax.text2D(0.02, 0.98, "", transform=ax.transAxes, va="top")

# sliders
ax_yaw = plt.axes([0.15, 0.06, 0.7, 0.02])
ax_sh  = plt.axes([0.15, 0.03, 0.7, 0.02])
ax_el  = plt.axes([0.15, 0.00, 0.7, 0.02])

s_yaw = Slider(ax_yaw, 'yaw (°)', -180, 180, valinit=yaw0)
s_sh  = Slider(ax_sh,  'shoulder (°)', -179, 179, valinit=sh0)
s_el  = Slider(ax_el,  'elbow (°)',   -179, 179, valinit=el0)

def update(_):
    q0 = np.deg2rad(s_yaw.val)
    q1 = np.deg2rad(s_sh.val)
    q2 = np.deg2rad(s_el.val)
    b, j, e = fk_3d(q0, q1, q2)
    line.set_data_3d([b[0], j[0], e[0]],
                     [b[1], j[1], e[1]],
                     [b[2], j[2], e[2]])
    txt.set_text(f"EE: x={e[0]:.3f}, y={e[1]:.3f}, z={e[2]:.3f}\n"
                 f"yaw={s_yaw.val:.1f}°, sh={s_sh.val:.1f}°, el={s_el.val:.1f}°")
    fig.canvas.draw_idle()

for s in (s_yaw, s_sh, s_el):
    s.on_changed(update)
update(None)
plt.show()
