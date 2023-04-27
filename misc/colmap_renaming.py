#!/usr/bin/env python3
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# pwd = "/home/julius/Documents/sparse/0/images_working.txt"
# filename = "/home/julius/Documents/sparse/0/groundtruth_handeye.txt"

pwd = "/home/julius/Documents/dataset_424/scenes/006_standing_coated_original/images_manip.txt"
filename = "/home/julius/Documents/dataset_424/scenes/006_standing_coated_original/groundtruth_handeye.txt"

# Image list with two lines of data per image:
#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
#   POINTS2D[] as (X, Y, POINT3D_ID)
# Number of images: 93, mean observations per image: 429.88172043010752

file = []
#associations
with open(pwd, "rt") as fin:
    with open(filename, "wt") as fout:
        for idx, line in enumerate(fin):
            if idx % 2 == 0:
                line = line.split()
                print(line)
                idx = line[-1].lstrip("0")
                idx = idx.rstrip(".png")
                reord_line = [idx] + line[5:8] + line[2:5] + line[1:2]
                print(reord_line)
                print("")
                file.append(reord_line)
        
        file.sort(key=lambda x: int(x[0])) 
        wr = csv.writer(fout, delimiter=' ')
        wr.writerows(file)
      
print(file[:, 1])
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(projection='3d')

ax.scatter(file[:][1], file[:][2], file[:][3],  color='r', s=3, marker='X')
#ax.plot(farthest_points['x'].values, farthest_points['y'].values, farthest_points['z'].values, marker='o', markersize=5, color='black', label='Torch-Method')
#ax.scatter(P[:,0], P[:,1], P[:,2], marker='X', s=40, color='green', label='Scipy-Method')

#ax.plot(total_points[:, 0], total_points[:, 1], total_points[:, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
#ax.legend()
ax.set_title("Farthest Point Sampling of Viewing Hemisphere")
plt.show()