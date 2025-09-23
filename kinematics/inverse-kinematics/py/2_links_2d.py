# two_link_click_ik.py
import numpy as np
import matplotlib.pyplot as plt

# ----- link lengths (units) -----
L1 = 1.5
L2 = 1.0
R  = L1 + L2

def ik_2r(x, y, L1=L1, L2=L2):
    """Return list of (theta1, theta2) in radians for target (x,y)."""
    r2 = x*x + y*y
    # reachability check
    if r2 > (L1 + L2)**2 + 1e-9 or r2 < (L1 - L2)**2 - 1e-9:
        return []
    c2 = (r2 - L1*L1 - L2*L2) / (2.0 * L1 * L2)
    c2 = np.clip(c2, -1.0, 1.0)
    s2_pos = np.sqrt(1.0 - c2*c2)         # elbow-down
    s2_neg = -s2_pos                      # elbow-up
    t2a = np.arctan2(s2_pos, c2)
    t2b = np.arctan2(s2_neg, c2)
    # theta1 via atan2 trick
    def t1_for(t2):
        k1 = L1 + L2*np.cos(t2)
        k2 = L2*np.sin(t2)
        return np.arctan2(y, x) - np.arctan2(k2, k1)
    return [(t1_for(t2a), t2a), (t1_for(t2b), t2b)]

def fk_2r(t1, t2, L1=L1, L2=L2):
    x1 = L1*np.cos(t1); y1 = L1*np.sin(t1)
    x2 = x1 + L2*np.cos(t1 + t2)
    y2 = y1 + L2*np.sin(t1 + t2)
    return (0,0), (x1,y1), (x2,y2)

# figure
fig, ax = plt.subplots(figsize=(7,7))
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-R-0.2, R+0.2); ax.set_ylim(-R-0.2, R+0.2)
ax.grid(True, linestyle="--", linewidth=0.5)
ax.set_title("2-Link IK (click anywhere)")

# draw reach circle limits (optional)
circ = plt.Circle((0,0), R, color="0.85", fill=False, linestyle=":")
ax.add_patch(circ)
inner = plt.Circle((0,0), abs(L1-L2), color="0.85", fill=False, linestyle=":" )
ax.add_patch(inner)

# artists for two solutions
(line_a,) = ax.plot([], [], marker="o", linewidth=4, label="elbow-down")
(line_b,) = ax.plot([], [], marker="o", linewidth=4, label="elbow-up")
target_dot, = ax.plot([], [], "rx", markersize=10, mew=2)
txt = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top",
              bbox=dict(boxstyle="round", fc="w", ec="0.7"))
ax.legend(loc="lower right")

def on_click(event):
    if not event.inaxes: 
        return
    x, y = event.xdata, event.ydata
    target_dot.set_data([x], [y])
    sols = ik_2r(x, y)
    if not sols:
        line_a.set_data([], []); line_b.set_data([], [])
        txt.set_text(f"Target: ({x:.3f}, {y:.3f})\nUnreachable.")
        fig.canvas.draw_idle()
        return
    (t1a,t2a), (t1b,t2b) = sols
    # FK for both
    b, j, e = fk_2r(t1a, t2a); line_a.set_data([b[0], j[0], e[0]], [b[1], j[1], e[1]])
    b, j, e = fk_2r(t1b, t2b); line_b.set_data([b[0], j[0], e[0]], [b[1], j[1], e[1]])
    txt.set_text(
        f"Target: ({x:.3f}, {y:.3f})\n"
        f"Elbow-down: θ1={np.degrees(t1a):.1f}°, θ2={np.degrees(t2a):.1f}°\n"
        f"Elbow-up  : θ1={np.degrees(t1b):.1f}°, θ2={np.degrees(t2b):.1f}°"
    )
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("button_press_event", on_click)
plt.show()
