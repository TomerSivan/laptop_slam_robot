#!/bin/bash
source ~/.bashrc
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=1

# Get the PID of the terminal
TERMINAL_PID=$$

# Output the PID to a file
echo $TERMINAL_PID > terminal_pid.txt

echo "PID of the terminal: $TERMINAL_PID"

# Launch the ROS 2 node and capture its PID
ros2 launch my_robot_controller robot_on.launch.py