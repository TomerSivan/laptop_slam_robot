import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pynput import keyboard

class KeyboardControlNode(Node):
    def __init__(self):
        super().__init__('keyboard_control_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.twist_msg = Twist()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def publish_twist(self, linear_x, angular_z):
        self.twist_msg.linear.x = linear_x
        self.twist_msg.angular.z = angular_z
        self.publisher_.publish(self.twist_msg)

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.publish_twist(0.8, 0.0)  # Move forward
            elif key.char == 's':
                self.publish_twist(-0.8, 0.0)  # Move backward
            elif key.char == 'a':
                self.publish_twist(0.0, 0.95)  # Turn left
            elif key.char == 'd':
                self.publish_twist(0.0, -0.95)  # Turn right
            else:
                self.publish_twist(0.0, 0.0)  # Stop
            self.get_logger().info(f"Published Twist: Linear: {self.twist_msg.linear.x}, Angular: {self.twist_msg.angular.z}")
        except AttributeError:
            self.publish_twist(0.0, 0.0)  # Stop on any other key press

def main(args=None):
    rclpy.init(args=args)
    keyboard_control_node = KeyboardControlNode()
    rclpy.spin(keyboard_control_node)
    keyboard_control_node.listener.stop()
    rclpy.shutdown()

if __name__ == '__main__':
    main()