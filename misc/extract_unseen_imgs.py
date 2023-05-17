#!/usr/bin/env python3
import fnmatch
import os
import numpy as np

subsample_indices_300 = [216, 375, 72, 269, 163, 318, 16, 218, 115, 377, 423, 118, 271, 221, 66, 165, 330, 37, 310, 400, 77, 298, 358, 246, 178, 146, 4, 122, 248, 193, 50, 100, 399, 343, 371, 198, 20, 300, 415, 274, 249, 247, 205, 141, 61, 379, 332, 54, 86, 185, 356, 144, 161, 44, 89, 295, 227, 278, 273, 313, 68, 7, 373, 126, 158, 32, 130, 71, 207, 102, 96, 2, 345, 19, 285, 133, 155, 369, 25, 351, 191, 316, 229, 117, 57, 412, 206, 416, 173, 38, 397, 398, 259, 385, 323, 236, 116, 177, 389, 315, 326, 98, 262, 364, 136, 270, 348, 281, 296, 84, 421, 263, 152, 204, 90, 60, 334, 280, 219, 228, 92, 342, 48, 294, 222, 78, 340, 314, 306, 360, 128, 59, 10, 372, 148, 363, 251, 288, 284, 388, 287, 15, 176, 151, 76, 1, 272,
                         282, 119, 11, 265, 233, 58, 346, 69, 134, 85, 304, 209, 153, 170, 382, 139, 210, 167, 277, 147, 417, 31, 384, 169, 199, 35, 260, 366, 422, 82, 292, 42, 172, 243, 67, 65, 181, 101, 223, 160, 6, 256, 291, 299, 418, 226, 406, 211, 73, 337, 95, 350, 381, 232, 303, 361, 331, 39, 70, 283, 55, 26, 110, 374, 135, 267, 322, 80, 62, 390, 74, 286, 162, 293, 149, 24, 241, 104, 28, 138, 159, 94, 393, 200, 75, 220, 401, 143, 81, 338, 53, 347, 188, 194, 357, 279, 9, 411, 362, 145, 91, 132, 244, 290, 45, 215, 51, 355, 208, 5, 404, 240, 192, 150, 190, 289, 142, 297, 8, 266, 367, 238, 83, 405, 21, 344, 354, 275, 164, 129, 14, 231, 407, 52, 394, 63, 88, 312, 40, 352, 378, 365, 180, 359, 109, 154, 370, 264, 321, 175, 29, 184, 237]

full_indices = np.arange(1,425).tolist()

unseen_indices = list(set(full_indices) - set(subsample_indices_300))
unseen_image_names = [(str(item).zfill(6))+'.png' for item in unseen_indices]

path_to_scenes = "/home/julius/Documents/Julius_03_x_auswertung"

for root, dirs, files in os.walk(path_to_scenes):
        #print("root: ", root) 
        #print("dirname root: ", os.path.dirname(root) ) 


        # print("dirs: ", dirs)
        # print("files: ", files)
        # print("")

        for pattern in unseen_image_names:
            for filename in fnmatch.filter(files, pattern):
                #print("root: ", root)
                #print("dirs: ", dirs)
                #print("filename: ", filename)
                source = (os.path.join(root, filename))
                print("source: ", source)
                
                
                # destination = source.replace('03', '03_' + str(sample), 1)
                # #print("destination: ", destination)
                # destination = os.path.dirname(destination) 
                # os.makedirs(destination, exist_ok=True)
                # #print("destination: ", destination)
                # if not os.path.exists(os.path.join(destination, filename)):
                #     shutil.copy2(source, destination)
                #     print("Copied {} from {} to {}".format(filename, source, destination))
                #     # print("")

                # else:
                #     print("File {} already exists in {}".format(filename, destination))