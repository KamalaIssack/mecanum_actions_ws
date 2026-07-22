import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster


class StaticLidarBroadcaster(Node):
    def __init__(self):
        super().__init__('static_lidar_broadcaster')

        # The object that will publish onto /tf_static
        self.broadcaster = StaticTransformBroadcaster(self)

        # Build and send the transform once
        self.publish_transform()

    def publish_transform(self):
        t = TransformStamped()

        # WHEN and WHO
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'      # parent
        t.child_frame_id = 'lidar_link'      # child

        # WHERE (translation, in metres)
        t.transform.translation.x = 0.20
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.15

        # HOW IT IS ROTATED (identity = no rotation)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.broadcaster.sendTransform(t)
        self.get_logger().info('Published static transform base_link -> lidar_link')


def main():
    rclpy.init()
    node = StaticLidarBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
    