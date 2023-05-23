#!/usr/bin/env python3

import io
import signal
import subprocess
import shutil
import numpy as np
import os
import time

n_samples = np.arange(50, 424, 50, dtype=int)
n_samples = np.append(n_samples, 424).tolist()
n_samples = [str(sample) for sample in n_samples]

path_to_master = '/home/julius/Documents/Julius_03_50'
path_to_scenes = path_to_master + '/scenes'

methods = ["nerfacto", "instant-ngp","instant-ngp-bounded"]
#methods = ["instant-dex_nerf"]
sigma = 10
#iterations = 100000

# scenes = sorted([f.name for f in os.scandir("/home/julius/Julius_03_960x540/scenes") if f.is_dir()])
# print(scenes)

#scenes = ['001_standing_coated_960x540',  '002_lying_coated_960x540',  '003_standing_liquid_960x540',  '004_lying_liquid_960x540', '005_standing_empty_960x540', '006_lying_empty_960x540']
scenes = ['001_standing_coated',  '002_lying_coated',  '003_standing_liquid',  '004_lying_liquid', '005_standing_empty', '006_lying_empty']
#scenes = ['005_standing_empty']



# for scene in scenes:
#     for method in methods:
#         if method == "nerfacto":
#             iterations = 5000
#         else:
#             iterations = 10000

#         path1 = '/home/julius/Documents/Julius_03_auswertung/scenes/' + str(scene) + "/" + str(method) + "/depth_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations)#the path where to save resized images
#         #path2 = '/home/julius/Documents/Julius_03_auswertung/scenes/' + str(scene) + "/" + str(method) + "/depth_norm_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations)#the path where to save resized images
#         #path3 = '/home/julius/Documents/Julius_03_auswertung/scenes/' + str(scene) + "/" + str(method) + "/rgb_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations) #the path where to save resized images

#         # create new folder
#         if not os.path.exists(path1):
#             #print(path1)
#             os.makedirs(path1, exist_ok=False)

#         # if not os.path.exists(path2):
#         #     #print(path2)
#         #     os.makedirs(path2, exist_ok=False)

#         # if not os.path.exists(path3):
#         #     #print(path3)
#         #     os.makedirs(path3, exist_ok=False)

#         #cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_nerf " + path1
#         cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_instant-dex_nerf " + path1
#         print(cmd1)
        
        #cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_nerf /home/julius/Documents/" + str(scene) + "/" + str(method) + "/depth_nerf_sigma15"
        #cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/005_standing_empty/depth_nerf /home/julius/Documents/Julius_03_auswertung/scenes/005_standing_empty/instant-ngp/depth_nerf_sigma15"
        # cmd1 = cmd1.split()
        # cmd2 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_norm_nerf " + path2
        # cmd2 = cmd2.split()
        # cmd3 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/rgb_nerf " + path3
        # cmd3 = cmd3.split()

#         p1 = subprocess.Popen(cmd1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
#         p1.wait()
#         p2 = subprocess.Popen(cmd2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
#         p2.wait()
#         p3 = subprocess.Popen(cmd3, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
#         p3.wait()
#         print(cmd1)
#         print(cmd2)
#         print(cmd3)
#         print("")
#         p1.kill()
#         p2.kill()
#         p3.kill()


eval_list = []
cmd_list = []
master_list = []

for scene in scenes:
    for method in methods:
        print("Now training method: {} for scene: {}.".format(method, scene))

        if method == "nerfacto":
            iterations = 5000
        else:
            iterations = 10000
        path1 = '/home/julius/Documents/Julius_03_auswertung/scenes/' + str(scene) + "/" + str(method) + "/depth_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations)#the path where to save resized images
        path2 = '/home/julius/Documents/Julius_03_auswertung/scenes/' + str(scene) + "/" + str(method) + "/depth_norm_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations)#the path where to save resized images
        path3 = '/home/julius/Documents/Julius_03_auswertung/scenes/' + str(scene) + "/" + str(method) + "/rgb_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations) #the path where to save resized images

        # # create new folder
        # if not os.path.exists(path1):
        #     #print(path1)
        #     os.makedirs(path1, exist_ok=False)

        # if not os.path.exists(path2):
        #     #print(path2)
        #     os.makedirs(path2, exist_ok=False)

        # if not os.path.exists(path3):
        #     #print(path3)
        #     os.makedirs(path3, exist_ok=False)

        cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_nerf " + path1
        #cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_nerf /home/julius/Documents/" + str(scene) + "/" + str(method) + "/depth_nerf_sigma15"
        #cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/005_standing_empty/depth_nerf /home/julius/Documents/Julius_03_auswertung/scenes/005_standing_empty/instant-ngp/depth_nerf_sigma15"
        #cmd1 = cmd1.split()
        cmd2 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_norm_nerf " + path2
        #cmd2 = cmd2.split()
        cmd3 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/rgb_nerf " + path3
        #cmd3 = cmd3.split()
        cmd_list.append(cmd1)
        cmd_list.append(cmd2)
        cmd_list.append(cmd3)

        #cmd_train = "ns-train " + method + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --max-num-iterations " + str(iterations) + " --data /home/julius/005_standing_empty" +" tracebot-data"
        cmd_train = "ns-train " + method + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --max-num-iterations " + str(iterations) + " --data /home/julius/Julius_03/scenes/" + scene + " tracebot-data"
        #print(cmd_train)
        #cmd_eval = "ns-eval --load-config /home/julius/outputs/" + scene + "/" + method 
        

        try:
            #subprocess.check_call(cmd_train, cwd=os.getcwd())
            print("Trying to run: ", cmd_train)
            cmd_train = cmd_train.split()
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
                    # print(line)

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

    
        print("Finished method: {} for scene: {}.".format(method, scene))
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