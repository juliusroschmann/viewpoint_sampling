#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import os
import shutil
import fnmatch
import sys

path_to_master = '/home/julius/Documents/Julius_03'
path_to_scenes = path_to_master + '/scenes'


#df = pd.read_csv('/home/julius/Desktop/viewpoint_sampling/misc/groundtruth_handeye.txt', sep=" ", header=None)
df = pd.read_csv(path_to_scenes + '/001_standing_coated/groundtruth_handeye.txt', sep=" ", header=None)

df = df.drop(0, axis=1)
df.columns = ["x", "y", "z", "qx", "qy", "qz", "qw"]

# if (len(sys.argv)) <= 1:
#     samples = 1
# else:
#     samples = [int(sample) for sample in (sys.argv[1:])] 

# print((samples))
# print((sys.argv))

#sub_sample_list = np.arange(50, 424, 50, dtype=int).tolist()
#sub_sample_list = np.append(sub_sample_list, 424).tolist()
sub_sample_list = [300]


for sample in sub_sample_list:

    def fps(points, n_samples):
        """
        points: [N, 3] array containing the whole point cloud
        n_samples: samples you want in the sampled point cloud typically << N 
        """
        points = np.array(points)
        
        # Represent the points by their indices in points
        points_left = np.arange(len(points)) # [scipy_points]

        # Initialise an array for the sampled indices
        sample_inds = np.zeros(n_samples, dtype='int') # [S]

        # Initialise distances to inf
        dists = np.ones_like(points_left) * float('inf') # [scipy_points]

        # Select a point from points by its index, save it
        selected = 216
        sample_inds[0] = points_left[selected]

        # Delete selected 
        points_left = np.delete(points_left, selected) # [scipy_points - 1]

        # Iteratively select points for a maximum of n_samples
        for i in range(1, n_samples):
            # Find the distance to the last added point in selected
            # and all the others
            last_added = sample_inds[i-1]
            
            dist_to_last_added_point = (
                (points[last_added] - points[points_left])**2).sum(-1) # [scipy_points - i]

            # If closer, updated distances
            dists[points_left] = np.minimum(dist_to_last_added_point, 
                                            dists[points_left]) # [scipy_points - i]

            # We want to pick the one that has the largest nearest neighbour
            # distance to the sampled points
            selected = np.argmax(dists[points_left])
            sample_inds[i] = points_left[selected]

            # Update points_left
            points_left = np.delete(points_left, selected)

        return points[sample_inds]


    values = df[['x', 'y', 'z']].to_numpy()
    pnts = fps(values, sample)

    p = sample
    # N = 16000000

    # # Find a convex hull in O(N log N)
    # points = np.random.rand(N, 3)   # N random points in 3-D
    points = values
    # # Returned 420 points in testing
    # hull = ConvexHull(points)

    # # Extract the points forming the hull
    # hullpoints = points[hull.vertices,:]
    hullpoints = values
    # Naive way of finding the best pair in O(H^2) time if H is number of points on
    # hull
    hdist = cdist(hullpoints, hullpoints, metric='euclidean')
    # print(hdist)
    # print(hdist.shape)
    # Get the farthest apart points
    bestpair = np.unravel_index(hdist.argmax(), hdist.shape)

    #print(bestpair.shape)

    P = np.array([hullpoints[bestpair[0]],hullpoints[bestpair[1]]])

    #print("P:", P)
    # Now we have a problem
    #print("Finding optimal set...")
    while len(P)<p:
        #print("P size = {0}".format(len(P)))
        distance_to_P = cdist(points, P, metric='euclidean')
        #print("distance_to_P", distance_to_P)
        #print(distance_to_P.shape)
        minimum_to_each_of_P = np.min(distance_to_P, axis=1)
        best_new_point_idx   = np.argmax(minimum_to_each_of_P)
        best_new_point = np.expand_dims(points[best_new_point_idx,:],0)
        P = np.append(P,best_new_point,axis=0)


    rows_list = []
    idx_list = np.array([])

    for idx, subarr in enumerate(pnts):
        rows_list.append((df.loc[(df['x'] == subarr[0]) & (df['y'] == subarr[1]) & (df['z'] == subarr[2])]).values.flatten())
        idx_list = np.append(idx_list, ((df.index[(df['x'] == subarr[0]) & (df['y'] == subarr[1]) & (df['z'] == subarr[2])]).to_numpy())) 
        idx_list = idx_list.astype(int)
    new_df = pd.DataFrame(columns= df.columns, data=rows_list, index=idx_list)
    #print(new_df.head(100))

    subsample_indices = new_df.index.to_list()
    test_img_indices = list(set(range(1,425)) - set(subsample_indices))
  
    #subsample_image_names = [(str(item).zfill(6))+'.png' for item in subsample_indices]
    subsample_image_names = [(str(item).zfill(6))+'.png' for item in test_img_indices]

    dest = path_to_master + "_" + str(sample) + "/"

    os.makedirs(dest, exist_ok=True)
    shutil.copy2(path_to_master + "/config.cfg", dest)
    shutil.copytree(path_to_master + "/objects", dest+'/objects', dirs_exist_ok=True)

    for scene in sorted(os.listdir(path_to_scenes)):

        old_gt = path_to_scenes + "/" + scene + "/groundtruth_handeye.txt"
        new_gt = dest+"scenes/"+scene + "/groundtruth_handeye.txt"
        print(os.path.dirname(new_gt))
        os.makedirs(os.path.dirname(new_gt), exist_ok=True)
        old_assoc = path_to_scenes + "/" + scene + "/associations.txt"
        new_assoc = dest+"scenes/"+scene + "/associations.txt"
        print(os.path.dirname(new_assoc))
        os.makedirs(os.path.dirname(new_assoc), exist_ok=True)
        searchfile = None

        shutil.copy2(path_to_scenes + "/" + scene + "/camera_d435.yaml", dest+"scenes/"+scene + "/camera_d435.yaml")

        with open(old_gt,'r') as f:
            searchfile = f.readlines()
            f.close()
        with open(new_gt, "wt") as fout:
            for idx, _ in enumerate(searchfile):
                if idx in subsample_indices:
                    line = searchfile[idx-1]
                    fout.write(line)
        
        with open(old_assoc,'r') as f:
            searchfile = f.readlines()
            f.close()
        with open(new_assoc, "wt") as fout:
            for idx, _ in enumerate(searchfile):
                if idx in subsample_indices:
                    line = searchfile[idx-1]
                    fout.write(line)

    for root, dirs, files in os.walk(path_to_scenes):
        #print("root: ", root) 
        #print("dirname root: ", os.path.dirname(root) ) 


        # print("dirs: ", dirs)
        # print("files: ", files)
        # print("")

        for pattern in subsample_image_names:
            for filename in fnmatch.filter(files, pattern):
                #print("root: ", root)
                #print("dirs: ", dirs)
                #print("filename: ", filename)
                source = (os.path.join(root, filename))
                #print("source: ", source)
                destination = source.replace('03', '03_' + str(sample), 1)
                #print("destination: ", destination)
                destination = os.path.dirname(destination) 
                os.makedirs(destination, exist_ok=True)
                #print("destination: ", destination)
                if not os.path.exists(os.path.join(destination, filename)):
                    shutil.copy2(source, destination)
                    print("Copied {} from {} to {}".format(filename, source, destination))
                    # print("")

                else:
                    print("File {} already exists in {}".format(filename, destination))
            
        
    

    print("finished samplesize: ", sample)


