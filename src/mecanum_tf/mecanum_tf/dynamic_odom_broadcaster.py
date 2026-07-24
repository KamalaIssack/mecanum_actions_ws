import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class DynamicOdomBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_odom_broadcaster')

        # Note: TransformBroadcaster, not StaticTransformBroadcaster.
        # This one publishes to /tf instead of /tf_static.
        self.broadcaster = TransformBroadcaster(self)

        # Remember when we started, so we can measure elapsed time
        self.start_time = self.get_clock().now()

        # Fire publish_transform 30 times per second
        self.timer = self.create_timer(1.0 / 30.0, self.publish_transform)

        self.get_logger().info('Publishing odom -> base_link on /tf at 30 Hz')

    def publish_transform(self):
        now = self.get_clock().now()

        # Seconds since the node started
        elapsed = (now - self.start_time).nanoseconds / 1e9

        # PRETEND MOTION.
        # This is where real wheel odometry from the STM32 will go later.
        # For now, drive a slow 1 metre circle and face along the path.
        radius = 1.0
        speed = 0.3                      # radians per second
        angle = speed * elapsed

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        yaw = angle + math.pi / 2.0      # face along the direction of travel

        t = TransformStamped()

        t.header.stamp = now.to_msg()
        t.header.frame_id = 'odom'        # parent
        t.child_frame_id = 'base_link'    # child

        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = 0.0

        # Convert a yaw angle into a quaternion.
        # For rotation about z only, this is the simple form.
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(yaw / 2.0)
        t.transform.rotation.w = math.cos(yaw / 2.0)

        self.broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = DynamicOdomBroadcaster()
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
