import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_controller',
            executable='joystick_controller',
            name='joystick_controller',
            output='screen',
            parameters=[
                {'param_name': 'param_value'}  
            ]
        )
    ])