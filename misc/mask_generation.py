#!/usr/bin/env python3

methods = ["nerfacto", "instant-ngp","instant-ngp-bounded"]
scenes = ['001_standing_coated',  '002_lying_coated',  '003_standing_liquid',  '004_lying_liquid', '005_standing_empty', '006_lying_empty']
sigma = 10

#/home/julius/3D-DAT-master/scripts/vis_masks.py
#python3 /home/julius/3D-DAT-master/scripts/vis_masks.py -c /home/julius/Julius_03/config.cfg -s "001_standing_coated" -o /home/julius/masks/001_standing_coated_masks




for scene in scenes:
    for method in methods:
        #print("Now training method: {} for scene: {}.".format(method, scene))

        if method == "nerfacto":
            iterations = 5000
        else:
            iterations = 10000
        path1 = '/home/julius/masks/' + str(scene) + "/" + str(method) + "/depth_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations)#the path where to save resized images
        path2 = '/home/julius/masks/' + str(scene) + "/" + str(method) + "/depth_norm_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations)#the path where to save resized images
        path3 = '/home/julius/masks/' + str(scene) + "/" + str(method) + "/rgb_nerf_sigma_" + str(sigma) + "_iter_" + str(iterations) #the path where to save resized images

        print(path1)
        print(path2)
        print(path3)
        print("")
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

        # cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_nerf " + path1
        # #cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_nerf /home/julius/Documents/" + str(scene) + "/" + str(method) + "/depth_nerf_sigma15"
        # #cmd1 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/005_standing_empty/depth_nerf /home/julius/Documents/Julius_03_auswertung/scenes/005_standing_empty/instant-ngp/depth_nerf_sigma15"
        # #cmd1 = cmd1.split()
        # cmd2 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/depth_norm_nerf " + path2
        # #cmd2 = cmd2.split()
        # cmd3 = "scp -r julius@192.168.141.40:/home/julius/Julius_03/scenes/" + str(scene) + "/rgb_nerf " + path3
        # #cmd3 = cmd3.split()
        # cmd_list.append(cmd1)
        # cmd_list.append(cmd2)
        # cmd_list.append(cmd3)

        # #cmd_train = "ns-train " + method + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --max-num-iterations " + str(iterations) + " --data /home/julius/005_standing_empty" +" tracebot-data"
        # cmd_train = "ns-train " + method + " --pipeline.model.depth-render-method dex-nerf --pipeline.model.sigma_thresh " + str(sigma) + " --max-num-iterations " + str(iterations) + " --data /home/julius/Julius_03/scenes/" + scene + " tracebot-data"
        # #print(cmd_train)
        # #cmd_eval = "ns-eval --load-config /home/julius/outputs/" + scene + "/" + method 
        

        # try:
        #     #subprocess.check_call(cmd_train, cwd=os.getcwd())
        #     print("Trying to run: ", cmd_train)
        #     cmd_train = cmd_train.split()
        #     p = subprocess.Popen(cmd_train, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #     flag = False
        #     #print("CHECK OUTPUT: ", subprocess.check_output(cmd_train, stderr=subprocess.STDOUT))
        #     for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):  # or another encoding
        #         #print(line)
        #         if flag == True:
        #             # print("----------------------------------------------------------------")
        #             # print(line)
        #             # print("----------------------------------------------------------------")
        #             # print("")
        #             print(line)
        #             cmd_eval = "ns-eval --load-config /home/julius/" + str(line.replace(" ", ""))
        #             cmd_eval = cmd_eval.replace("\n", "")
        #             #cmd_eval = cmd_eval.split()
        #             eval_list.append(cmd_eval)
        #             flag = False
                
        #         if "Saving config to:" in line:
        #             flag = True
        #             # print(line)

        #             # start_index = line.find("outputs")
        #             # end_index = line.find("experiment")-1

        #             # extracted_file_path = line[start_index:end_index]
        #             # cmd_eval = "ns-eval --load-config /home/julius/" + extracted_file_path #str(line.replace(" ", ""))
        #             # cmd_eval = cmd_eval.replace("\n", "")
        #             # print(cmd_eval)
        #             # #cmd_eval = cmd_eval.split()
        #             # eval_list.append(cmd_eval)
                   
        #         if "Training Finished" in line:
        #             time.sleep(2)
        #             p.send_signal(signal.SIGINT)
            
        #     p.wait()

        # except subprocess.CalledProcessError:
        #     print("There was an error with command ____cmd_train____ exited with non-zero code!")

    
        # print("Finished method: {} for scene: {}.".format(method, scene))
        # print("")
        # p.kill()