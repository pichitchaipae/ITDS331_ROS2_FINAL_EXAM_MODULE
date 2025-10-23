import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/jao/Desktop/ITDS331_ROS2_FINAL_EXAM_MODULE/ros2/install/restaurant_robot'
