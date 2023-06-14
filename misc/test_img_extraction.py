#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import os
import shutil
import fnmatch
import sys

#subsamples = [10,20,30,40,50,60,80,100,200,300]
subsamples = [50]

#scenes = ['001_standing_coated', '002_lying_coated', '003_standing_liquid', '004_lying_liquid', '005_standing_empty', '006_lying_empty']
scenes = ['001_standing_coated']

test_img_indices = [3, 12, 13, 17, 18, 22, 23, 27, 30, 33, 34, 36, 41, 43, 46, 47, 49, 56, 64, 79, 87, 93, 97, 99, 103, 105, 106, 107, 108, 111, 112, 113, 114, 120, 121, 123, 124, 125, 127, 131, 137, 140, 156, 157, 166, 168, 171, 174, 179, 182, 183, 186, 187, 189, 195, 196, 197, 201, 202, 203, 212, 213, 214,
                    217, 224, 225, 230, 234, 235, 239, 242, 245, 250, 252, 253, 254, 255, 257, 258, 261, 268, 276, 301, 302, 305, 307, 308, 309, 311, 317, 319, 320, 324, 325, 327, 328, 329, 333, 335, 336, 339, 341, 349, 353, 368, 376, 380, 383, 386, 387, 391, 392, 395, 396, 402, 403, 408, 409, 410, 413, 414, 419, 420, 424]
subsample_image_names = [(str(item).zfill(6)) +
                            '.png' for item in test_img_indices]

#/home/julius/Documents/Julius_03_x_auswertung/Julius_03_10/scenes/001_standing_coated/depth_nerf_v2_centered_nerfacto
#/home/julius/Documents/Julius_03_x_auswertung/Julius_03_10/scenes/001_standing_coated/depth_nerf_124

#path_to_master = '/home/julius/Documents/Julius_03_x_auswertung/Julius_03_' 
path_to_master = '/home/julius/Videos/Julius_03_x/Julius_03_' 
#folders = ["rgb_nerf", "depth_nerf", "depth_norm_nerf"]
folders = ["depth_nerf"]

extension = "_v2_centered_nerfacto_only_subsamples_v2"

for folder in folders:
    for subsample in subsamples:
        for scene in scenes:
            path = path_to_master + f"{subsample}/scenes/{scene}/{folder}"
            #print(path)
            dest = os.path.dirname(path.replace("Videos/Julius_03_x", "Documents/Julius_03_x_auswertung")) + f"/{folder}{extension}"
            #print(dest)
            os.makedirs(dest, exist_ok=True)
            dest_names_to_read = dest.replace(f"{folder}{extension}", "rgb")
            files = sorted([os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            file_names_to_read = sorted([os.path.basename(os.path.join(dest_names_to_read, f)) for f in os.listdir(dest_names_to_read) if os.path.isfile(os.path.join(dest_names_to_read, f))])
            
            for idx, file in enumerate(files):
                dest2 = os.path.join(dest, file_names_to_read[idx])
                shutil.copy2(file, dest2)
              
                # if os.path.basename(file) in subsample_image_names:
                    
                #     shutil.copy2(file, dest)
                    
                
