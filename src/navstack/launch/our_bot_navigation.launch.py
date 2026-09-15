#!/usr/bin/env python3
# ==============================================================================
# Nav2 Navigation Stack Launch File
# Namespace: /our_bot
# ==============================================================================

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('navstack')

    controller_yaml = os.path.join(pkg_share, 'config', 'our_bot_controller.yaml')
    bt_navigator_yaml = os.path.join(pkg_share, 'config', 'our_bot_bt_navigator.yaml')
    planner_yaml = os.path.join(pkg_share, 'config', 'our_bot_planner_server.yaml')
    recovery_yaml = os.path.join(pkg_share, 'config', 'our_bot_recovery.yaml')
    amcl_yaml = os.path.join(pkg_share, 'config', 'our_bot_amcl.yaml')
    map_file = os.path.join(pkg_share, 'maps', 'my_nav_map.yaml')
    behavior_xml = os.path.join(pkg_share, 'config', 'our_bot_behavior.xml')

    namespace = 'our_bot'


    return LaunchDescription([
        # ----------------------------------------------------------------------
        # 1. SHARED GLOBAL MAP SERVER
        # DIFFERENCE: Map server runs WITHOUT a namespace so all robots share 
        # the single global /map topic.
        # ----------------------------------------------------------------------
        # 1. Map Server (Unscoped global node)
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'use_sim_time': True, 'yaml_filename': map_file}]
        ),

        # 2. Robot Scoped Navigation Nodes
        Node(
            namespace=namespace,
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[amcl_yaml],
            # remappings=[
            #     ('map', '/map'),
            #     ('/initialpose', '/our_bot/initialpose'),
            #     ('initialpose', '/our_bot/initialpose')
            # ]
        ),
        Node(
            namespace=namespace,
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[planner_yaml],
            # remappings=[('map', '/map')]
        ),
        Node(
            namespace=namespace,
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[controller_yaml]
        ),
        Node(
            namespace=namespace,
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            output='screen',
            parameters=[recovery_yaml]
        ),
        Node(
            namespace=namespace,
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[bt_navigator_yaml, {'default_nav_to_pose_bt_xml': behavior_xml}],
            # remappings=[
            #     ('/goal_pose', '/our_bot/goal_pose'),
            #     ('goal_pose', '/our_bot/goal_pose')
            # ]
        ),

        # 3. SINGLE UNIFIED LIFECYCLE MANAGER
        # Explicit node list guarantees map_server is active BEFORE amcl and costmaps transition
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_our_bot',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'autostart': True,
                'bond_timeout': 0.0,
                'node_names': [
                    'map_server',
                    'our_bot/amcl',
                    'our_bot/planner_server',
                    'our_bot/controller_server',
                    'our_bot/behavior_server',
                    'our_bot/bt_navigator'
                ]
            }]
        )
    ])