#!/usr/bin/env python3

import os

"""
Moveit config params
"""
GROUP_NAME_ARM = "RoboLab"  # "tracebot_arms"
GROUP_NAME_GRIPPER = "Iiwa"
WORLD_FRAME = "arc/Robolab/world"  # "world"
ROBOT_BASE_FRAME = "linaxis_link_ee"
EEF_LINK = "iiwa_link_7"
#EEF_LINK = "camera_depth_optical_frame"
PLANNING_TIME = 80
ROBOT_SPEED = 0.01 #0-1


"""
Topic definitions
"""
POSE_ARRAY_ROS_TOPIC = "/jr_hemisphere_view_points_pose_array"
POSE_ARRAY_FLIPPED_ROS_TOPIC = "/jr_hemisphere_view_points_pose_array_flipped"
MIDDLE_POINT_HEMISPHERE_TOPIC = "/jr_hemisphere_middle_point"
HEMISPHERE_POINT_AFTER_POINT_TOPIC = "/jr_hemisphere_point_after_point"

"""
Path to file for icoshpere generation
"""
NAME_OF_PYTHON_SCRIPT_TO_CALL = os.getcwd() + "/ico_kuka.py"

"""
Coordinates of middle point of hemisphere
"""
POI_X = -0.5
POI_Y = 0.0
POI_Z = 0.9

"""
Icosphere params
"""
SUB_DIVISIONS = 1
RADIUS = 0.3

"""
Collision Box dimensions
"""
FACTOR = 1.2
BOX_X = RADIUS / FACTOR
BOX_Y = RADIUS / FACTOR
BOX_Z = RADIUS / FACTOR
