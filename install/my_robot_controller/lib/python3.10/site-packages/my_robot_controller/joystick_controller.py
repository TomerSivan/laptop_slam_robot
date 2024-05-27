#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

class KeyboardController(Node):
    def __init__(self):
        super().__init__('keyboard_controller')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.get_logger().info('Keyboard controller node initialized')
        self.get_logger().info('Use the following keys to control the robot:')
        self.get_logger().info('  - Press W to move forward')
        self.get_logger().info('  - Press S to move backward')
        self.get_logger().info('  - Press A to turn left')
        self.get_logger().info('  - Press D to turn right')
        self.get_logger().info('  - Press any other key to stop')

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def publish_twist(self, linear_vel, angular_vel):
        # Log current speed and direction
        self.get_logger().info('Current speed: {:.2f}, Current direction: {:.2f}'.format(linear_vel, angular_vel))

        # Create Twist message
        twist = Twist()
        twist.linear.x = linear_vel
        twist.angular.z = angular_vel

        # Publish Twist message
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    keyboard_controller = KeyboardController()
    linear_vel = 0.0
    angular_vel = 0.0
    try:
        while True:
            key = keyboard_controller.getKey()
            if key == 'w':
                linear_vel = 1.0
                angular_vel = 0.0
            elif key == 's':
                linear_vel = -1.0
                angular_vel = 0.0
            elif key == 'a':
                linear_vel = 0.0
                angular_vel = 1.0
            elif key == 'd':
                linear_vel = 0.0
                angular_vel = -1.0
            else:
                linear_vel = 0.0
                angular_vel = 0.0

            keyboard_controller.publish_twist(linear_vel, angular_vel)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, keyboard_controller.settings)
        rclpy.shutdown()

if __name__ == '__main__':
    main()