# ==============================================================================
# Spawn Launch File for enemy_bot
# Namespaces state publisher to /enemy_bot, sets frame_prefix to enemy_bot/,
# passes explicit spawn height z=0.05 (prevents ground mesh collision), and yaw=3.14159.
# ==============================================================================

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_gazebo = get_package_share_directory('turtlebot3_gazebo')
    
    sdf_path = os.path.join(pkg_gazebo, 'models', 'turtlebot3_waffle', 'model_enemy_bot.sdf')
    bridge_params = os.path.join(pkg_gazebo, 'params', 'enemy_bot_bridge.yaml')
    urdf_path = os.path.join(pkg_gazebo, 'urdf', 'turtlebot3_waffle.urdf')

    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    x_pose = LaunchConfiguration('x_pose', default='2.0')
    y_pose = LaunchConfiguration('y_pose', default='0.5')
    z_pose = LaunchConfiguration('z_pose', default='0.05')
    yaw_pose = LaunchConfiguration('yaw_pose', default='3.14159')

    declare_x_cmd = DeclareLaunchArgument('x_pose', default_value='2.0')
    declare_y_cmd = DeclareLaunchArgument('y_pose', default_value='0.5')
    declare_z_cmd = DeclareLaunchArgument('z_pose', default_value='0.05')
    declare_yaw_cmd = DeclareLaunchArgument('yaw_pose', default_value='3.14159')

    spawner_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'enemy_bot',
            '-file', sdf_path,
            '-x', x_pose,
            '-y', y_pose,
            '-z', z_pose,
            '-Y', yaw_pose,
            '-yaw', yaw_pose
        ],
        output='screen',
    )

    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace='enemy_bot',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_desc,
            'frame_prefix': 'enemy_bot/'
        }],
    )

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='enemy_bot_bridge',
        arguments=[
            '--ros-args',
            '-p', f'config_file:={bridge_params}',
        ],
        output='screen',
    )

    return LaunchDescription([
        declare_x_cmd,
        declare_y_cmd,
        declare_z_cmd,
        declare_yaw_cmd,
        spawner_node,
        robot_state_pub,
        bridge_node
    ])