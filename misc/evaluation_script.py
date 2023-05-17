#!/usr/bin/env python3

import io
import signal
import subprocess
import shutil
import numpy as np
import os
import time
import fnmatch

# n_samples = np.arange(10, 70, 10, dtype=int)
# n_samples = np.append(n_samples, [80, 100, 200, 300]).tolist()
# n_samples = [str(sample) for sample in n_samples]
#print(n_samples)


#path_to_master = '/home/julius/Julius_03_x'

path_to_master = "/home/julius/Documents/Julius_03_x_auswertung"

# if not os.path.exists(path_to_master):
#     os.makedirs(path_to_master)

# def ig_f(dir, files):
#     return [f for f in files if os.path.isfile(os.path.join(dir, f))]

# shutil.copytree("/home/julius/Documents/Julius_03_x", path_to_master, ignore=ig_f, dirs_exist_ok=True)

# for root, dirs, files in os.walk(path_to_master):
#     for item in dirs:
        
#         if item == 'depth' or item == 'rgb':
#             print("Removing: ", os.path.join(root, item))
#             os.rmdir(os.path.join(root, item))



#methods = ["nerfacto", "instant-ngp","instant-ngp-bounded"]
methods = ["nerfacto", "instant-dex_nerf"]
sigma = 10
iterations = 20000
scenes = ['001_standing_coated',  '002_lying_coated',  '003_standing_liquid',  '004_lying_liquid', '005_standing_empty', '006_lying_empty']

path_to_scenes = sorted(os.listdir(path_to_master), key=lambda x: int(x.split('_')[2]))
path_to_scenes = [os.path.join(os.path.join(path_to_master, dir),"scenes") for dir in path_to_scenes]

eval_list = []
cmd_list = []
master_list = []


for path in path_to_scenes:
    for scene in scenes:
        path_to_one_scene = os.path.join(path, scene)
        #shutil.copy2("/home/julius/Documents/intrinsics.txt", path_to_one_scene)
        print("Now training for scene: {}.".format(path_to_one_scene))
        cmd_train = "ns-train nerfacto --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --max-num-iterations " + str(iterations) + " tracebot-data"" --data " + path_to_one_scene + " --data_eval /home/julius/Julius_03/scenes/001_standing_coated"
        #print(cmd_train)

        try:
            cmd_train = cmd_train.split()
            p = subprocess.Popen(cmd_train, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            #flag = False
            #print("CHECK OUTPUT: ", subprocess.check_output(cmd_train, stderr=subprocess.STDOUT))
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):  # or another encoding
                #print(line)
                if ".yml" in line:
                    print(line)
                    start_index = line.find("outputs")
                    end_index = line.find(".yml")
                    line = line[start_index:end_index] + ".yml"
                    cmd_eval = "ns-eval --load-config /home/julius/" + line #str(line.replace(" ", ""))
                    cmd_eval = cmd_eval.replace("\n", "")
                    print(cmd_eval)
                    #cmd_eval = cmd_eval.split()
                    eval_list.append(cmd_eval)
                    #flag = False
                
                # if "Saving config to:" in line:
                #     flag = True
                #     print(line)

                    # start_index = line.find("outputs")
                    # end_index = line.find("experiment")-1

                    # extracted_file_path = line[start_index:end_index]
                    # cmd_eval = "ns-eval --load-config /home/julius/" + extracted_file_path #str(line.replace(" ", ""))
                    # cmd_eval = cmd_eval.replace("\n", "")
                    # print(cmd_eval)
                    # #cmd_eval = cmd_eval.split()
                    # eval_list.append(cmd_eval)
                
                if "Training Finished" in line:
                    time.sleep(2)
                    p.send_signal(signal.SIGINT)
            
            p.wait()

        except subprocess.CalledProcessError:
            print("There was an error with command ____cmd_train____ exited with non-zero code!")

    
        print("Finished nerfacto for scene: {}.".format(path_to_one_scene))
        print("")
        p.kill()

print("")
print("")
print("")
print("----------Finished training----------")

print("Eval List: ", eval_list)
print("")
print("Cmd List: ", cmd_list)
print("")
master_list = list(zip(eval_list, cmd_list))
print("Master List: ", master_list)

