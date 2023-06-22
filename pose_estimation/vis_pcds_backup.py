import open3d as o3d
import numpy as np
import os

folder1 = "/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/"

icp_canister = []
icp_large_bottle = []
icp_medium_bottle = []
icp_small_bottle = []

transf_canister = []
transf_large_bottle = []
transf_medium_bottle = []
transf_small_bottle = []

object_pcd = []
plane_pcd = []

for pcd in sorted(os.listdir(folder1)):
    
    if "icp_101_canister_full_small" in pcd:
        icp_canister.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
    elif "icp_102_LargeRinseFluidA_Bottle" in pcd:
        icp_large_bottle.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
    elif "icp_103_MediumRinseFluidK_Bottle" in pcd:
        icp_medium_bottle.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
    elif "icp_104_SmallSoyBroth_Bottle" in pcd:
        icp_small_bottle.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))


    elif "transf_101_canister_full_small" in pcd:
        transf_canister.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
    elif "transf_102_LargeRinseFluidA_Bottle" in pcd:
        transf_large_bottle.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
    elif "transf_103_MediumRinseFluidK_Bottle" in pcd:
        transf_medium_bottle.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
    elif "transf_104_SmallSoyBroth_Bottle" in pcd:
        transf_small_bottle.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))


    elif "object_pcd" in pcd:
        object_pcd.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
    elif "plane_pcd" in pcd:
        plane_pcd.append(o3d.io.read_point_cloud(os.path.join(folder1, pcd)))
  

# idx = 3
# o3d.visualization.draw_geometries([object_pcd[idx], icp_canister[idx], icp_small_bottle[idx], icp_medium_bottle[idx], icp_large_bottle[idx]])

for idx in range(len(object_pcd)):
    o3d.visualization.draw_geometries([object_pcd[idx], icp_canister[idx], icp_small_bottle[idx], icp_medium_bottle[idx], icp_large_bottle[idx]])



# vis = o3d.visualization.Visualizer()
# vis.create_window()
# vis.add_geometry(object_pcd[0])
# vis.add_geometry(icp_canister[0])
# vis.add_geometry(icp_small_bottle[0])
# vis.add_geometry(icp_medium_bottle[0])
# vis.add_geometry(icp_large_bottle[0])
# vis.update_geometry(object_pcd[0])
# vis.update_geometry(icp_canister[0])
# vis.update_geometry(icp_small_bottle[0])
# vis.update_geometry(icp_medium_bottle[0])
# vis.update_geometry(icp_large_bottle[0])
# vis.poll_events()
# vis.update_renderer()
#vis.capture_screen_image("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/001_standing_coated.png")
#vis.destroy_window()


# target =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/object_pcd.ply")
# canister =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/transf_101_canister_full_small.ply")
# small_bottle =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/transf_104_SmallSoyBroth_Bottle.ply")
# medium_bottle =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/transf_103_MediumRinseFluidK_Bottle.ply")
# large_bottle =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/transf_102_LargeRinseFluidA_Bottle.ply")

# icp_canister =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/icp_101_canister_full_small.ply")
# icp_small_bottle =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/icp_104_SmallSoyBroth_Bottle.ply")
# icp_medium_bottle =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/icp_103_MediumRinseFluidK_Bottle.ply")
# icp_large_bottle =  o3d.io.read_point_cloud("/home/julius/Desktop/verefine_pipeline/data/models/scenes/results/icp_102_LargeRinseFluidA_Bottle.ply")

# # o3d.visualization.draw_geometries([target])
# # o3d.visualization.draw_geometries([transfer])

# #o3d.visualization.draw_geometries([source])
# o3d.visualization.draw_geometries([target, canister, small_bottle, medium_bottle, large_bottle])
# o3d.visualization.draw_geometries([target, icp_canister, icp_small_bottle, icp_medium_bottle, icp_large_bottle])


