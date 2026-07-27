import time
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from mecanum_interfaces.action import MoveForSeconds


class MoveForSecondsServer(Node):
    def __init__(self):
        super().__init__('move_for_seconds_server')
        self.action_server = ActionServer(
            self,
            MoveForSeconds,
            'move_for_seconds',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup(),
        )
        self.get_logger().info('MoveForSeconds action server ready')

    def goal_callback(self, goal_request):
        self.get_logger().info(f'Received goal: duration={goal_request.duration}')
        if goal_request.duration <= 0.0:
            self.get_logger().warn('Rejecting goal: duration must be positive')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        duration = goal_handle.request.duration
        feedback_msg = MoveForSeconds.Feedback()
        start = time.time()

        while (time.time() - start) < duration:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = MoveForSeconds.Result()
                result.success = False
                result.message = 'Canceled by client'
                self.get_logger().info('Goal canceled')
                return result

            feedback_msg.elapsed = time.time() - start
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: elapsed={feedback_msg.elapsed:.1f}')
            time.sleep(1.0)

        goal_handle.succeed()
        result = MoveForSeconds.Result()
        result.success = True
        result.message = f'Moved for {duration} seconds'
        return result


def main():
    rclpy.init()
    node = MoveForSecondsServer()
    executor = MultiThreadedExecutor()
    try:
        rclpy.spin(node, executor=executor)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
