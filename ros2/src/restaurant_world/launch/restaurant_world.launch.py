from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    world = os.path.join(
        get_package_share_directory('restaurant_world'), 'worlds', 'restaurant.world')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')),
        launch_arguments={'world': world}.items()
    )

    spawner = Node(
        package='gazebo_ros', executable='spawn_entity.py', output='screen',
        arguments=['-entity', 'turtlebot3',
                   '-database', 'turtlebot3_burger',
                   '-x', '0.0', '-y', '-2.0', '-z', '0.01', '-Y', '0.0']
    )

    return LaunchDescription([gazebo, spawner])
