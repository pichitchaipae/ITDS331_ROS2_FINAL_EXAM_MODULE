# Copilot Induction: ITDS331 ROS2 Final Exam Module

## Project Overview
This is a ROS 2 final exam project (ITDS331) implementing a restaurant service robot simulation using TurtleBot3. The project consists of three main missions:

1. **SLAM Map Creation**: Manual exploration and mapping of restaurant environment
2. **Autonomous Navigation**: Testing navigation stack with saved maps
3. **Automated Service System**: ROS2 action-based food delivery simulation

The project simulates a restaurant environment in Gazebo with TurtleBot3 robot for autonomous navigation tasks including exploration, SLAM (Simultaneous Localization and Mapping), teleoperation, and automated service operations.

## ⚠️ Common Pitfalls & Critical Warnings

### 🚫 DO NOT Use turtlebot3_world.launch.py
**CRITICAL**: Never run `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py` - this loads the **default TurtleBot3 world**, not our custom restaurant world!

**✅ CORRECT Command:**
```bash
ros2 launch restaurant_world restaurant_world.launch.py
```

**❌ WRONG Command (loads wrong world):**
```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

### 🔍 Debugging World Loading Issues
If you see the wrong world loading:
1. Check that you're using `restaurant_world.launch.py`, not `turtlebot3_world.launch.py`
2. Verify the package name is `restaurant_world`, not `turtlebot3_gazebo`
3. Ensure proper sourcing: `source install/setup.bash`

### 🐛 TurtleBot Spawn Issues
- TurtleBot spawns at door: `(3.5, -2.5, 0)` - this is correct
- If TurtleBot disappears: Check for collision with zone markers
- Kitchen divider must be `<static>true</static>` (cannot move)

## Mission Requirements

This project implements three main missions for the ITDS331 ROS2 Final Exam:

### Mission 1: Map Creation (SLAM)
**Objective**: Create a complete and accurate map of the restaurant environment using SLAM.

**Steps**:
1. Launch Gazebo simulator with the restaurant world environment
2. Launch TurtleBot3 robot and SLAM system (SLAM Toolbox)
3. Use teleoperation (keyboard or joystick) to manually drive the robot and explore the entire restaurant area
4. Save the completed map as .yaml and .pgm files

**Evaluation Criteria**:
- **Map Completeness**: Map covers all areas including kitchen zone and all customer tables
- **Accuracy**: Walls and obstacles in the map match the simulation environment with minimal distortion
- **Process**: Successfully save the map files correctly

### Mission 2: Autonomous Navigation
**Objective**: Test autonomous navigation using the saved map from Mission 1.

**Steps**:
1. Close SLAM nodes and launch Navigation system (Nav2) using the saved map
2. Set the robot's initial pose correctly in RViz2
3. Test navigation goals in sequence:
   - From start position to Table 1
   - From Table 1 to Kitchen zone
   - From Kitchen zone to Table 3
4. Observe robot movement to ensure obstacle avoidance

**Evaluation Criteria**:
- **System Setup**: Successfully launch Navigation system and set initial pose
- **Movement**: Robot reaches all 3 designated goal points successfully
- **Obstacle Avoidance**: Robot plans safe paths avoiding known obstacles in the map and any new obstacles

### Mission 3: Automated Restaurant Service Simulation
**Objective**: Create a ROS2 node that simulates automated food service operations.

**Requirements**:
- Create an Action Server that receives "orders" containing table_id
- When an order is received, the robot performs these steps:
  1. Navigate to Kitchen zone to "pick up food" (simulate with 5-second wait)
  2. Navigate to the customer's table (specified by table_id)
  3. Display message: "Food served at table [table_id] successfully"
- Provide continuous feedback during operation (e.g., "Heading to kitchen", "Delivering food to table X")
- Return result indicating mission success/failure
- Additional creative implementations are encouraged

**Technical Implementation**:
- ROS2 Node in Python or C++
- Action Server for order processing
- Integration with Navigation stack for autonomous movement
- Feedback and result communication

**Expected Files** (in `restaurant_robot` package):
- `action/RestaurantService.action` - Action definition
- `src/restaurant_service_server.py` - Action server implementation
- `launch/restaurant_service.launch.py` - Launch file for the service
- Integration with existing navigation launch files

## Technology Stack

### Operating System
- **Ubuntu 24.04 LTS (Noble Numbat)** - The base operating system for development and deployment

### ROS 2 Distribution
- **ROS 2 Jazzy Jalisco** - The primary ROS 2 distribution used for this project
- Installed from official ROS 2 Debian packages under `/opt/ros/jazzy`

### Simulation Framework
- **Gazebo (gz-sim 8)** - Modern Gazebo simulation engine for robotics simulation
- Integrated with ROS 2 via `ros_gz_sim` bridge package
- Uses SDF (Simulation Description Format) for world and model definitions

### Build System
- **colcon** - ROS 2's build system for compiling and installing packages
- Uses `--symlink-install` for development workflow

### Robot Platform
- **TurtleBot3** - Differential drive robot platform
- Models: Burger (primary), Waffle, Waffle Pi
- Packages: `turtlebot3_simulations`, `turtlebot3_cartographer`, `turtlebot3_teleop`

## Project Structure

```
ITDS331_ROS2_FINAL_EXAM_MODULE/
├── README.md                    # Project documentation
├── .gitignore                  # Git ignore rules
├── ros2/                       # ROS 2 workspace subdirectory
│   ├── src/
│   │   ├── restaurant_robot/   # Custom robot control package
│   │   └── restaurant_world/   # Restaurant environment package
│   ├── build/                  # Build artifacts
│   ├── install/                # Installed packages
│   └── log/                    # Build logs
└── build/                      # Legacy build directory
```

## Key Packages

### restaurant_world
- Contains Gazebo world file (`worlds/restaurant.world`)
- Launch files for starting the simulation
- Models and maps for the restaurant environment
- Uses `ros_gz_sim` for ROS 2 integration

### restaurant_robot
- Custom robot control and navigation logic
- Integration with TurtleBot3 packages
- **Mission 3**: Contains the automated restaurant service Action Server
- Implements order processing, autonomous navigation between kitchen and tables
- Provides feedback and result communication for service operations

## Development Workflow

### Environment Setup
```bash
# Source ROS 2
source /opt/ros/jazzy/setup.bash

# Optional: Add to ~/.bashrc for automatic sourcing
echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc

# Build workspace
cd ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2
colcon build --symlink-install

# Source workspace overlay
source install/setup.bash
```

### 🔧 After Making Changes: Rebuild Workflow
**After editing world files, models, or code:**

1. **Kill any running Gazebo processes:**
   ```bash
   pkill -f "gz sim"
   ```

2. **Rebuild the workspace:**
   ```bash
   cd ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2
   colcon build --symlink-install
   ```

3. **Source the updated overlay:**
   ```bash
   source install/setup.bash
   ```

**Why this is necessary:**
- World/model changes require rebuilding to take effect
- Old Gazebo processes may cache previous versions
- Ensures you're running the latest project state

### 🚀 Complete Development Cycle: Fix → Rebuild → Test

**After making changes to world files, models, or code:**

1. **Kill running processes:**
   ```bash
   pkill -f "gz sim"
   ```

2. **Rebuild workspace:**
   ```bash
   cd ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2
   colcon build --symlink-install
   source install/setup.bash
   ```

3. **Test the changes:**
   ```bash
   ros2 launch restaurant_world restaurant_world.launch.py
   ```

**Quick verification commands:**
```bash
# Check if rebuild was successful
ls ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/restaurant_world/

# Verify world file is updated
head -5 ~/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/restaurant_world/share/restaurant_world/worlds/restaurant.world
```

### Mission Workflows

#### Mission 1: SLAM Map Creation
```bash
# Terminal 1: Launch restaurant world
ros2 launch restaurant_world restaurant_world.launch.py

# Terminal 2: Launch SLAM system
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True

# Terminal 3: Teleoperation for exploration
ros2 run turtlebot3_teleop teleop_keyboard

# After exploration: Save map
ros2 run nav2_map_server map_saver_cli -f ~/map_restaurant
```

**⚠️ IMPORTANT: DO NOT use turtlebot3_world.launch.py**
- ❌ `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py` - **WRONG!** This loads the default TurtleBot3 world
- ✅ `ros2 launch restaurant_world restaurant_world.launch.py` - **CORRECT!** This loads our custom restaurant world

**🐛 Common Issue**: Accidentally running `turtlebot3_world.launch.py` instead of `restaurant_world.launch.py` will load the wrong world and cause confusion.

#### Mission 2: Autonomous Navigation Testing
```bash
# Close SLAM nodes, then launch Navigation with saved map
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map_restaurant.yaml

# In RViz2: Set initial pose, then send navigation goals to:
# 1. Table 1, 2. Kitchen zone, 3. Table 3
```

#### Mission 3: Automated Service System
```bash
# Launch Navigation system
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map_restaurant.yaml

# Run the restaurant service node (to be implemented)
ros2 run restaurant_robot restaurant_service_server

# Test with action client (example)
ros2 action send_goal /restaurant_service restaurant_robot/action/RestaurantService "{table_id: 1}"
```

## Common Dependencies

### ROS 2 Packages
- `ros-jazzy-ros-dev` - ROS development tools
- `ros-jazzy-ros-gz-sim` - Gazebo-ROS 2 bridge
- `ros-jazzy-turtlebot3-*` - TurtleBot3 packages

### System Packages
- `python3-colcon-common-extensions` - Colcon build tool
- `libgz-sim8-dev` - Gazebo Sim development libraries

## Configuration Notes

### Gazebo Integration
- Uses `ros_gz_sim` instead of deprecated `gazebo_ros`
- World files use SDF format compatible with gz-sim8
- Robot spawning handled through ROS 2 services

### Build Configuration
- CMake minimum version 3.5
- C++ standard 14
- Python 3.8+ compatible

### Environment Variables
- `AMENT_PREFIX_PATH` - Contains installed package paths
- `COLCON_PREFIX_PATH` - Build system prefix paths
- `ROS_PACKAGE_PATH` - Source package search paths

## Troubleshooting

### Common Issues
1. **Package not found**: Ensure ROS 2 is sourced and workspace is built
2. **Gazebo model errors**: Check SDF syntax and model availability
3. **Build failures**: Verify all dependencies are installed

### Debug Commands
```bash
# Check ROS 2 packages
ros2 pkg list | grep restaurant

# Check environment
echo $AMENT_PREFIX_PATH

# Validate launch file
ros2 launch --show-args restaurant_world restaurant_world.launch.py
```

## Development Guidelines

### Code Style
- Follow ROS 2 C++ and Python style guidelines
- Use meaningful variable and function names
- Add documentation for complex logic

### Version Control
- Use descriptive commit messages
- Keep commits focused on single changes
- Update documentation with code changes

### Testing
- Test launch files in isolated terminals
- Verify simulation performance
- Check navigation stack integration

## Learning Resources

### ROS 2 Documentation
- [ROS 2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [Colcon Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html)

### Gazebo Documentation
- [Gazebo Platform](https://gazebosim.org/docs/all/getstarted/)
- [ROS-Gazebo Integration](https://gazebosim.org/api/sim/8/ros2_integration.html)

### TurtleBot3 Documentation
- [TurtleBot3 Manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
- [Simulation Guide](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/)

This induction file helps AI assistants understand the project context, technologies, and development practices. Update this file when adding new technologies or changing project structure.