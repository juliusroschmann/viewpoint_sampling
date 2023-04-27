#!/usr/bin/env python3

#import fps
import glob
import subprocess
import numpy as np
import os
import pathlib

n_samples = np.arange(1, 424, 50, dtype=int)
n_samples = np.append(n_samples, 424).tolist()
n_samples = [str(sample) for sample in n_samples]
print(n_samples)

#subprocess.Popen(["python3", "fps.py"] + list(n_samples), capture_output=True)

# for simple commands
try:
    success = subprocess.run(["ls", "-l", "/gki,"], check=True, capture_output=True) 
    if success.returncode==0:
        print("")
        print("SUCCESS")
    else:
        print("")
        print("FAILED")
except Exception as e:
    print("EXCEPTION: ", e) 


# for complex commands, with many args, use string + `shell=True`:
# cmd_str = "ls -l /tmp | awk '{print $3,$9}' | grep root"
# subprocess.run(cmd_str, shell=True)


methods = ["nerfacto", "instant-ngp-bounded"]
sigma = 15
scenes = ["001_standing_liquid", "002_lying_liquid", "003_standing_empty", "005_lying_empty", "006_standing_coated", "007_lying_coated"]

cmd_train = "ns-train " + methods[0] + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --data /home/julius/nerfstudio-tracebot/data/Julius/scenes/" + scenes[0] + " tracebot-data"
cmd_eval = "ns-eval --load-config /home/julius/outputs/" + scenes[0] + "/" + methods[0] + "/2023-04-17_145315/config.yml" 
print(cmd_eval)

for method in methods:
    for scene in scenes:
        cmd_train = "ns-train " + method + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --data /home/julius/nerfstudio-tracebot/data/Julius/scenes/" + scene + " tracebot-data"
        #cmd_eval = "ns-eval --load-config /home/julius/outputs/" + scene + "/" + method + "/"
        cmd_eval = "~/Desktop"
        #print(pathlib.Path(cmd_eval).glob('*/'))
        print(sorted(glob.glob(os.path.join(cmd_eval, '*/')), key=os.path.getmtime))
        
        folder = max(pathlib.Path(cmd_eval).glob('*/'), key=os.path.getmtime)
        cmd_eval = "ns-eval --load-config /home/julius/outputs/" + scene + "/" + method + "/" + folder + "/config.yml" 

        print(cmd_train)
        print(pathlib.Path(cmd_eval).glob('*/'))
        print("")

# "ns-train nerfacto --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh 15 --data /home/julius/nerfstudio-tracebot/data/Julius/scenes/003_standing_empty tracebot-data"
# "ns-eval --load-config /home/julius/outputs/003_standing_empty/nerfacto/2023-04-17_145315/config.yml" 

# "ns-train nerfacto --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh 15 --data /home/julius/nerfstudio-tracebot/data/Julius/scenes/003_standing_empty tracebot-data --downscale_factor 2"
# "ns-eval --load-config ~/outputs/003_standing_empty/nerfacto/2023-04-18_094805/config.yml"

# "ns-train nerfacto --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh 15 --data /home/julius/nerfstudio-tracebot/data/Julius/scenes/003_standing_empty tracebot-data --downscale_factor 4"
# "ns-eval --load-config ~/outputs/003_standing_empty/nerfacto/2023-04-18_100338/config.yml"