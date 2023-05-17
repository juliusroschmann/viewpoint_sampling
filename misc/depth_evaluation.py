#!/usr/bin/env python3
from skimage.io import imread, imread_collection
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np
import os

# Read the image as a float
folder_per_obj_masks = '/home/julius/Documents/Julius_03_masks'
folder_full_blender_depth = '/home/julius/Documents/Julius_03_depth_masks'
scenes = sorted(os.listdir(folder_per_obj_masks))

canister_list = []
small_bottle_list = []
medium_bottle_list = []
large_bottle_list = []
full_depth_list = []
to_eval_imgs_list = []

##here implement for loop over all scenes
for scene in [scenes[0]]:
    folder_to_evaluate = f'/home/julius/Documents/Julius_03_auswertung/scenes_trained_with_other_params/{scene}/nerfacto/depth_nerf_sigma_10_iter_5000/depth_nerf'

    folder1=os.path.join(folder_per_obj_masks, scene)
    for img in sorted(os.listdir(folder1)):
        image = (os.path.join(folder1, img))
        if "canister" in img:
            canister_list.append(image)
        elif "small" in img:
            small_bottle_list.append(image)
        elif "medium" in img:
            medium_bottle_list.append(image)
        elif "large" in img:
            large_bottle_list.append(image)

    canister_masks = imread_collection(canister_list)
    small_bottle_masks = imread_collection(small_bottle_list)
    medium_bottle_masks = imread_collection(medium_bottle_list)
    large_bottle_masks = imread_collection(large_bottle_list)

    folder2=os.path.join(folder_full_blender_depth, scene)
    for img in sorted(os.listdir(folder2)):
        image = (os.path.join(folder2, img))
        full_depth_list.append(image)

    blender_depth = imread_collection(full_depth_list)

    for img in sorted(os.listdir(folder_to_evaluate)):
        image = (os.path.join(folder_to_evaluate, img))
        to_eval_imgs_list.append(image)

    to_eval_imgs = imread_collection(to_eval_imgs_list)

    if len(canister_masks) != len(blender_depth) or len(small_bottle_masks) != len(blender_depth) or len(medium_bottle_masks) != len(blender_depth) or len(large_bottle_masks) != len(blender_depth) or len(to_eval_imgs) != len(blender_depth):
        print("canister_masks: ", len(canister_masks))
        print("small_bottle_masks: ", len(small_bottle_masks))
        print("medium_bottle_masks: ", len(canister_masks))
        print("large_bottle_masks: ", len(large_bottle_masks))
        print("blender_depth: ", len(blender_depth))
        print("to_eval_imgs: ", len(to_eval_imgs))
        
        raise ValueError (f"Lists do not have the same size! Check folder {folder1} or {folder2} or {folder_to_evaluate}!")
    
    else:
        for idx, item in enumerate(blender_depth):
           
            canister_gt = np.where(canister_masks[idx] > 0, blender_depth[idx], 0)
            small_bottle_gt = np.where(small_bottle_masks[idx] > 0, blender_depth[idx], 0)
            medium_bottle_gt = np.where(medium_bottle_masks[idx] > 0, blender_depth[idx], 0)
            large_bottle_gt = np.where(large_bottle_masks[idx] > 0, blender_depth[idx], 0)

            canister_real = np.where(canister_masks[idx] > 0, to_eval_imgs[idx], 0)
            small_bottle_real = np.where(small_bottle_masks[idx] > 0, to_eval_imgs[idx], 0)
            medium_bottle_real = np.where(medium_bottle_masks[idx] > 0, to_eval_imgs[idx], 0)
            large_bottle_real = np.where(large_bottle_masks[idx] > 0, to_eval_imgs[idx], 0)

            #canister_diff = canister_gt - canister_real
            small_bottle_diff = small_bottle_gt - small_bottle_real
            medium_bottle_diff = medium_bottle_gt - medium_bottle_real
            large_bottle_diff = large_bottle_gt - large_bottle_real
            full_diff = blender_depth[idx] - to_eval_imgs[idx]

            ##ACHTUNG CANISTER HAT LOCH --> #PIXEL ANDERS
            x = np.argwhere(large_bottle_gt[:,:] > 0)[:, 0]
            y = np.argwhere(large_bottle_gt[:,:] > 0)[:, 1]
            px_gt = large_bottle_gt[x, y]
            #print(px_gt[:50])
                       
            x = np.argwhere(large_bottle_real[:,:] > 0)[:, 0]
            y = np.argwhere(large_bottle_real[:,:] > 0)[:, 1]
            px_real = large_bottle_real[x, y]
            #print(px_real[:50])

            px_diff = px_gt - px_real
            
            #print(px_diff[:50])
            print("max: ", np.max(px_diff))
            print("min: ", np.min(px_diff))
            print("med: ", np.median(px_diff))
            print("mean: ", np.mean(px_diff))
            print("std: ", np.std(px_diff))
            print("var: ", np.var(px_diff))

            #print(np.all(np.equal(px_gt, px_real)))
                    
            # plt.imshow(large_bottle_diff, cmap="tab20")
            # plt.show()

            fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(20, 15))
            
            ax[0][0].imshow(canister_gt)
            ax[0][0].title.set_text("canister_gt")
            ax[0][1].imshow(canister_real)
            ax[0][1].title.set_text("canister_real")
            ax[0][2].imshow(np.random.randint(0,255, size=1280*720).reshape((720,1280)))
            ax[0][2].title.set_text("canister_diff")

            ax[1][0].imshow(small_bottle_gt)
            ax[1][0].title.set_text("small_bottle_gt")
            ax[1][1].imshow(small_bottle_real)
            ax[1][1].title.set_text("small_bottle_real")
            ax[1][2].imshow(small_bottle_diff)
            ax[1][2].title.set_text("small_bottle_diff")

            ax[2][0].imshow(medium_bottle_gt)
            ax[2][0].title.set_text("medium_bottle_gt")
            ax[2][1].imshow(medium_bottle_real)
            ax[2][1].title.set_text("medium_bottle_real")
            ax[2][2].imshow(medium_bottle_diff)
            ax[2][2].title.set_text("medium_bottle_diff")

            ax[3][0].imshow(large_bottle_gt)
            ax[3][0].title.set_text("large_bottle_gt")
            ax[3][1].imshow(large_bottle_real)
            ax[3][1].title.set_text("large_bottle_real")
            ax[3][2].imshow(large_bottle_diff)
            ax[3][2].title.set_text("large_bottle_diff")
            # ax = ax.ravel()
            # divider = make_axes_locatable(ax[0])
            # cax = divider.append_axes('right', size='5%', pad=0.05)
            # fig.colorbar(ax[0], cax=cax, orientation='vertical')

            # divider = make_axes_locatable(ax[1])
            # cax = divider.append_axes('right', size='5%', pad=0.05)
            # fig.colorbar(ax[1], cax=cax, orientation='vertical')

            plt.tight_layout()
            plt.show()


            # fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))
            # ax[0][0].imshow(canister_real)
            # ax[0][0].title.set_text("canister_real")
            # ax[0][1].imshow(small_bottle_real)
            # ax[0][1].title.set_text("small_bottle_real")
            # ax[1][0].imshow(medium_bottle_real)
            # ax[1][0].title.set_text("medium_bottle_real")
            # ax[1][1].imshow(large_bottle_real)
            # ax[1][1].title.set_text("large_bottle_real")
            # plt.tight_layout()
            
            
            # plt.show()

            break

    