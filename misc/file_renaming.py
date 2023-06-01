

pwd = "/home/julius/Documents/Julius_03_depth_masks/006_lying_empty/"
old_file = pwd + "associations_cut.txt"

new_file = pwd + "associations_new.txt"
#pwd += filename

index = 85

##groundtruth
# with open(old_file, "rt") as fin:
#     with open(new_file, "wt") as fout:
#         for idx, line in enumerate(fin):
#             print(line)
#             fout.write(line.replace(str(idx+1), str(idx+index), 1))

##associations
# with open(old_file, "rt") as fin:
#     with open(new_file, "wt") as fout:
#         for idx, line in enumerate(fin):
#             print(line)
#             line = line.replace(str(idx+1)+" ", str(idx+index)+" ")
#             fout.write(line.replace(str(idx+1).zfill(6), str(idx+index).zfill(6)))


#image renaming
# import os
# import shutil

# for i, file in enumerate(sorted(os.listdir(pwd))):
#     print(len(os.listdir(pwd)))
#     print("renaming: {} to: {}".format(pwd + file,  pwd + "depth_" + str(i+1).zfill(6) + ".png"))
#     #print("New: ", str(i+index).zfill(6) + ".png")
#     os.rename(pwd + file, pwd + "depth_" + str(i+1).zfill(6) + ".png")
#     #shutil.copy(pwd + file,  "/home/julius/Documents/Julius_03/scenes/test_004/depth/" + str(i+index).zfill(6) + ".png")


import os
import json

path = "/home/julius/Documents/Julius_03_x_auswertung"

# this is the extension you want to detect
extension = 'transforms.json'
all_files = []
for root, dirs_list, files_list in os.walk(path):
    for file_name in files_list:
        if extension in file_name:
            file_name_path = os.path.join(root, file_name)

with open('filename.json') as f:
    data = json.load(f)
    data['offset'] = [0.25, 0.25, 0.25]

with open('filename.json', 'w') as f2:
    json.dump(data, f2)