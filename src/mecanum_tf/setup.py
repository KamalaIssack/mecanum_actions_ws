import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mecanum_tf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='isaackamala11@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
             'static_lidar_broadcaster = mecanum_tf.static_lidar_broadcaster:main',
             'dynamic_odom_broadcaster = mecanum_tf.dynamic_odom_broadcaster:main',
             'wheel_speed_test_publisher = mecanum_tf.wheel_speed_test_publisher:main',
             'reset_odometry_client = mecanum_tf.reset_odometry_client:main',
             'move_for_seconds_server = mecanum_tf.move_for_seconds_server:main',
             'move_for_seconds_client = mecanum_tf.move_for_seconds_client:main',
        ],
    },
)
