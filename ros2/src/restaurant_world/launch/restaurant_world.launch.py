import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Ensure TB3 model is set (defaults to burger if not provided)
    tb3_model_env = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value=os.environ.get('TURTLEBOT3_MODEL', 'burger')
    )
    # Package dirs
    pkg_rest_world = get_package_share_directory('restaurant_world')
    world_file = os.path.join(pkg_rest_world, 'worlds', 'restaurant.world')

    # Resource paths: restaurant models + TB3 Gazebo models
    models_path = os.path.join(pkg_rest_world, 'models')
    tb3_models_path = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'models')
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path + ':' + tb3_models_path + ':' + os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    )

    # Gazebo (GUI) with world
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r -v2 {world_file}',
            'on_exit_shutdown': 'true'
        }.items()
    )

    # Spawn TurtleBot3 via official spawner (includes bridges)
    tb3_spawn = IncludeLaunchDescription(
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
        tb3_model_env,
        gz_resource_path,
        gazebo,
        tb3_spawn,
    ])