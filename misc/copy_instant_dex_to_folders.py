#!/usr/bin/env python3

import shutil
import os

path_to_master = "/home/julius/Documents/instant_dex_nerf/"
path_to_scenes = sorted(os.listdir(path_to_master) )#, key=lambda x: int(x.split('_')[2]))
path_to_scenes = [os.path.join(path_to_master, dir) for dir in path_to_scenes]

for path in path_to_scenes:
    scene_names = os.path.split(path)[1]
    scene = scene_names.split("scenes_")[1]
    subdir = scene_names.split("full_")[1]
    subdir = subdir.split("_scenes")[0]

    #print(path)
    new_path = "/home/julius/Documents/Julius_03_x_auswertung/" + subdir + "/instant-dex_nerf_full/" + scene + "/depth_new/"
    shutil.move(path, new_path)
    #print(new_path)
    #print("")