#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R


pwd = "/home/julius/Documents/dataset_424/scenes/006_standing_coated_original/groundtruth_handeye.txt"
filename = "/home/julius/Documents/dataset_424/scenes/006_standing_coated_original/groundtruth_handeye_new.txt"

#Transform: 'arc/Robolab/camera_color_optical_frame' -> 'camera_color_optical_frame'
# corr_quats = [0.0022983077076086877, 0.010939593807761348, 0.0029934279091178096, 0.9999330389872889]
# corr_trans = [0.014897541289755963, 3.0473431842648058e-06, 0.00010757303340369617]

#Transform: 'camera_color_optical_frame' -> 'arc/Robolab/camera_color_optical_frame'
# corr_quats = [-0.0053062107237441015, -0.9242243482011233, -0.0007014753764085845, 0.38181239667179484]
# corr_trans = [ -0.0421067221428114, 0.008611378363015391, 0.13242472698099847]

# #Julius1
# to_invert_quats = [0.05535879108774639, -0.9219026858920344, -0.0029388021559775394, 0.38343474729899424]
# to_invert_trans = [-0.03639694548787128, 0.0460206286575571, 0.15058235339287368]


# transform = R.from_quat(corr_quats)
# transform = transform.as_matrix()

# transform_mat = np.zeros((4,4))
# transform_mat[:3, :3] = transform
# transform_mat[:3, 3] = corr_trans
# transform_mat[3, :] = [0, 0, 0, 1]
# print(transform_mat)
# print("")

# inverse_transform_mat = np.linalg.inv(transform_mat)

# transform = R.from_quat(to_invert_quats)
# transform = transform.as_matrix()

# transform_mat_new = np.zeros((4,4))
# transform_mat_new[:3, :3] = transform
# transform_mat_new[:3, 3] = to_invert_trans
# transform_mat_new[3, :] = [0, 0, 0, 1]



df = pd.read_csv(pwd, sep=" ", header=None)
df.columns = ["idx", "x", "y", "z", "qx", "qy", "qz", "qw"]

print(df.head())

with open(filename, "wt") as fout:
        for idx, _ in enumerate(df["qx"]):
            actual_quats = [df.loc[idx, "qx"], df.loc[idx, "qy"], df.loc[idx, "qz"], df.loc[idx, "qw"]]
            actual_trans = [df.loc[idx, "x"], df.loc[idx, "y"], df.loc[idx, "z"]]
            r = R.from_quat(actual_quats)
            r = r.as_matrix()
            #print(r)
            pose_mat = np.zeros((4,4))
            pose_mat[:3, :3] = r
            pose_mat[:3, 3] = actual_trans
            pose_mat[3, :] = [0, 0, 0, 1]

            # print("pose_mat")
            # print(pose_mat)
            # print("")

            inv_pose_mat = np.linalg.inv(pose_mat)

            # quaternions
            quats = R.from_matrix(inv_pose_mat[:3, :3]).as_quat()

            # translation
            translation = inv_pose_mat[:3, 3]

            # print("inv_pose_mat")
            # print(inv_pose_mat)
            # print("")
            # new_pose = pose_mat @ inverse_transform_mat
            # new_pose = new_pose @ transform_mat_new
            # print("new_pose")
            # print(new_pose)
            # print("")

            # translation = new_pose[:3, 3]
            # quats = R.from_matrix(new_pose[:3, :3])
            # quats = quats.as_quat()
            new_line = np.append(translation, quats)

            # new_trans = np.array(np.asarray(actual_trans) + np.asarray(corr_trans))
            # new_quats = np.array(np.asarray(actual_quats) + np.asarray(corr_quats))
            # print("")
            # print((translation))
            # print((corr_trans))
            # print((new_trans))
            # print("")
            # print(type(actual_quats))
            # print(type(corr_quats))
            # print(type(new_quats))
            
            # print(new_trans)
            # print(new_quats)
            new_line = np.append(translation, quats)
            line_string = str(idx+1) + ' ' + ' '.join(map(str, new_line))
            #print(line_string)
            fout.write(line_string + '\n')


