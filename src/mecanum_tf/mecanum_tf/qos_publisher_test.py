import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from mecanum_interfaces.msg import WheelSpeeds


class QosPublisherTest(Node):
    def __init__(self):
        super().__init__('qos_publisher_test')
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = ReliabilityPolicy.BEST_EFFORT

        self.publisher = self.create_publisher(WheelSpeeds, 'wheel_speeds_qos', qos_profile)
        self.timer = self.create_timer(1.0, self.publish_speeds)
        self.get_logger().info('Publishing WheelSpeeds on /wheel_speeds_qos with BEST_EFFORT')

    def publish_speeds(self):
        msg = WheelSpeeds()
        msg.front_left = 1.0
        msg.front_right = 1.0
        msg.rear_left = 1.0
        msg.rear_right = 1.0
        self.publisher.publish(msg)
        self.get_logger().info('Published wheel speeds')


def main():
    rclpy.init()
    node = QosPublisherTest()
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
