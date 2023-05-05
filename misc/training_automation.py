#!/usr/bin/env python3

import io
import signal
import subprocess
import numpy as np
import os
import time

n_samples = np.arange(50, 424, 50, dtype=int)
n_samples = np.append(n_samples, 424).tolist()
n_samples = [str(sample) for sample in n_samples]
print(n_samples)

methods = ["nerfacto", "instant-ngp","instant-ngp-bounded"]
#methods = ["instant-ngp"]
sigma = 15


scenes = sorted([f.name for f in os.scandir("/home/julius/Julius_03_960x540/scenes") if f.is_dir()])

print(scenes)

#scenes = ["001_standing_coated_960x540", "002_lying_coated_960x540"]
#scenes = ["002_lying_coated_960x540"]

#cmd_train = "ns-train " + methods[0] + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --data /home/julius/Julius_03_960x540/scenes/" + scenes[0] + " tracebot-data"
#cmd_eval = "ns-eval --load-config /home/julius/outputs/" + scenes[0] + "/" + methods[0] + "/_____INSERT_FOLDER_HERE______/config.yml" 
#print(cmd_eval)

eval_list = []

for scene in scenes:
    for method in methods:
        if method == "nerfacto":
            iterations = 5000
        else:
            iterations = 10000
        cmd_train = "ns-train " + method + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --max-num-iterations " + str(iterations) + " --data /home/julius/Julius_03_960x540/scenes/" + scene + " tracebot-data"
        print(cmd_train)
        #cmd_eval = "ns-eval --load-config /home/julius/outputs/" + scene + "/" + method 
        cmd_train = cmd_train.split()

        try:
            #subprocess.check_call(cmd_train, cwd=os.getcwd())
            print("Trying to run: ", cmd_train)
            p = subprocess.Popen(cmd_train, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            flag = False
            #print("CHECK OUTPUT: ", subprocess.check_output(cmd_train, stderr=subprocess.STDOUT))
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):  # or another encoding
                #print(line)
                if flag == True:
                    # print("----------------------------------------------------------------")
                    # print(line)
                    # print("----------------------------------------------------------------")
                    # print("")
                    print(line)
                    cmd_eval = "ns-eval --load-config /home/julius/" + str(line.replace(" ", ""))
                    cmd_eval = cmd_eval.replace("\n", "")
                    #cmd_eval = cmd_eval.split()
                    eval_list.append(cmd_eval)
                    flag = False
                
                if "Saving config to:" in line:
                    flag = True
                   
                if "Training Finished" in line:
                    time.sleep(2)
                    p.send_signal(signal.SIGINT)
            
            p.wait()
            # print("")
            # print("----------------------------------SUCCESS")
            # print("")
            # p.send_signal(signal.SIGINT)
        except subprocess.CalledProcessError:
            print("There was an error with command ____cmd_train____ exited with non-zero code!")

        print("")
        print("Now training next scene.")
        print("")
        p.kill()
print("")
print("")
print("")
print("----------Finished training----------")
print("Eval List: ", eval_list)

# p1 =  subprocess.Popen(eval_list[0], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# p2 =  subprocess.Popen(eval_list[1], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# print("Output from process 2: " + (p2.communicate()[0]).decode())
# print("")
# for line in io.TextIOWrapper(p2.stdout, encoding="utf-8"):  # or another encoding
#         print(line)

#procs = [ subprocess.Popen(i, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in eval_list]

# for idx, p in enumerate(procs):
    
#     for line in io.TextIOWrapper(p2.stdout, encoding="utf-8"):  # or another encoding
#         print(line)
#         break
    
#     #print(s_out)
#     print("trying to print s_out")
#     p.wait()
#     print("finished waiting")
#     p.kill()


    
# for item in eval_list:
#     item = item.split()
#     print("Item: ", item)
#     try:
#         p = subprocess.Popen(item, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#         p.wait()
#         print("Waiting for subprocess!")
#     except subprocess.CalledProcessError:
#         print("There was an error with command ____cmd_eval____ exited with non-zero code!")


# for scene in scenes:
#     for method in methods:
#         # path = "/home/julius/outputs/" + scene + "/" + method 
#         # print("Path:", path)
#         # print("Globbing: ", [f.path for f in os.scandir(path) if f.is_dir()])
#         # cmd_eval = "ns-eval --load-config" + max([f.path for f in os.scandir(path) if f.is_dir() ], key=os.path.getmtime) + "/config.yml"
#         # cmd_eval = cmd_eval.split()

#         # try:
#         #     #subprocess.check_call(cmd_eval, cwd=os.getcwd())
#         #     print("Trying to run: ", cmd_eval)
#         #     p = subprocess.Popen(cmd_eval, stdin=subprocess.PIPE, stdout=subprocess.PIPE) 
#         #     print("")
#         #     print("----------------------------------SUCCESS")
#         #     print("")
#         #     p.send_signal(signal.SIGINT)
#         # except subprocess.CalledProcessError:
#         #     print("There was an error with command ____cmd_eval____ exited with non-zero code!")
       
#         # p.kill()

#         #/home/julius/Julius_03_960x540/scenes/001_standing_coated_960x540
#         #scp -r julius@192.168.141.40:/home/julius/Julius_03_960x540/scenes/001_standing_coated_960x540/depth_nerf /home/julius/Documents/auswertung_03/001_standing_coated_960x540/instant-ngp/depth_nerf
#         copy_cmd = "scp -r julius@192.168.141.40:/home/julius/Julius_03_960x540/scenes/" + scene + "/depth_nerf"
#         copy_cmd = copy_cmd.split()


#ns-train instant-ngp --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh 15 --data /home/julius/Julius_03_960x540/scenes/001_standing_coated_960x540 tracebot-data --viewer.websocket-port 7008
#ns-train instant-ngp --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh 15 --data /home/julius/Julius_03_960x540/scenes/002_lying_coated_960x540 tracebot-data