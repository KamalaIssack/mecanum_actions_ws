# mecanum_actions_ws

> **Archive notice:** This repository is a ROS 2 fundamentals learning archive. The production packages (`mecanum_description`, `mecanum_interfaces`) and the physical robot now live in [Mecanum-wheel-mobile-robot-project](https://github.com/KamalaIssack/Mecanum-wheel-mobile-robot-project), under `ros2_ws/`. Some learning nodes in `mecanum_tf` import `mecanum_interfaces` and will no longer build here — that's expected for an archive and not a bug.

## Overview

A ROS 2 Jazzy colcon workspace used to learn ROS 2 fundamentals: tf2 broadcasters, launch files, custom interfaces, and QoS behavior.

## Packages

- **`mecanum_tf`** — learning nodes covering:
  - Static and dynamic tf2 broadcasters (`static_lidar_broadcaster`, `dynamic_odom_broadcaster`)
  - A launch file (`tf_demo.launch.py`) that runs both broadcasters together
  - A `ResetOdometry` service client/server pair
  - A `MoveForSeconds` action client/server pair
  - QoS profile demo: a publisher and a subscriber with matched QoS settings

## Building

```bash
colcon build
source install/setup.bash
```

Note that `mecanum_tf` nodes depending on `mecanum_interfaces` (the service/action demos) will fail to build here since that package moved to the production repo. The tf2 broadcaster and QoS demo nodes are unaffected.
