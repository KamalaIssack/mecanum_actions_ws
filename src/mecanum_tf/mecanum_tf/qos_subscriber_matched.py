import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from mecanum_interfaces.msg import WheelSpeeds


class QosSubscriberMatched(Node):
    def __init__(self):
        super().__init__('qos_subscriber_matched')
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = ReliabilityPolicy.BEST_EFFORT

        self.subscription = self.create_subscription(
            WheelSpeeds, 'wheel_speeds_qos', self.listener_callback, qos_profile
        )
        self.get_logger().info('Subscribing to /wheel_speeds_qos with BEST_EFFORT')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: FL={msg.front_left}')


def main():
    rclpy.init()
    node = QosSubscriberMatched()
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
