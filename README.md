# ITDS331_ROS2_FINAL_EXAM_MODULE
เปิด world ร้านอาหารใน Gazebo

    ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py world:=<path_to_world>/restaurant.world

เปิดระบบ SLAM

    ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
    ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True

เปิด teleoperation เพื่อควบคุมหุ่นยนต์

    ros2 run turtlebot3_teleop teleop_keyboard

บันทึกแผนที่ 
เมื่อสำรวจครบแล้ว เปิด terminal ใหม่ แล้วรัน:

    ros2 run nav2_map_server map_saver_cli -f ~/map_restaurant
    -> map_restaurant.yaml
       map_restaurant.pgm

ตรวจสอบผลลัพธ์
เปิดดูด้วย Rviz2:

    ros2 launch turtlebot3_cartographer rviz.launch.py
