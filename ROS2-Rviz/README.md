# Mobile Robot URDF Visualization with RViz2

This repository contains a simple **URDF model** of a mobile robot (with a base, lidar, left/right wheels, and caster wheel) and instructions for visualizing it in **RViz2** using ROS 2 Humble.

---

## 📦 Prerequisites

- **ROS 2 Humble** installed on your system  
- `urdf_tutorial` package:

```bash
sudo apt update
sudo apt install ros-humble-urdf-tutorial
```

---

## 📂 File Structure

```
mobile-robot-pkg/
└── urdf/
    └── my_robot.urdf
```

---

## 🚀 Launch Instructions

1. **Source your ROS 2 setup:**
    ```bash
    source /opt/ros/humble/setup.bash
    ```

2. **Launch the URDF in RViz2 using the urdf_tutorial package:**
    ```bash
    ros2 launch urdf_tutorial display.launch.py model:=<absolute_path_to_my_robot.urdf>
    ```
    Replace `<absolute_path_to_my_robot.urdf>` with the full path to your URDF file.

---

## 🖥️ Visualizing in RViz2

- RViz2 will start automatically when you launch.
- In the Displays panel:
    - Add a **RobotModel** display.
    - Set the **Description Source** to `Topic`.
    - Ensure the **Topic** is `/robot_description`.
    - Set the **Fixed Frame** to `base_link` or `base_footprint` to see the robot properly.

You should now see your robot model rendered in RViz 🎉

---

## 🤖 Robot Description

The robot consists of:
- **Base link:** Green box (0.6 × 0.4 × 0.2 m)
- **Lidar sensor:** White cylinder on top of the base
- **Left & Right wheels:** Grey cylinders (continuous joints)
- **Caster wheel:** Grey sphere at the front (fixed joint)

This minimal model is useful for learning ROS 2, URDF, and robot visualization.

---

## 📌 Next Steps

- Create your own `display.launch.py` file inside this package.
- Use `robot_state_publisher` and `joint_state_publisher_gui` nodes directly.
- Add sensors, arms, or mobility plugins for Gazebo simulation.
