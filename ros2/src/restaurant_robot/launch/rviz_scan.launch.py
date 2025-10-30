"""
DEPRECATED: Use restaurant_robot/launch/rviz_slam.launch.py instead.

This file remains in the source tree only for historical reference and will not
be installed or supported. Running this launch is intentionally disabled to
prevent duplicate configurations.
"""

def generate_launch_description():
    raise RuntimeError(
        'DEPRECATED launch: use restaurant_robot/launch/rviz_slam.launch.py '
        'with config/slam_mapping.rviz'
    )
