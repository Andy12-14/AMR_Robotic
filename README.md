Autonomous Exploration and Mapping with ROS 2

A complete simulation pipeline demonstrating a custom differential drive robot capable of autonomous navigation, reactive obstacle avoidance, and real-time environment mapping (SLAM) using ROS 2 and Gazebo Harmonic.



Features

Custom URDF: A differential drive robot equipped with a 360° LiDAR and a front-facing camera.

Autonomous Navigation: Custom Python node utilizing laser scan data to dynamically filter noise (NaN/Inf) and avoid obstacles in real-time.

SLAM Integration: Real-time 2D occupancy grid generation using the slam_toolbox.

High-Fidelity Simulation: Built for Gazebo Harmonic with ros_gz bridges.

Installation Guide (Windows / WSL)

This project is built to run on Ubuntu 24.04 using ROS 2 Jazzy. If you are on Windows, you will need to set up Windows Subsystem for Linux (WSL).

Step 1: Install WSL and Ubuntu 24.04

Open your Windows PowerShell as Administrator and run:

wsl --install -d Ubuntu-24.04



Restart your computer if prompted. Once rebooted, open the "Ubuntu 24.04" app from your Windows Start menu and create your UNIX username and password.

Step 2: Install ROS 2 Jazzy

Inside your Ubuntu terminal, install ROS 2 Jazzy by following the official setup:

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL [https://raw.githubusercontent.com/ros/rosdistro/master/ros.key](https://raw.githubusercontent.com/ros/rosdistro/master/ros.key) -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] [http://packages.ros.org/ros2/ubuntu](http://packages.ros.org/ros2/ubuntu) $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install ros-jazzy-desktop ros-jazzy-ros-gz



Step 3: Set Up the Workspace

We will create a standard ROS 2 workspace and clone the repository into the src directory.

# 1. Source your ROS 2 installation
source /opt/ros/jazzy/setup.bash

# 2. Create the workspace and src folder
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 3. Clone this repository
git clone [https://github.com/Andy12-14/AMR_Robotic.git](https://github.com/Andy12-14/AMR_Robotic.git)

# 4. Navigate back to the workspace root
cd ~/ros2_ws

# 5. Install any missing dependencies using rosdep
sudo rosdep init
rosdep update
rosdep install --from-paths src -y --ignore-src

# 6. Build the workspace using colcon
colcon build --symlink-install



Pro Tip: Add source ~/ros2_ws/install/setup.bash to your ~/.bashrc file so you don't have to source it every time you open a new terminal.

How to Run the Project

You will need to open three separate terminal windows. Make sure to source your workspace in every new terminal:
source ~/ros2_ws/install/setup.bash

1. Launch the Simulation (Gazebo)

First, spawn the custom differential drive robot inside the simulated maze environment.

ros2 launch diff_robot sim_launch.py



(Note: If your launch file is named differently, replace sim_launch.py with the correct name).

2. Start SLAM and RViz

In a second terminal, launch the SLAM toolbox and RViz to begin the mapping process.

ros2 launch diff_robot slam_launch.py



3. Unleash the "Brain" (Obstacle Avoidance)

In a third terminal, run the custom Python node. The robot will start moving, using its LiDAR to evade walls and dynamically explore the maze.

ros2 run diff_robot obstacle_avoidance



Visualizing the Robot's Sensors

Once the robot is running autonomously, you can view what it sees in real-time.

Viewing the SLAM Map (RViz)

If RViz does not open automatically with your SLAM launch file, you can start it manually and add the map:

Open a new terminal and run: rviz2

In the bottom left, click Add -> select Map -> click OK.

In the left panel under the new Map dropdown, find Topic and change it to /map.

Ensure your Fixed Frame (at the top left) is set to map or odom. You will see the black, white, and grey occupancy grid drawing in real-time!

Viewing the Camera Feed (RQT)

To see the live RGB video feed from the front-facing camera, we use the standard ROS 2 image viewer:

Open a new terminal and source your ROS 2 installation.

Run the image view tool:

ros2 run rqt_image_view rqt_image_view



A window will pop up. In the dropdown menu at the top left, select the camera topic (typically /camera/image_raw). You will now see the live video stream from Gazebo!

How the Code Works

The core logic lies in the obstacle_avoidance Python node:

Sense: Subscribes to the /scan topic to receive 360-degree LiDAR data.

Filter: Slices the front 80 degrees for "tunnel vision" and mathematically filters out NaN and Inf anomalies caused by sensor scattering.

Act: Continuously monitors a 0.8-meter safety threshold. If an object breaches this zone, it overrides the forward command (1.2 m/s) with a sharp rotational escape velocity.

Contributing

Feel free to fork this project, submit pull requests, or use it as a base for your own ROS 2 robotics projects! Future goals include implementing the Nav2 stack for directed pathfinding and utilizing the onboard camera for object recognition.

Created for autonomous robotics demonstration and educational purposes.