# ==============================================================================
# Spawn TurtleBot3 & Bridge Bringup Launch File
# Namespace: /our_bot
# ==============================================================================

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    TURTLEBOT3_MODEL = os.environ.get('TURTLEBOT3_MODEL', 'waffle')
    model_folder = 'turtlebot3_' + TURTLEBOT3_MODEL

    urdf_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'models',
        model_folder,
        'model.sdf'
    )

    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')

    declare_x_position_cmd = DeclareLaunchArgument('x_pose', default_value='-2.0')
    declare_y_position_cmd = DeclareLaunchArgument('y_pose', default_value='-0.5')

    # Spawns SDF model into Gazebo with 'our_bot' entity name
    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'our_bot',
            '-file', urdf_path,
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01'
        ],
        output='screen',
    )

    bridge_params = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'params',
        model_folder + '_bridge.yaml'
    )

    # ROS-Gazebo bridge loading our updated parameter file
    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p', f'config_file:={bridge_params}',
        ],
        output='screen',
    )

    # Image bridge for camera feed scoped to robot namespace
    start_gazebo_ros_image_bridge_cmd = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/our_bot/camera/image_raw'],
        output='screen',
    )

    ld = LaunchDescription()
    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)
    ld.add_action(start_gazebo_ros_spawner_cmd)
    ld.add_action(start_gazebo_ros_bridge_cmd)
    ld.add_action(start_gazebo_ros_image_bridge_cmd)

    return ld