import rclpy
from rclpy.node import Node
from mecanum_interfaces.msg import WheelSpeeds


class WheelSpeedTestPublisher(Node):
    def __init__(self):
        super().__init__('wheel_speed_test_publisher')
        self.publisher = self.create_publisher(WheelSpeeds, 'wheel_speeds', 10)
        self.timer = self.create_timer(1.0, self.publish_speeds)
        self.get_logger().info('Publishing WheelSpeeds on /wheel_speeds at 1 Hz')

    def publish_speeds(self):
        msg = WheelSpeeds()
        msg.front_left = 0.5
        msg.front_right = 0.5
        msg.rear_left = 0.5
        msg.rear_right = 0.5
        self.publisher.publish(msg)
        self.get_logger().info(
            f'Published: FL={msg.front_left} FR={msg.front_right} '
            f'RL={msg.rear_left} RR={msg.rear_right}'
        )


def main():
    rclpy.init()
    node = WheelSpeedTestPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
