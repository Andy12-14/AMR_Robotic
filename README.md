# Autonomous Exploration and Mapping with ROS 2

A complete simulation pipeline demonstrating a custom differential drive robot capable of autonomous navigation, reactive obstacle avoidance, and real-time environment mapping (SLAM) using ROS 2 and Gazebo Harmonic.

## Features

- **Custom URDF:** A differential drive robot equipped with a 360° LiDAR and a front-facing camera.
- **Autonomous Navigation:** Custom Python node utilizing laser scan data to dynamically filter noise (NaN/Inf) and avoid obstacles in real-time.
- **SLAM Integration:** Real-time 2D occupancy grid generation using `slam_toolbox`.
- **High-Fidelity Simulation:** Built for Gazebo Harmonic with `ros_gz` bridges.

## Installation Guide (Windows / WSL)

This project is built to run on **Ubuntu 24.04** using **ROS 2 Jazzy**. If you are on Windows, use **Windows Subsystem for Linux (WSL)**.

### Step 1: Install WSL and Ubuntu 24.04

Open Windows PowerShell as Administrator and run:

```powershell
wsl --install -d Ubuntu-24.04
```

Restart your computer if prompted. After rebooting, open the **Ubuntu 24.04** app and create your UNIX username and password.

### Step 2: Install ROS 2 Jazzy

Inside your Ubuntu terminal, install ROS 2 Jazzy:

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" > /etc/apt/sources.list.d/ros2.list'

sudo apt update
sudo apt install ros-jazzy-desktop ros-jazzy-ros-gz
```

### Step 3: Set Up the Workspace

Create a standard ROS 2 workspace and clone the repository into the `src` directory.

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

git clone https://github.com/Andy12-14/AMR_Robotic.git

cd ~/ros2_ws
sudo rosdep init
rosdep update
rosdep install --from-paths src -y --ignore-src
colcon build --symlink-install
```

> Pro Tip: Add `source ~/ros2_ws/install/setup.bash` to your `~/.bashrc` so you do not need to source it in every new terminal.

## How to Run the Project

Open three separate terminal windows. In each terminal, source the workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

### 1. Launch the Simulation (Gazebo)

Spawn the custom differential drive robot inside the simulated maze environment:

```bash
ros2 launch diff_robot sim_launch.py
```

> If your launch file is named differently, replace `sim_launch.py` with the correct file name.

### 2. Start SLAM and RViz

In a second terminal, launch the SLAM toolbox and RViz:

```bash
ros2 launch diff_robot slam_launch.py
```

### 3. Run Obstacle Avoidance

In a third terminal, start the custom Python node:

```bash
ros2 run diff_robot obstacle_avoidance
```

The robot will begin moving autonomously, using its LiDAR data to avoid obstacles and explore the maze.

## Visualizing the Robot's Sensors

### Viewing the SLAM Map (RViz)

If RViz does not open automatically, start it manually:

```bash
rviz2
```

- Click **Add** -> select **Map** -> click **OK**.
- Under the Map dropdown, set **Topic** to `/map`.
- Set the **Fixed Frame** to `map` or `odom`.

You will see the occupancy grid update in real-time.

### Viewing the Camera Feed (RQT)

To view the live RGB video feed from the front-facing camera:

```bash
ros2 run rqt_image_view rqt_image_view
```

Then select the camera topic (typically `/camera/image_raw`) from the dropdown menu.

## How the Code Works

The core logic resides in the `obstacle_avoidance` Python node:

- **Sense:** Subscribes to the `/scan` topic to receive 360-degree LiDAR data.
- **Filter:** Uses the front 80 degrees of laser data and filters out `NaN` and `Inf` anomalies caused by sensor noise.
- **Act:** Monitors a 0.8-meter safety threshold. If an object enters that zone, the node overrides the forward command and executes a rotation escape maneuver.

## Contributing

Feel free to fork this project, submit pull requests, or use it as a base for your own ROS 2 robotics projects.

Future goals include:

- Implementing the Nav2 stack for directed pathfinding.
- Utilizing the onboard camera for object recognition.

Created for autonomous robotics demonstration and educational purposes.
