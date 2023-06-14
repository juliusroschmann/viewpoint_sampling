#!/usr/bin/env python3
#!/usr/bin/env python3

import os
import shutil
import fnmatch
import json

#subsamples = [10,20,30,40,50,60,80,100,200,300]
subsamples = [50]

#scenes = ['001_standing_coated', '002_lying_coated', '003_standing_liquid', '004_lying_liquid', '005_standing_empty', '006_lying_empty']
scenes = ['001_standing_coated']


path_to_master = '/home/julius/Documents/Julius_03_x_auswertung/Julius_03_' 
#path_to_master = '/home/julius/Videos/Julius_03_x/Julius_03_' 
#folders = ["rgb_nerf", "depth_nerf", "depth_norm_nerf"]
file = "transforms.json"

extension = "_v2_centered_nerfacto_only_subsamples_v2"

for subsample in subsamples:
    for scene in scenes:
        path = path_to_master + f"{subsample}/scenes/{scene}/{file}"  
        dest = os.path.dirname(path)+"/transforms_backup.json"
        
        #shutil.copy2(path, dest)

        #read json file
        with open(path) as f: 
            data = json.load(f)

        #append new item
        for frame in data['frames']:
            frame['depth_file_path'] = frame['file_path'].replace('rgb','depth')

        #write to file
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

        exit()

        # dest = os.path.dirname(path.replace("Videos/Julius_03_x", "Documents/Julius_03_x_auswertung")) + f"/{file}{extension}"
        # #print(dest)
        # os.makedirs(dest, exist_ok=True)
        # dest_names_to_read = dest.replace(f"{file}{extension}", "rgb")
        # files = sorted([os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        # file_names_to_read = sorted([os.path.basename(os.path.join(dest_names_to_read, f)) for f in os.listdir(dest_names_to_read) if os.path.isfile(os.path.join(dest_names_to_read, f))])
        
        # for idx, file in enumerate(files):
        #     dest2 = os.path.join(dest, file_names_to_read[idx])
        #     shutil.copy2(file, dest2)
            
        #     # if os.path.basename(file) in subsample_image_names:
                
        #     #     shutil.copy2(file, dest)
                
                







# import pandas as pd
# import numpy as np
# df = pd.read_json("/home/julius/Downloads/optimized_quat_extrinsics.json")
# df = df.set_index('id')

# # Split q and t values into separate columns
# df[['qx', 'qy', 'qz', 'qw']] = pd.DataFrame(df.q.values.tolist(), index= df.index)
# df[['x', 'y', 'z']] = pd.DataFrame(df.t.values.tolist(), index= df.index)

# # Drop q and t columns
# df = df.drop(columns=['q', 't', 'time'])

# df = df[['x', 'y', 'z', 'qx', 'qy', 'qz', 'qw']]
# print(df)
# new_line = []
# with open("groundtruth_handeye.txt", "wt") as fout:
#         for idx, _ in enumerate(df["qx"]):
#             actual_quats = [df.loc[idx, "qx"], df.loc[idx, "qy"], df.loc[idx, "qz"], df.loc[idx, "qw"]]
#             actual_trans = [df.loc[idx, "x"], df.loc[idx, "y"], df.loc[idx, "z"]]
#             #print(actual_quats)
#             #print(actual_trans)
#             new_line = actual_trans+ (actual_quats)
#             #print(new_line)
#             line_string = str(idx+1) + ' ' + ' '.join(map(str, new_line))
#             print(line_string)
#             fout.write(line_string + '\n')