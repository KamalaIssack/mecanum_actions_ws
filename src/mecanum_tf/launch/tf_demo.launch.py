import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config_file = os.path.join(
    get_package_share_directory('mecanum_tf'),
    'config',
    'lidar_params.yaml'
)
    static_lidar = Node(
        package='mecanum_tf',
        executable='static_lidar_broadcaster',
        name='static_lidar_broadcaster',
        output='screen',
        parameters=[config_file],
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
