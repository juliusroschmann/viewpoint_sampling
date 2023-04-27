#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import shutil
import fnmatch
import sys

df = pd.read_csv('/home/julius/Desktop/viewpoint_sampling/misc/poses_6d.csv')

if (len(sys.argv)) <= 1:
    samples = 1
else:
    samples = [int(sample) for sample in (sys.argv[1:])] 

print((samples))
print((sys.argv))

for sample in samples:

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
    new_df.head(100)



    subsample_indices = new_df.index.to_list()
    subsample_indices = [(str(item).zfill(6))+'.png' for item in subsample_indices]

    dest = "/home/julius/Documents/" + "dataset_" + str(sample) + "/"
    os.makedirs(dest, exist_ok=True)

    for root, dirs, files in os.walk("/home/julius/Documents/dataset_424/scenes"):
        # print("root: ", root)
        # print("dirs: ", dirs)
        # print("files: ", files)
        # print("")
        for pattern in subsample_indices:
            for filename in fnmatch.filter(files, pattern):
                #print(filename)
                source = (os.path.join(root, filename))
                #print(source)
                destination = source.replace('424', str(sample))
                #print(destination)
                destination = os.path.dirname(destination) 
                os.makedirs(destination, exist_ok=True)
                #print(destination)
                if not os.path.exists(os.path.join(destination, filename)):
                    shutil.copy2(source, destination)
                    # print("Copied {} from {} to {}".format(filename, source, destination))
                    # print("")

                else:
                    print("File {} already exists in {}".format(filename, destination))

    shutil.copy2("/home/julius/Documents/dataset_424/config.cfg", dest)
    shutil.copytree("/home/julius/Documents/dataset_424/objects", dest+'/objects', dirs_exist_ok=True)

    print("finished samplesize: ", sample)


