#!/usr/bin/env python3

import numpy as np
import pandas as pd
import torch
from dgl.geometry import farthest_point_sampler

if torch.cuda.is_available():
    print('We have a GPU!')
else:
    print('Sorry, CPU only.')

df = pd.read_csv('poses_6d.csv')
#print(df.head())

min = df['z'].abs().max()
min_idx = df.index[df['z'] == min]
print(min)
print(min_idx.tolist())
print(df.loc[min_idx.tolist()])

#print(df.info())
#print(type(df.values))
#print(df.values)
#a=np.vstack(df['Point'].values).astype(np.float32)
#print(a)
#x = torch.rand((2, 10, 3))

x = torch.from_numpy(df.values)
x = x.unsqueeze(0) 
# print(x.shape)
# print(type(x[0]))

# print(x.shape)
# y = torch.rand((2, 10, 3))
# print(y)
# print(y.shape)
point_idx = farthest_point_sampler(x, 2)#, start_idx=0)
point_idx = point_idx.flatten().tolist()
print(point_idx)

farthest_points = df.loc[point_idx]
print(farthest_points)
