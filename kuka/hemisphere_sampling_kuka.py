#!/usr/bin/env python3

import copy
import geometry_msgs.msg
import moveit_commander
import moveit_msgs.msg
import rospy
import subprocess
import sys
import numpy as np
import pandas as pd
import math
from scipy.spatial.transform import Rotation as R
from settings_kuka import *
from moveit_commander.conversions import pose_to_list

def all_close(goal, actual, tolerance_d=0.01, tolerance_phi_rad=np.deg2rad(5)):
    """
    Check if goal and actual are within [tolerance_d] meters and [tolerance_phi_rad] radians from each other.
    Adapted from http://docs.ros.org/en/kinetic/api/moveit_tutorials/html/doc/move_group_python_interface/move_group_python_interface_tutorial.html
    :param goal:  goal pose to compare to
    :param actual: actual robot pose
    :param tolerance_d: euclidian distance from goal
    :param tolerance_phi_rad: angular divergence from goal
    :return: (bool, float, float): success if within tolerance, delta_d, delta_phi
    """
    if type(goal) is list:
        for index in range(len(goal)):
            if np.abs(actual[index] - goal[index]) > tolerance_d:
                return False
    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance_d, tolerance_phi_rad)
    elif type(goal) is geometry_msgs.msg.Pose:
        x0, y0, z0, qx0, qy0, qz0, qw0 = pose_to_list(actual)
        x1, y1, z1, qx1, qy1, qz1, qw1 = pose_to_list(goal)
        d = np.linalg.norm([x1-x0, y1-y0, z1-z0])
        cos_phi = np.abs(np.dot([qx0, qy0, qz0, qw0], [qx1, qy1, qz1, qw1]))
        rospy.loginfo("tolerances")
        rospy.loginfo(d)
        rospy.loginfo(cos_phi)
        return d <= tolerance_d and cos_phi >= np.cos(tolerance_phi_rad)
    return True

class HemisphereMotion:
    """
    A class that provides methods to perform motion tasks related to the hemisphere.
    """
    def __init__(self) -> None:
        """
        Constructor. Set up the MoveGroupCommander objects and the publishers.
        """
        self.scene = moveit_commander.PlanningSceneInterface()
        self.scene.clear()
        self.move_group = moveit_commander.MoveGroupCommander(GROUP_NAME_ARM)
        self.move_group.set_max_velocity_scaling_factor(ROBOT_SPEED)
        self.move_group.set_max_acceleration_scaling_factor(ROBOT_SPEED)
        self.move_group.set_end_effector_link(EEF_LINK)
        self.move_group.set_planning_time(PLANNING_TIME)
        self.gripper = moveit_commander.MoveGroupCommander(GROUP_NAME_GRIPPER)

        self.hemisphere_point_after_point_publisher = rospy.Publisher(
            HEMISPHERE_POINT_AFTER_POINT_TOPIC,
            geometry_msgs.msg.PoseStamped,
            queue_size=0,
        )
        self.display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )

    def run_other_script(self, name=NAME_OF_PYTHON_SCRIPT_TO_CALL):
        """
        Runs the python script to generate the icosphere in a subprocess.
        :param name: Name of the python script to call
        :return:
        """
        subprocess.Popen(executable=name, args="")

    def get_middle_point(self):
        """
        Waits for a message containing the middle point of the hemisphere.
        """
        rospy.loginfo("WAITING FOR VIEWING HEMISPHERE!")
        self.middle_point = rospy.wait_for_message(
            MIDDLE_POINT_HEMISPHERE_TOPIC, geometry_msgs.msg.PoseStamped
        )

    def get_pose_array(self):
        """
        Waits for a message containing the pose array of the hemisphere.
        """
        self.pose_array = rospy.wait_for_message(
            POSE_ARRAY_ROS_TOPIC, geometry_msgs.msg.PoseArray
        )

    def get_pose_array_flipped(self):
        """
        Waits for a message containing the flipped pose array of the hemisphere.
        """
        self.pose_array_flipped = rospy.wait_for_message(
            POSE_ARRAY_FLIPPED_ROS_TOPIC, geometry_msgs.msg.PoseArray
        )

    def convert_pose_array(self):
        """
        Most important function. Converts the pose array to PoseStamped messages which are approached succinctly.
        """
        self.move_group.clear_pose_targets()
        pose_s_list = []
        approached_poses_s = []
        data = {"Idx": [], "SubDiv": [], "Point": [], "Orientation": [],
             "Succ. Approached": [], "Error": [], "Delta_d": [], "Delta_phi": []}
        df_pose_array = pd.DataFrame(data=data)

        for idx, pose in enumerate(self.pose_array.poses):
            pose_s = geometry_msgs.msg.PoseStamped(
                pose=pose, header=self.pose_array.header)
            self.hemisphere_point_after_point_publisher.publish(pose_s)
            pose_s_list.append(pose_s)
            rospy.sleep(0.5)

            try:
                self.move_group.go(pose_s, wait=True)
                success, delta_d, delta_phi = all_close(
                    pose_s, self.move_group.get_current_pose().pose)
                delta_d = np.around(delta_d, decimals=4)
                delta_phi = np.around(delta_phi, decimals=4)
                print("SUCCESS:", success)
                if success:
                    approached_poses_s.append(pose_s)
                    new_row = pd.Series({"Idx": idx, "SubDiv": -1, "Point": np.around(pose_to_list(pose_s.pose)[:3], decimals=4), "Orientation": np.around(pose_to_list(
                        pose_s.pose)[3:], decimals=4), "Succ. Approached": 1, "Error": "Pose reached within tolerance", "Delta_d": delta_d, "Delta_phi": delta_phi})
                else:
                    new_row = pd.Series({"Idx": idx, "SubDiv": -1, "Point": np.around(pose_to_list(pose_s.pose)[:3], decimals=4), "Orientation": np.around(pose_to_list(
                        pose_s.pose)[3:], decimals=4), "Succ. Approached": 0, "Error": "Pose reached NOT within tolerance", "Delta_d": delta_d, "Delta_phi": delta_phi})

            except Exception as excep:
                print(excep)
                print("SKIPPING pose_s: {}".format(
                    np.around(pose_to_list(pose_s.pose), decimals=4)))
                new_row = pd.Series({"Idx": idx, "SubDiv": -1, "Point": np.around(pose_to_list(pose_s.pose)[:3], decimals=4), "Orientation": np.around(
                    pose_to_list(pose_s.pose)[3:], decimals=4), "Succ. Approached": 0, "Error": excep, "Delta_d": -1, "Delta_phi": -1})

            df_pose_array.loc[len(df_pose_array)] = new_row

        print(df_pose_array.to_string())
        df_pose_array.to_csv("pose_array_executed.csv", index=False)


    def add_box(self):
        """
        Adds a collision box inside the hemisphere to avoid collision with scene objects.
        """
        self.box_name = "box"
        self.scene.add_box(self.box_name, self.middle_point,
                           size=(BOX_X, BOX_Y, BOX_Z))
        return #self.wait_for_state_update(box_is_known=True, timeout=timeout)
        
    # def move_taskspace(self, pose_goal, max_timeout=PLANNING_TIME):
    #     """
    #     Function to control the robot motion.
    #     """

    #     self.move_group.clear_pose_targets()
    #     # plan and execute
    #     try:
    #         self.move_group.set_pose_target(pose_goal)
    #         self.move_group.go(wait=True)

    #     except moveit_commander.exception.MoveItCommanderException as excep:
    #         rospy.loginfo("return alternative pose")

    #     self.move_group.stop()
    #     self.move_group.clear_pose_targets()
    #     rospy.loginfo("waiting until the goal is reached")
    #     timeout = 0
    #     while timeout < max_timeout and not all_close(pose_goal, self.move_group.get_current_pose().pose):
    #         rospy.sleep(0.5)
    #         timeout += 0.5
    #     return (all_close(pose_goal, self.move_group.get_current_pose().pose))


    def add_planning_scene_limits(self):
        """
        Adds walls, table, etc to avoid collision with real world objects.
        """
        planning_frame = self.move_group.get_planning_frame()

        # add a table plane
        self.table_plane_name = "table_plane"
        self.table_plane_pose = geometry_msgs.msg.PoseStamped()
        self.table_plane_pose.header.frame_id = planning_frame

        self.table_plane_pose.pose.position.x = 0.0
        self.table_plane_pose.pose.position.y = 0.0
        self.table_plane_pose.pose.position.z = 0.73
        self.table_plane_pose.pose.orientation.w = 1.0     

        self.scene.add_box(self.table_plane_name, self.table_plane_pose, size=(2.6, 2.6, 0.02))

        # add a box defining the window
        self.box_window_pose_name = "window_side_limit"
        self.box_window_pose = geometry_msgs.msg.PoseStamped()
        self.box_window_pose.header.frame_id = planning_frame

        self.box_window_pose.pose.position.x = 0.0
        self.box_window_pose.pose.position.y = 1.0
        self.box_window_pose.pose.position.z = 0.8
        self.box_window_pose.pose.orientation.w = 1.0
        
        self.scene.add_box(self.box_window_pose_name, self.box_window_pose, size=(3.0, 0.1, 1.8))

        # add a box for the table side
        self.box_table_pose_name = "table_side_limit"
        self.box_table_pose = geometry_msgs.msg.PoseStamped()
        self.box_table_pose.header.frame_id = planning_frame

        self.box_table_pose.pose.position.x = 0.0
        self.box_table_pose.pose.position.y = -1.0
        self.box_table_pose.pose.position.z = 0.8
        self.box_table_pose.pose.orientation.w = 1.0

        self.scene.add_box(self.box_table_pose_name, self.box_table_pose, size=(3.0, 0.1, 1.8))

        # add a box to limit the middle
        self.box_middle_pose_name = "middle_limit"
        self.box_middle_pose = geometry_msgs.msg.PoseStamped()
        self.box_middle_pose.header.frame_id = planning_frame
        
        self.box_middle_pose.pose.position.x = 0.0
        self.box_middle_pose.pose.position.y = 0.0
        self.box_middle_pose.pose.position.z = 0.8
        self.box_middle_pose.pose.orientation.w = 1.0
        
        self.scene.add_box(self.box_middle_pose_name, self.box_middle_pose, size=(0.1, 2.0, 1.4))

        # add a box for the cables
        self.cable_pose_name = "cable_box"
        self.cable_pose = geometry_msgs.msg.PoseStamped()
        self.cable_pose.header.frame_id = ROBOT_BASE_FRAME

        self.cable_pose.pose.position.x = 0.19
        self.cable_pose.pose.position.y = 0.375
        self.cable_pose.pose.position.z = 0.12
        self.cable_pose.pose.orientation.w = 1.0
        
        self.scene.add_box(self.cable_pose_name, self.cable_pose, size=(0.2, 0.65, 0.2))
        self.scene.attach_box(ROBOT_BASE_FRAME, self.cable_pose_name)
        

def main():
    """
    Function to control the program execution.
    """
    try:
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("jr_hemisphere_motion", anonymous=True)

        hemisphere_motion = HemisphereMotion()
        hemisphere_motion.add_planning_scene_limits()
        hemisphere_motion.run_other_script()
        hemisphere_motion.get_middle_point()
        hemisphere_motion.get_pose_array()
        hemisphere_motion.get_pose_array_flipped()
        hemisphere_motion.add_box()
        hemisphere_motion.convert_pose_array()

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
