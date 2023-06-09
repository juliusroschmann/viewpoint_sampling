#!/usr/bin/env python3

import io
import signal
import subprocess

subsamples = [10,20,30,40,50,60,80,100,200,300]
#subsamples = [10]

scenes = ['001_standing_coated', '002_lying_coated', '003_standing_liquid', '004_lying_liquid', '005_standing_empty', '006_lying_empty']
# test_img_indices = [3, 12, 13, 17, 18, 22, 23, 27, 30, 33, 34, 36, 41, 43, 46, 47, 49, 56, 64, 79, 87, 93, 97, 99, 103, 105, 106, 107, 108, 111, 112, 113, 114, 120, 121, 123, 124, 125, 127, 131, 137, 140, 156, 157, 166, 168, 171, 174, 179, 182, 183, 186, 187, 189, 195, 196, 197, 201, 202, 203, 212, 213, 214,
#                     217, 224, 225, 230, 234, 235, 239, 242, 245, 250, 252, 253, 254, 255, 257, 258, 261, 268, 276, 301, 302, 305, 307, 308, 309, 311, 317, 319, 320, 324, 325, 327, 328, 329, 333, 335, 336, 339, 341, 349, 353, 368, 376, 380, 383, 386, 387, 391, 392, 395, 396, 402, 403, 408, 409, 410, 413, 414, 419, 420, 424]
# subsample_image_names = [(str(item).zfill(6)) +
#                             '.png' for item in test_img_indices]

#/home/julius/Documents/Julius_03_x_auswertung/Julius_03_10/scenes/001_standing_coated/depth_nerf_v2_centered_nerfacto
#/home/julius/Documents/Julius_03_x_auswertung/Julius_03_10/scenes/001_standing_coated/depth_nerf_124

#python3 /home/julius/Downloads/3D-DAT-master/scripts/reconstruct.py -d /home/julius/Documents/Julius_03_x_auswertung/Julius_03_50/config_nerf_v2_centered_nerfacto.cfg --scene_id 001_standing_coated
path_to_master = '/home/julius/Documents/Julius_03_x_auswertung/Julius_03_' 

for subsample in subsamples:
    for scene in scenes:

        cmd_train = f"python3 /home/julius/Downloads/3D-DAT-master/scripts/reconstruct.py -d {path_to_master}{subsample}/config_nerf_v2_centered_nerfacto.cfg --scene_id {scene}"
        #cmd_train = f"python3 /home/julius/Downloads/3D-DAT-master/scripts/reconstruct.py -d /home/julius/Documents/Julius_03_x_auswertung/Julius_03_10/config_nerf_v2_centered_nerfacto.cfg --scene_id {scene}"
        print(cmd_train)
        cmd_train = cmd_train.split()
        p = subprocess.Popen(cmd_train, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #flag = False
        #print("CHECK OUTPUT: ", subprocess.check_output(cmd_train, stderr=subprocess.STDOUT))
        for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):  # or another encoding
            if "Finished" in line:
                print(line)
        p.wait()
        p.kill()

    