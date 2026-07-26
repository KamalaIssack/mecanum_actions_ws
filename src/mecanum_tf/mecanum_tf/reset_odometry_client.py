import sys
import rclpy
from rclpy.node import Node
from mecanum_interfaces.srv import ResetOdometry


class ResetOdometryClient(Node):
    def __init__(self):
        super().__init__('reset_odometry_client')
        self.client = self.create_client(ResetOdometry, 'reset_odometry')

    def send_request(self):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for reset_odometry service...')
        request = ResetOdometry.Request()
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main():
    rclpy.init()
    node = ResetOdometryClient()
    result = node.send_request()
    node.get_logger().info(f'success={result.success} message="{result.message}"')
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
