

pwd = "/home/administrator/Documents/recordings/Julius/scenes/002_lying_liquid_plus/rgb/"

# filename = "associations.txt"
# pwd += filename

#groundtruth
# with open(pwd, "rt") as fin:
#     with open(filename, "wt") as fout:
#         for idx, line in enumerate(fin):
#             print(line)
#             fout.write(line.replace(str(idx+1), str(idx+339), 1))

#associations
# with open(pwd, "rt") as fin:
#     with open(filename, "wt") as fout:
#         for idx, line in enumerate(fin):
#             print(line)
#             line = line.replace(str(idx+1)+" ", str(idx+339)+" ")
#             fout.write(line.replace(str(idx+1).zfill(6), str(idx+339).zfill(6)))


#image renaming
import os

for i, filename in enumerate(sorted(os.listdir(pwd))):
    print(filename)
    os.rename(pwd + filename, pwd + str(i+339).zfill(6) + ".png")

