#!/usr/bin/env python3

import pandas as pd
import numpy as np
df = pd.read_json("/home/julius/Downloads/optimized_quat_extrinsics.json")
df = df.set_index('id')

# Split q and t values into separate columns
df[['qx', 'qy', 'qz', 'qw']] = pd.DataFrame(df.q.values.tolist(), index= df.index)
df[['x', 'y', 'z']] = pd.DataFrame(df.t.values.tolist(), index= df.index)

# Drop q and t columns
df = df.drop(columns=['q', 't', 'time'])

df = df[['x', 'y', 'z', 'qx', 'qy', 'qz', 'qw']]
print(df)
new_line = []
with open("groundtruth_handeye.txt", "wt") as fout:
        for idx, _ in enumerate(df["qx"]):
            actual_quats = [df.loc[idx, "qx"], df.loc[idx, "qy"], df.loc[idx, "qz"], df.loc[idx, "qw"]]
            actual_trans = [df.loc[idx, "x"], df.loc[idx, "y"], df.loc[idx, "z"]]
            #print(actual_quats)
            #print(actual_trans)
            new_line = actual_trans+ (actual_quats)
            #print(new_line)
            line_string = str(idx+1) + ' ' + ' '.join(map(str, new_line))
            print(line_string)
            fout.write(line_string + '\n')