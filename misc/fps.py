# %%
#!/usr/bin/env python3


import numpy as np
import pandas as pd
import torch
from dgl.geometry import farthest_point_sampler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# %%
df = pd.read_csv('/home/julius/Desktop/viewpoint_sampling/misc/poses_6d.csv')
#print(df.head())

min = df['z'].abs().max()
min_idx = df.index[df['z'] == min]
print(min)
print(min_idx.tolist())
print(df.loc[min_idx.tolist()])

# %%
x = torch.from_numpy(df.values)
x = x.unsqueeze(0) 
# print(x.shape)
# print(type(x[0]))

# print(x.shape)
# y = torch.rand((2, 10, 3))
# print(y)
# print(y.shape)
point_idx = farthest_point_sampler(x, 5)#, start_idx=0)
point_idx = point_idx.flatten().tolist()
print(point_idx)

farthest_points = df.loc[point_idx]
#farthest_points.sample(2)
print(farthest_points['x'].values)


# %%
def fps(points, n_samples):
    """
    points: [N, 3] array containing the whole point cloud
    n_samples: samples you want in the sampled point cloud typically << N 
    """
    points = np.array(points)
    
    # Represent the points by their indices in points
    points_left = np.arange(len(points)) # [P]

    # Initialise an array for the sampled indices
    sample_inds = np.zeros(n_samples, dtype='int') # [S]

    # Initialise distances to inf
    dists = np.ones_like(points_left) * float('inf') # [P]

    # Select a point from points by its index, save it
    selected = 100
    sample_inds[0] = points_left[selected]

    # Delete selected 
    points_left = np.delete(points_left, selected) # [P - 1]

    # Iteratively select points for a maximum of n_samples
    for i in range(1, n_samples):
        # Find the distance to the last added point in selected
        # and all the others
        last_added = sample_inds[i-1]
        
        dist_to_last_added_point = (
            (points[last_added] - points[points_left])**2).sum(-1) # [P - i]

        # If closer, updated distances
        dists[points_left] = np.minimum(dist_to_last_added_point, 
                                        dists[points_left]) # [P - i]

        # We want to pick the one that has the largest nearest neighbour
        # distance to the sampled points
        selected = np.argmax(dists[points_left])
        sample_inds[i] = points_left[selected]

        # Update points_left
        points_left = np.delete(points_left, selected)

    return points[sample_inds]


# %%
values = df[['x', 'y', 'z']].to_numpy()
print(values)

pnts = fps(values, 5)
print(pnts)

# %%
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(projection='3d')

ax.scatter(df['x'].values, df['y'].values, df['z'].values,  color='r', s=3, marker='X')
ax.plot(farthest_points['x'].values, farthest_points['y'].values, farthest_points['z'].values, marker='o', markersize=10, color='green')
ax.plot(pnts[:,0], pnts[:,1], pnts[:,2], marker='o', markersize=10, color='black')


#ax.plot(total_points[:, 0], total_points[:, 1], total_points[:, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()


