

pwd = "/home/julius/Documents/Julius_03/scenes/004_lying_liquid_84+/depth/"
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
import os
import shutil

for i, file in enumerate(sorted(os.listdir(pwd))):
    print(len(os.listdir(pwd)))
    print("renaming: {} to: {}".format(pwd + file,  pwd + str(i+index).zfill(6) + ".png"))
    #print("New: ", str(i+index).zfill(6) + ".png")
    #os.rename(pwd + file, pwd + str(i+index).zfill(6) + ".png")
    shutil.copy(pwd + file,  "/home/julius/Documents/Julius_03/scenes/test_004/depth/" + str(i+index).zfill(6) + ".png")

