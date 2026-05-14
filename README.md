# Autonomous Material Handling Robot

A fully autonomous indoor navigation robot built on ROS2 Jazzy with SLAM-based mapping, Nav2 navigation, real-time obstacle avoidance, and ArUco marker-based task assignment.

## What it does
- Builds a 2D map of its environment using LiDAR and SLAM
- Localizes itself on the saved map using AMCL
- Navigates autonomously to pre-assigned drop zones
- Detects ArUco markers via camera to automatically assign destinations
- Avoids dynamic obstacles in real time using Nav2 costmaps

## System Requirements
- Ubuntu 24.04 (WSL2 or native)
- ROS2 Jazzy Jalisco
- Python 3.10+
- opencv-contrib-python

## Install dependencies
```bash
sudo apt install ros-jazzy-desktop ros-jazzy-ros-gz -y
sudo apt install ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-simulations -y
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup -y
sudo apt install ros-jazzy-slam-toolbox ros-jazzy-topic-tools -y
pip3 install opencv-contrib-python pillow
```

## Clone this repo
```bash
git clone --recurse-submodules https://github.com/Shikhar-2005/autonomous-material-handling-robot.git
```

## Demo Mode 1 — Manual navigation
Launch Gazebo, Nav2, and topic relay. Set 2D Pose Estimate in RViz. Click Nav2 Goal.

## Demo Mode 2 — Operator A/B assignment
```bash
source /opt/ros/jazzy/setup.bash && python3 navigate_to_goal.py
```
Type 1 for Zone A (2.52, 2.35) or 2 for Zone B (2.49, -1.34).

## Demo Mode 3 — ArUco vision trigger
```bash
python3 aruco_detect.py
```
Show ArUco marker ID 1 or 2 from https://chev.me/arucogen (4x4_50 dictionary) to camera. Robot navigates automatically.

## Update camera IP
```bash
sed -i 's/YOUR_PHONE_IP/192.168.X.X/g' aruco_detect.py
```

## Hardware (for physical deployment)
- TurtleBot3 Waffle chassis
- Raspberry Pi 4 (2GB)
- RPLIDAR A1
- L298N motor driver
- 3S LiPo battery

## Credits
See CREDITS.md for all external packages and licenses.
