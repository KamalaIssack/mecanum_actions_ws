import signal
import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from mecanum_interfaces.action import MoveForSeconds


class MoveForSecondsClient(Node):
    def __init__(self):
        super().__init__('move_for_seconds_client')
        self.action_client = ActionClient(self, MoveForSeconds, 'move_for_seconds')
        self.goal_handle = None

    def send_goal(self, duration):
        self.action_client.wait_for_server()
        goal_msg = MoveForSeconds.Goal()
        goal_msg.duration = duration

        self.get_logger().info(f'Sending goal: duration={duration}')
        send_goal_future = self.action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().info('Goal was rejected')
            rclpy.shutdown()
            return
        self.get_logger().info('Goal accepted')
        result_future = self.goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback):
        self.get_logger().info(f'Feedback: elapsed={feedback.feedback.elapsed:.1f}')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: success={result.success} message="{result.message}"')
        rclpy.shutdown()

    def cancel_goal(self):
        if self.goal_handle is not None:
            self.get_logger().info('Sending cancel request')
            self.goal_handle.cancel_goal_async()


def main():
    rclpy.init()
    node = MoveForSecondsClient()
    duration = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0

    def handle_sigint(sig, frame):
        node.get_logger().info('Ctrl-C received, sending cancel request')
        node.cancel_goal()

    signal.signal(signal.SIGINT, handle_sigint)
    node.send_goal(duration)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
