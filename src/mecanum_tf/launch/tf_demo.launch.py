from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    static_lidar = Node(
        package='mecanum_tf',
        executable='static_lidar_broadcaster',
        name='static_lidar_broadcaster',
        output='screen',
    )

    dynamic_odom = Node(
        package='mecanum_tf',
        executable='dynamic_odom_broadcaster',
        name='dynamic_odom_broadcaster',
        output='screen',
    )

    return LaunchDescription([
        static_lidar,
        dynamic_odom,
    ])
