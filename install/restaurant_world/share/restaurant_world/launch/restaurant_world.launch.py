import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package directory
    pkg_restaurant_world = get_package_share_directory('restaurant_world')
    
    # Path to world file
    world_file = os.path.join(pkg_restaurant_world, 'worlds', 'restaurant.world')
    
    # Path to models directory
    models_path = os.path.join(pkg_restaurant_world, 'models')
    
    # Path to TurtleBot3 models
    turtlebot3_models_path = get_package_share_directory('turtlebot3_gazebo') + '/models'
    
    # Set Gazebo resource path to include our models and TurtleBot3 models
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path + ':' + turtlebot3_models_path + ':' + os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    )
    
    # Launch Gazebo with the world
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-v2', world_file, '--force-version', '8'],
        output='screen',
    )
    
    # Spawn TurtleBot3 at entrance using local model
    urdf_path = os.path.join(pkg_restaurant_world, 'models', 'turtlebot3_burger', 'model.sdf')
    spawn_turtlebot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_turtlebot3_burger',
            '-file', urdf_path,
            '-x', '3.5',
            '-y', '-2.5',
            '-z', '0.0'
        ],
        output='screen',
    )
    
    # Fake TurtleBot3 node for simulation
    fake_turtlebot = Node(
        package='turtlebot3_fake_node',
        executable='turtlebot3_fake_node',
        name='turtlebot3_fake_node',
        output='screen',
        parameters=[
            {'use_sim_time': True},
            {'joint_states_frame': 'base_footprint'},
            {'odom_frame': 'odom'},
            {'base_frame': 'base_footprint'},
            {'wheels.separation': 0.160},
            {'wheels.radius': 0.033}
        ]
    )
        # Parameter bridge for TurtleBot topics
    bridge_params = os.path.join(pkg_restaurant_world, 'params', 'turtlebot3_burger_bridge.yaml')
    parameter_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen',
    )
    
    # Fake scan publisher since sensor not working in headless environment
    fake_scan_publisher = Node(
        executable='python3',
        arguments=['/home/jao/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/src/restaurant_robot/restaurant_robot/fake_scan_publisher.py'],
        output='screen',
    )
    
    return LaunchDescription([
        gz_resource_path,
        gazebo,
        spawn_turtlebot,
        parameter_bridge,
    ])