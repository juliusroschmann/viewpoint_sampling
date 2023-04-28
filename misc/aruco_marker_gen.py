#!/usr/bin/env python3

import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd


aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000) #aruco.Dictionary_get(aruco.DICT_5X5_250)

fig = plt.figure()
nx = 20
ny = 20
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict,i, 1000)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")

#plt.savefig("_data/markers.pdf")
plt.show()