import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
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
    
    # Launch Gazebo with the world using ros_gz_sim launch file
    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r -v2 {world_file}', 'on_exit_shutdown': 'true'}.items()
    )
    
    # Spawn TurtleBot3 at entrance
    spawn_turtlebot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch', 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': '3.5',
            'y_pose': '-2.5',
            'z_pose': '0.0'
        }.items()
    )
    
    return LaunchDescription([
        gz_resource_path,
        gazebo,
        spawn_turtlebot,
    ])