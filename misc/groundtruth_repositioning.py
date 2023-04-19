#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R


pwd = "/home/julius/Desktop/viewpoint_sampling/misc/groundtruth_handeye.txt"
filename = "/home/julius/Desktop/viewpoint_sampling/misc/groundtruth_handeye_new.txt"

df = pd.read_csv(pwd, sep=" ", header=None)
df.columns = ["idx", "x", "y", "z", "qx", "qy", "qz", "qw"]

print(df.head())
print(df["qx"])

with open(filename, "wt") as fout:
        for idx, _ in enumerate(df["qx"]):
            r = R.from_quat([df.loc[idx, "qx"], df.loc[idx, "qy"], df.loc[idx, "qz"], df.loc[idx, "qw"]])
            r = r.as_matrix()
            #print(r)
            pose_mat = np.zeros((4,4))
            pose_mat[:3, :3] = r
            pose_mat[:3, 3] = [df.loc[idx, "x"], df.loc[idx, "y"], df.loc[idx, "z"]]
            pose_mat[3, :] = [0, 0, 0, 1]
            print(pose_mat)
            print("")
            # fout.write(line.replace(str(idx+1).zfill(6), str(idx+339).zfill(6)))


