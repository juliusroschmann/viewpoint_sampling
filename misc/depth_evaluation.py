#!/usr/bin/env python3
from skimage.io import imread, imread_collection
import ipdb
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from tqdm import tqdm
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def main():
    # Read the image as a float
    folder_per_obj_masks = '/home/julius/Documents/Julius_03_masks'
    folder_full_blender_depth = '/home/julius/Documents/Julius_03_depth_masks'
    scenes = sorted(os.listdir(folder_per_obj_masks))
    
    obj_list = ["canister", "small_bottle", "medium_bottle", "large_bottle"]
    title_list = []
    for obj in obj_list:
        title_list.append(f"{obj}_ground_truth_blender")
        title_list.append(f"{obj}_nerf_reconstruction")
        title_list.append(f"{obj}_depth_difference")

    test_img_indices = [3, 12, 13, 17, 18, 22, 23, 27, 30, 33, 34, 36, 41, 43, 46, 47, 49, 56, 64, 79, 87, 93, 97, 99, 103, 105, 106, 107, 108, 111, 112, 113, 114, 120, 121, 123, 124, 125, 127, 131, 137, 140, 156, 157, 166, 168, 171, 174, 179, 182, 183, 186, 187, 189, 195, 196, 197, 201, 202, 203, 212, 213, 214,
                        217, 224, 225, 230, 234, 235, 239, 242, 245, 250, 252, 253, 254, 255, 257, 258, 261, 268, 276, 301, 302, 305, 307, 308, 309, 311, 317, 319, 320, 324, 325, 327, 328, 329, 333, 335, 336, 339, 341, 349, 353, 368, 376, 380, 383, 386, 387, 391, 392, 395, 396, 402, 403, 408, 409, 410, 413, 414, 419, 420, 424]
    #test_img_indices = list(range(425))
 
    method = "nerfacto_2_centered_124"
    subsamples = [10, 20, 30, 40, 50, 60, 80, 100, 200, 300]
    #subsamples = [300]
    # here implement for loop over all scenes
    #for scene in [scenes[0]]:
    for subsample in subsamples:
        for scene in scenes:
            canister_list = []
            small_bottle_list = []
            medium_bottle_list = []
            large_bottle_list = []
            full_depth_list = []
            to_eval_imgs_list = []
            # folder_to_evaluate = f'/home/julius/Documents/Julius_03_auswertung/scenes_trained_with_other_params/{scene}/nerfacto/depth_nerf_sigma_10_iter_5000/depth_nerf'
            #folder_to_evaluate = f"/home/julius/Documents/Julius_03_x_auswertung/Julius_03_{subsample}/scenes/{scene}/depth_nerf"
            #folder_to_evaluate = f"/home/julius/Documents/Julius_03/scenes/{scene}/depth"
            #folder_to_evaluate = f"/home/julius/Documents/Julius_03_x_auswertung/Julius_03_{subsample}/instant-dex_nerf_full/{scene}/depth_{method}_full_Julius_03_{subsample}_scenes_{scene}"
            
            folder_to_evaluate = f"/home/julius/Documents/Julius_03_x_auswertung/Julius_03_{subsample}/scenes/{scene}/depth_nerf_124_v2_centered_nerfacto"
            
            folder_to_results = os.path.dirname(
                os.path.dirname(os.path.dirname(folder_to_evaluate))) + "/results/" + str(scene)
            print(folder_to_results)
            os.makedirs(folder_to_results, exist_ok=True)
        
            folder1 = os.path.join(folder_per_obj_masks, scene)
            subsample_image_names = [(str(item).zfill(6)) +
                                '.png' for item in test_img_indices]
            for img in sorted(os.listdir(folder1)):
                image = (os.path.join(folder1, img))
                
                if img[-10:] in subsample_image_names:
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

            folder2 = os.path.join(folder_full_blender_depth, scene)
            for img in sorted(os.listdir(folder2)):
                if img[-10:] in subsample_image_names:
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

                raise ValueError(
                    f"Lists do not have the same size! Check folder {folder1} or {folder2} or {folder_to_evaluate}!")

            else:
                mydict = {"Subsample": [], "File": [], "Scene": [], "Object": [], "Max": [],
                        "Min": [], "Median": [], "Mean": [], "Std": [], "Var": [], "Px_gt": [], "Px_real": [], "Px=0": []}
                for idx, _ in enumerate(tqdm(blender_depth)):

                    filename = os.path.basename(full_depth_list[idx])

                    canister_gt = np.where(
                        canister_masks[idx] > 0, blender_depth[idx], 0)
                    small_bottle_gt = np.where(
                        small_bottle_masks[idx] > 0, blender_depth[idx], 0)
                    medium_bottle_gt = np.where(
                        medium_bottle_masks[idx] > 0, blender_depth[idx], 0)
                    large_bottle_gt = np.where(
                        large_bottle_masks[idx] > 0, blender_depth[idx], 0)
                    gt_list = [canister_gt, small_bottle_gt,
                            medium_bottle_gt, large_bottle_gt]

                    canister_real = np.where(
                        canister_masks[idx] > 0, to_eval_imgs[idx], 0)
                    small_bottle_real = np.where(
                        small_bottle_masks[idx] > 0, to_eval_imgs[idx], 0)
                    medium_bottle_real = np.where(
                        medium_bottle_masks[idx] > 0, to_eval_imgs[idx], 0)
                    large_bottle_real = np.where(
                        large_bottle_masks[idx] > 0, to_eval_imgs[idx], 0)
                    real_list = [canister_real, small_bottle_real,
                                medium_bottle_real, large_bottle_real]

                    # #canister_diff = canister_gt - canister_real
                    # canister_diff = np.random.randint(0,10, size=1280*720).reshape((720,1280))
                    # small_bottle_diff = small_bottle_gt - small_bottle_real
                    # medium_bottle_diff = medium_bottle_gt - medium_bottle_real
                    # large_bottle_diff = large_bottle_gt - large_bottle_real
                    # full_diff = blender_depth[idx] - to_eval_imgs[idx]

                    # ACHTUNG CANISTER HAT LOCH --> #PIXEL ANDERS
                    # canister_diff = np.random.randint(
                    #      0, 10, size=1280*720).reshape((720, 1280))
                    canister_diff = calc_diff(
                        True, canister_gt, canister_real)
                    small_bottle_diff = calc_diff(
                        True, small_bottle_gt, small_bottle_real)
                    medium_bottle_diff = calc_diff(
                        True, medium_bottle_gt, medium_bottle_real)
                    large_bottle_diff = calc_diff(
                        True, large_bottle_gt, large_bottle_real)

                    diff_list = [canister_diff, small_bottle_diff,
                                medium_bottle_diff, large_bottle_diff]

                    master_list = [canister_gt, canister_real, canister_diff, small_bottle_gt, small_bottle_real, small_bottle_diff,
                                medium_bottle_gt, medium_bottle_real, medium_bottle_diff, large_bottle_gt, large_bottle_real, large_bottle_diff]

                    canister_vals = calc_diff(False, canister_gt, canister_real)
                    small_bottle_vals = calc_diff(
                        False, small_bottle_gt, small_bottle_real)
                    medium_bottle_vals = calc_diff(
                        False, medium_bottle_gt, medium_bottle_real)
                    large_bottle_vals = calc_diff(
                        False, large_bottle_gt, large_bottle_real)

                    # print("small_bottle_vals: ", small_bottle_vals)
                    # print("medium_bottle_vals: ", medium_bottle_vals)
                    # print("large_bottle_vals: ", large_bottle_vals)
                    # print()

                    mydict = append_to_dict(
                        mydict, subsample, filename, scene, canister_vals, object_name=obj_list[0])
                    mydict = append_to_dict(
                        mydict, subsample, filename, scene, small_bottle_vals, object_name=obj_list[1])
                    mydict = append_to_dict(
                        mydict, subsample, filename, scene, medium_bottle_vals, object_name=obj_list[2])
                    mydict = append_to_dict(
                        mydict, subsample, filename, scene, large_bottle_vals, object_name=obj_list[3])

                    # fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(20, 15))
                    # plt.set_cmap('plasma')
                    # plt.suptitle(f"Image {filename} from scene {scene}")
                    # for idx, ax in enumerate(axes.flat):
                    #     ax.set_axis_off()
                    #     im = ax.imshow(master_list[idx])
                    #     ax.set_title(title_list[idx])

                    # cb_ax = fig.add_axes([0.9, 0.1, 0.02, 0.8])
                    # cbar = fig.colorbar(im, cax=cb_ax)
                    # cbar.set_ticks(np.arange(0, 100.5, 5)) # cbar.set_ticklabels(['low', 'medium', 'high'])
                    # fname = filename.split(".png")[0]              
                    # # plt.savefig(folder_to_results + f"/{scene}_{fname}_{method}.pdf") #, bbox_inches='tight')
                    # # fig.close()
                    # plt.show()
                    

                df = pd.DataFrame.from_dict(data=mydict)
                path_string = folder_to_results + f"/results_{scene}_{method}.csv"
                #path_string = folder_to_results + f"/results_{scene}_{method}_FULL.csv"
                df.to_csv(path_string)
                print(f"Saving dataframe to: {path_string}")
                # print(df.head(100))
                # print(df["Max"].mean())
                # print(df["Min"].mean())
                # print(df["Median"].mean())
                # print(df["Mean"].mean())



def calc_diff(just_diff, obj_gt, obj_real):

    new_img = np.zeros_like(obj_gt)
    x = np.argwhere(obj_gt)[:, 0]
    y = np.argwhere(obj_gt)[:, 1]
    px_gt = obj_gt[x, y]
    px_real = obj_real[x, y]

    zeros = np.argwhere(px_real == 0)
    
    flag = 0
    if flag:
        px_gt_reduced = px_gt
        px_gt_reduced[zeros] = 0
        px_diff = np.abs(px_gt_reduced - px_real)
        # print(px_diff)
        px_diff_clipped = np.clip(np.abs(px_diff), 0, 100)
        # print(px_diff)
        new_img[x, y] = px_diff_clipped

    else:
        px_diff = np.abs(px_gt - px_real)
        # print(px_diff)
        px_diff_clipped = np.clip(np.abs(px_diff), 0, 100)
        # print(px_diff)
        new_img[x, y] = px_diff_clipped

    if just_diff:
        # print(f"px_gt median: {np.median(px_gt):.4f}, px_real median: {np.median(px_real):.4f}, diff factor: {(np.median(px_gt) / np.median(px_real)):.4f}" )
        # print(f"px_gt mean: {np.mean(px_gt):.4f}, px_real mean: {np.mean(px_real):.4f}, diff factor: {(np.mean(px_gt) / np.mean(px_real)):.4f}" )
        # print()
        return new_img

    if len(px_diff) == 0:
        return [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    else:
        return [np.max(px_diff), np.min(px_diff), np.median(px_diff), np.mean(px_diff), np.std(px_diff), np.var(px_diff), len(px_gt), len(px_real), len(zeros)]#(len(np.argwhere(px_real)) / len(np.argwhere(px_gt)))]


def append_to_dict(mydict, subsample, filename, scene, vals, object_name):
    mydict["Subsample"].append(subsample)
    mydict["File"].append(filename)
    mydict["Scene"].append(scene)
    mydict["Object"].append(object_name)
    mydict["Max"].append(vals[0])
    mydict["Min"].append(vals[1])
    mydict["Median"].append(vals[2])
    mydict["Mean"].append(vals[3])
    mydict["Std"].append(vals[4])
    mydict["Var"].append(vals[5])
    mydict["Px_gt"].append(vals[6])
    mydict["Px_real"].append(vals[7])
    mydict["Px=0"].append(vals[8])
    return mydict


if __name__ == '__main__':
    main()
