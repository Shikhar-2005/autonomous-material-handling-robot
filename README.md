# Autonomous Material Handling Robot
 
A fully autonomous indoor navigation robot built on **ROS2 Jazzy**, using **LiDAR-based SLAM** for environment mapping, **Nav2** for path planning and obstacle avoidance, **AMCL** for localization, and a **computer vision pipeline** for ArUco marker-based task assignment.
 
This project was developed as a Major Engineering Project and demonstrates a complete end-to-end autonomous material handling system — from environment mapping to vision-triggered delivery.
 
---
 
## Demo
 
### System Flow
```
Conveyor → ArUco marker detected by camera → Robot receives zone assignment
→ Nav2 plans collision-free path → Robot navigates autonomously
→ Dynamic obstacles avoided in real time → Goal reached
```
 
### Demo Modes
| Mode | How it works |
|---|---|
| Manual Nav2 Goal | Click target on RViz map — robot navigates there |
| Operator A/B | Press 1 or 2 in terminal — robot goes to pre-assigned zone |
| ArUco Vision | Show marker ID 1 or 2 to camera — robot navigates automatically |
 
---
 
## What Was Built and Configured
 
This project is not a simple install-and-run. The following was designed, configured, debugged and integrated from scratch:
 
### 1. ROS2 Environment Setup
- Configured ROS2 Jazzy Jalisco on Ubuntu 24.04 (WSL2)
- Resolved distribution incompatibility — ROS2 Humble does not support Ubuntu 24.04, requiring migration to Jazzy
- Configured Gazebo Harmonic bridge (`ros-gz`) after identifying that the classic `gazebo-ros-pkgs` package was deprecated in Jazzy
- Set up all environment variables, sourcing, and persistent shell configuration
### 2. LiDAR Integration
- Integrated RPLIDAR A1 sensor into the ROS2 data pipeline
- Validated `/scan` topic publishing at 10Hz with correct coordinate frame transforms
- Verified TF tree: `base_scan → base_link → odom → map`
### 3. SLAM Mapping
- Configured `slam_toolbox` for online asynchronous mapping
- Executed multiple mapping sessions with manual teleop, iterating on driving patterns to eliminate ghost artifacts
- Built and saved a clean 2D occupancy grid map (`my_map_v3`) of the environment
- Wrote a PIL-based map cleaning script (`clean_map.py`) to remove SLAM uncertainty pixels
### 4. Nav2 Navigation Stack Configuration
- Configured global and local costmaps with appropriate inflation radii
- Configured AMCL particle filter for localization on the saved map
- Diagnosed and resolved a critical `cmd_vel` topic routing issue specific to ROS2 Jazzy:
  - Nav2 controller published to `/cmd_vel_nav`
  - Robot bridge listened on `/cmd_vel`
  - Collision monitor in the pipeline was blocking the command chain
  - Fixed by deploying a `topic_tools relay` node to bridge the topics
- This issue is undocumented in official TurtleBot3 or Nav2 documentation
### 5. Task Assignment System
- Defined two drop zone coordinates on the saved map using RViz Publish Point tool
- Wrote `navigate_to_goal.py` — a ROS2 Python node that sends `NavigateToPose` action goals to Nav2 based on operator input
### 6. Computer Vision Pipeline
- Integrated OpenCV ArUco detection using the 4x4_50 dictionary
- Implemented a networked camera architecture — phone running IP Webcam streams MJPEG over WiFi, OpenCV reads the feed
- This architecture intentionally separates the vision unit from the robot compute unit, matching real-world deployments where a dedicated camera node sits at the pickup station
- Wrote `aruco_detect.py` — detects marker ID 1 or 2 and automatically triggers navigation
---
 
## System Architecture
 
```
VISION UNIT (Phone + IP Webcam app)
    Phone camera → MJPEG stream over WiFi (http://IP:8080/video)
    ↓
aruco_detect.py → OpenCV detects ArUco marker ID
    ↓
navigate_to_goal.py → Nav2 NavigateToPose action goal
    ↓
Nav2 stack → path planning → DWB controller → /cmd_vel_nav
    ↓
topic_tools relay → /cmd_vel → Gazebo robot bridge → motors
    ↓
AMCL localizes robot on saved map (my_map_v3)
    ↓
Real-time obstacle avoidance via local costmap
```
 
---
 
## Drop Zones
 
Coordinates obtained by hovering over the map in RViz with Publish Point tool:
 
| Zone | X | Y | Location |
|---|---|---|---|
| Zone A (Position 1) | 2.52 | 2.35 | Top area of arena |
| Zone B (Position 2) | 2.49 | -1.34 | Bottom area of arena |
 
---
 
## Repository Structure
 
```
autonomous-material-handling-robot/
│
├── navigate_to_goal.py     # ROS2 node — A/B zone navigation
├── aruco_detect.py         # OpenCV ArUco detection + navigation trigger
├── clean_map.py            # PIL script — removes SLAM uncertainty pixels
│
├── maps/
│   ├── my_map_v3.yaml      # Saved occupancy grid map metadata
│   └── my_map_v3.pgm       # Saved occupancy grid map image
│
├── config/
│   ├── nav2_params.yaml    # Nav2 stack configuration
│   └── slam_params.yaml    # SLAM toolbox configuration
│
└── CREDITS.md              # All external packages and licenses
```
 
---
 
## Requirements
 
- Ubuntu 22.04 or 24.04 (WSL2 or native)
- ROS2 Jazzy Jalisco
- Python 3.10+
---
 
## Installation
 
```bash
# ROS2 Jazzy
sudo apt install ros-jazzy-desktop -y
sudo apt install ros-jazzy-ros-gz -y
sudo apt install ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-simulations -y
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup -y
sudo apt install ros-jazzy-slam-toolbox ros-jazzy-topic-tools -y
 
# Python dependencies
pip3 install opencv-contrib-python pillow
 
# Environment
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
source ~/.bashrc
```
 
---
 
## Running the System
 
### Step 1 — Launch Gazebo
```bash
source /opt/ros/jazzy/setup.bash && export TURTLEBOT3_MODEL=waffle && \
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```
 
### Step 2 — Launch Navigation2
```bash
source /opt/ros/jazzy/setup.bash && export TURTLEBOT3_MODEL=waffle && \
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
use_sim_time:=True map:=/path/to/maps/my_map_v3.yaml
```
 
### Step 3 — Launch Topic Relay (critical)
```bash
source /opt/ros/jazzy/setup.bash && \
ros2 run topic_tools relay /cmd_vel_nav /cmd_vel
```
 
### Step 4 — Set initial pose in RViz
- Click **2D Pose Estimate** in RViz toolbar
- Click on robot's position on the map
- Drag in the direction the robot faces
- Wait for green AMCL particle cloud
---
 
## Demo Mode 1 — Manual Navigation
Click **Nav2 Goal** in RViz → click any white area on map → robot navigates there autonomously.
 
---
 
## Demo Mode 2 — Operator A/B Assignment
```bash
source /opt/ros/jazzy/setup.bash && python3 navigate_to_goal.py
```
Type `1` → robot navigates to Zone A. Type `2` → robot navigates to Zone B.
 
---
 
## Demo Mode 3 — ArUco Vision Trigger
 
**Update camera IP first:**
```bash
sed -i 's/YOUR_PHONE_IP/192.168.X.X/g' aruco_detect.py
```
 
**Run:**
```bash
python3 aruco_detect.py
```
 
Show ArUco marker ID 1 or 2 from [https://chev.me/arucogen](https://chev.me/arucogen) (dictionary: 4x4_50) to the camera. Robot navigates automatically to the corresponding zone.
 
---
 
## Key Technical Challenges Solved
 
| Challenge | Solution |
|---|---|
| ROS2 Humble incompatible with Ubuntu 24.04 | Migrated to ROS2 Jazzy Jalisco |
| Gazebo Classic deprecated in Jazzy | Used `ros-jazzy-ros-gz` (Gazebo Harmonic bridge) |
| Nav2 not sending velocity commands to robot | Diagnosed broken `cmd_vel` pipeline, deployed `topic_tools relay` |
| WSL2 cannot access USB webcam | Used IP Webcam app on phone streaming MJPEG over WiFi |
| Ghost artifacts in SLAM map | Drive away from spawn point before mapping; wrote map cleaning script |
| AMCL not converging | Correct 2D Pose Estimate with accurate orientation drag direction |
 
---
 
## Hardware (Physical Deployment)
 
| Component | Specification | Cost (INR) |
|---|---|---|
| Chassis | 2WD kit with BO motors | ₹800 |
| Motor Driver | L298N | ₹150 |
| Compute | Raspberry Pi 4 (2GB) | ₹4,500 |
| LiDAR | RPLIDAR A1 — 12m, 360° | ₹8,000 |
| Battery | 3S LiPo 2200mAh | ₹800 |
| Misc | Wires, mounts, SD card | ₹800 |
| **Total** | | **~₹15,050** |
 
---
 
## Future Scope
 
- Multi-robot swarm operation using ROS2 namespaces
- Robotic arm at drop station for automated sorting
- Replace phone camera with dedicated Raspberry Pi camera node
- Web dashboard for fleet management and task assignment
- Auto return-to-dock with battery monitoring
---
 
## Dependencies
 
| Package | Author | License | Purpose |
|---|---|---|---|
| [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) | Steve Macenski | LGPL-2.1 | SLAM mapping and localization |
| [Nav2](https://github.com/ros-planning/navigation2) | Nav2 Contributors | Apache-2.0 | Path planning, AMCL, obstacle avoidance |
| [TurtleBot3](https://github.com/ROBOTIS-GIT/turtlebot3) | ROBOTIS | Apache-2.0 | Robot platform and simulation |
| [OpenCV](https://github.com/opencv/opencv) | OpenCV Contributors | Apache-2.0 | ArUco marker detection |
| [ROS2 Jazzy](https://github.com/ros2) | Open Robotics | Apache-2.0 | Robot middleware framework |
 
See [CREDITS.md](CREDITS.md) for full details.
 
---
 
## Author
 
Shikhar Srivastava 
