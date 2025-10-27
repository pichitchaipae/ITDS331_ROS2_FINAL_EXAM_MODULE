# ITDS331_ROS2_FINAL_EXAM_MODULE

Professional README — setup, build, run, and troubleshooting for the restaurant world ROS 2 workspace.

## Table of contents

- About
- Prerequisites
- Setup (source + dependencies)
- Build
- Run / Examples
- Saving maps
- Visualization
- Troubleshooting
- Contributing
- License

## About

This workspace contains packages and launch files used to run a Restaurant world in Gazebo with a TurtleBot3 robot for exploration, SLAM, teleoperation, and map saving.

Note: some original notes in this repository are in Thai; this README provides an English, professional reference.

This project uses ROS 2 Jazzy. See the Colcon tutorial for Jazzy here:
https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html

## Prerequisites

- Ubuntu (tested on Ubuntu with ROS 2 Jazzy installed)
- ROS 2 Jazzy installed under `/opt/ros/jazzy`
- colcon (colcon-common-extensions)
- TurtleBot3 packages (simulations, teleop, Gazebo worlds)

Useful links:

- ROS 2 installation (Deb packages) — Humble: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html
- Ubuntu Desktop download (recommended 24.04.3 LTS for ROS 2 compatibility): https://ubuntu.com/download/desktop

Install common ROS 2 developer meta-package (optional but recommended):

```bash
sudo apt update
sudo apt install ros-jazzy-ros-dev
```

Install colcon if you don't already have it:

```bash
sudo apt install python3-colcon-common-extensions
```

## Setup

Before you build or run anything, you must source your ROS 2 installation in every new terminal session:

```bash
source /opt/ros/jazzy/setup.bash
```

If you want this done automatically for each new shell, add the line above to your `~/.bashrc` (optional):

```bash
echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
```

Then, from the workspace root (`~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE`) build the workspace:

```bash
cd ros2
colcon build --symlink-install
```

After a successful build source the install overlay before running packages in the workspace:

```bash
source ros2/install/setup.bash
```

## Run / Examples

### 🚀 Mission 1: Restaurant SLAM Mapping

**⚠️ IMPORTANT:** Do NOT use `turtlebot3_world.launch.py` - it loads the wrong world!

#### Step 1: Launch Restaurant World
Open a new terminal and launch the restaurant environment:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch restaurant_world restaurant_world.launch.py
```

This will:
- Open Gazebo with the restaurant environment
- Spawn TurtleBot3 Burger at the entrance door
- Load all restaurant models (tables, chairs, kitchen equipment)

**⚠️ Troubleshooting:** If you see the wrong world loading, kill old Gazebo processes:
```bash
pkill -f "gz sim"
```

#### Step 2: Start SLAM Mapping System
Open a second terminal for the SLAM system:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```

This will:
- Start SLAM Toolbox for real-time mapping
- Process laser scans from TurtleBot3
- Build a map as you drive

#### Step 3: Control the Robot (Teleoperation)
Open a third terminal for keyboard control:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 run turtlebot3_teleop teleop_keyboard
```

**Keyboard Controls:**
```
   w
a  s  d
   x
```

- **w**: Move forward
- **a**: Turn left
- **d**: Turn right
- **s**: Move backward
- **x**: Stop

#### Complete Mission 1 Setup (All Terminals)
Open **three terminals** simultaneously and run these commands:

**Terminal 1: Restaurant World**
```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch restaurant_world restaurant_world.launch.py
```

**Terminal 2: SLAM Mapping**
```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```

**Terminal 3: Teleoperation**
```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 run turtlebot3_teleop teleop_keyboard
```
- **space**: Emergency stop

#### Step 4: Map the Restaurant
Use the keyboard controls to drive the TurtleBot3 around the restaurant:

1. **Start at Entrance** (robot spawns here)
2. **Explore Dining Area** - drive around all tables and chairs
3. **Enter Kitchen** - navigate through the service opening in the divider
4. **Map Kitchen Zone** - cover the stove and counter areas
5. **Complete Circuit** - return to the entrance

**Tips:**
- Drive slowly for accurate mapping
- Get close to walls and obstacles
- Cover all colored floor zones (entrance, dining, kitchen)
- The SLAM system builds the map automatically

### ❌ WRONG Commands (Do Not Use)
```bash
# WRONG - loads default TurtleBot3 world, not restaurant!
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# WRONG - old Cartographer method
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
```

## Saving maps

After exploring, open a new terminal, source both ROS 2 and the workspace install (if needed), then save the map:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
ros2 run nav2_map_server map_saver_cli -f ~/map_restaurant
# creates: ~/map_restaurant.yaml and ~/map_restaurant.pgm
```

## Visualization

Open RViz to inspect results (example for Cartographer):

```bash
ros2 launch turtlebot3_cartographer rviz.launch.py
```

## Troubleshooting

This is a very common ROS 2 error. It almost always means your ROS 2 environment is not sourced in the current terminal session.

The error `Could not find a package configuration file provided by "ament_cmake"` indicates that the build system (CMake) cannot find the core ROS 2 build tools.

### Fix: source ROS 2

Before you build, you must source your ROS 2 installation first:

```bash
source /opt/ros/jazzy/setup.bash
colcon build
```

Why this works:

- Sourcing the `setup.bash` file sets environment variables like `CMAKE_PREFIX_PATH` and `AMENT_PREFIX_PATH`, which tell `cmake` and `colcon` where to find ROS 2 packages and build tools.
- You must source the file in every new terminal before working with ROS 2.
- Installing additional packages (e.g., Gazebo or TurtleBot3) does not replace the need to source ROS 2.

### If it still fails

If sourcing doesn't fix the issue, ensure the core ROS 2 development packages are installed:

```bash
sudo apt install ros-jazzy-ros-dev
```

Then source and rebuild.

## Contributing

## Gazebo / ros_gz_sim (common simulation issues)

If you plan to run Gazebo (gz-sim) simulations or use `ros_gz_sim` (the ROS/Gazebo bridge), these links are useful:

- TurtleBot3 Gazebo simulation guide: https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation
- Gazebo (gz-sim) official install: https://gazebosim.org/api/sim/8/install.html

Gazebo Platform (get started): https://gazebosim.org/docs/all/getstarted/

Gazebo Versions / recommendation:

- Ubuntu 24.04 (Noble) users: on the Gazebo website select the "Gazebo Harmonic" release — this is recommended when using ROS 2 Jazzy.

Problem 1 (example CMake error):

	CMake Error at CMakeLists.txt:23 (find_package):
		By not providing "Findros_gz_sim.cmake" in CMAKE_MODULE_PATH this project
		has asked CMake to find a package configuration file provided by
		"ros_gz_sim", but CMake did not find one.

	Could not find a package configuration file provided by "ros_gz_sim" with
	any of the following names:

		ros_gz_simConfig.cmake
		ros_gz_sim-config.cmake

	Add the installation prefix of "ros_gz_sim" to CMAKE_PREFIX_PATH or set
	"ros_gz_sim_DIR" to a directory containing one of the above files.  If
	"ros_gz_sim" provides a separate development package or SDK, be sure it has
	been installed.

Solve 1 — quick install (Jazzy package names shown):

```bash
sudo apt-get update --fix-missing
sudo apt-get install ros-jazzy-ros-gz-sim
sudo apt-get install ros-jazzy-turtlebot3-*
```

Install Gazebo (gz-sim 8) — example repository and package install:

```bash
# Configure package repositories
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update

# Install Gazebo Sim development libraries
sudo apt-get install libgz-sim8-dev
```

Notes:

- Replace `jazzy` in package names with your ROS 2 distribution name if different (e.g., `humble` or `iron`).
- After installing, make sure you source your ROS 2 environment and the workspace overlay before building:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/setup.bash
colcon build
```

If problems persist, check that `ros_gz_sim` is installed and that `CMAKE_PREFIX_PATH` includes the install location (you can echo it to verify).


Contributions are welcome. Open an issue or submit a pull request with a clear description of changes. Keep commits small and focused.

## License

This repository does not specify a license. If you want to release it, consider adding an OSI-approved license such as MIT or Apache-2.0.

---

If you'd like, I can also:

- Commit the README change and push a branch to your repository.
- Add a short Thai translation for the user-facing quick-start.

Please tell me which follow-up you'd like.

