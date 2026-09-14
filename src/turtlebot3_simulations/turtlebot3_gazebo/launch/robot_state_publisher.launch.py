#!/usr/bin/env python3
# ==============================================================================
# Robot State Publisher Launch File
# Namespace: /our_bot | Frame Prefix: our_bot/
# ==============================================================================

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    TURTLEBOT3_MODEL = os.environ.get('TURTLEBOT3_MODEL', 'waffle')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    urdf_file_name = f'turtlebot3_{TURTLEBOT3_MODEL}.urdf'

    urdf_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'urdf',
        urdf_file_name)

    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),

        # Robot state publisher automatically prepends frame_prefix to URDF links
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace='our_bot',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'robot_description': robot_desc,
                'frame_prefix': 'our_bot/'
            }],
        ),
    ])