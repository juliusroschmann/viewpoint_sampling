
import argparse
import cv2
import numpy as np
import os
import sys
from tqdm import tqdm
import trimesh
import yaml
import open3d as o3d
import copy
import v4r_dataset_toolkit as v4r
# This needs to be imported before pyrender to disable
# antialiasing in mask generation
from v4r_dataset_toolkit import pyrender_wrapper
import pyrender
from PIL import Image
import matplotlib.pyplot as plt

groundtruth_to_pyrender = np.array([[1, 0, 0, 0],
                                    [0, -1, 0, 0],
                                    [0, 0, -1, 0],
                                    [0, 0, 0, 1]])


def project_mesh_to_2d(models, cam_poses, intrinsic):
    # --- PyRender scene setup ------------------------------------------------
    scene = pyrender.Scene(bg_color=[0, 0, 0])

    seg_node_map = {}
    # Add model mesh
    for model_idx, model in enumerate(models):
        # pyrender render flag SEG does not allow to ignore culling backfaces
        # Instead set color for the mask on the trimesh mesh
        visual = trimesh.visual.create_visual(mesh=model)
        model.visual = visual
        pyr_mesh = pyrender.Mesh.from_trimesh(model, smooth=False)
        nm = pyrender.Node(mesh=pyr_mesh)
        scene.add_node(nm)

    # Add camera
    camera = pyrender.camera.IntrinsicsCamera(intrinsic.fx,
                                              intrinsic.fy,
                                              intrinsic.cx,
                                              intrinsic.cy)
    nc = pyrender.Node(camera=camera, matrix=np.eye(4))
    scene.add_node(nc)
    nl = pyrender.Node(matrix=np.eye(4))
    scene.add_node(nl)

   # --- Rendering -----------------------------------------------------------
    renders = []
    r = pyrender.OffscreenRenderer(intrinsic.width, intrinsic.height)
    for cam_pose in tqdm(cam_poses, desc="Reprojection rendering"):
        # different coordinate system when using renderer
        cam_pose = cam_pose.dot(groundtruth_to_pyrender)
        # Render
        scene.set_pose(nc, pose=cam_pose)
        scene.set_pose(nl, pose=cam_pose)

        depth = r.render(
            scene,
            flags=pyrender.RenderFlags.DEPTH_ONLY)

        depth = (1000. * depth).astype(np.uint16)
        renders.append(depth)

    return renders


def put_text(text, img, x, y, color):
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)

    img = cv2.rectangle(img, (x, y - 30), (x + w, y), color, -1)
    img = cv2.putText(img, text, (x, y - 8),
                      cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 1)


def load_object_models(scene_file_reader):
    oriented_models = []
    # Load poses
    objects = scene_file_reader.get_object_poses(args.scene_id)
    for object in tqdm(objects, desc="Loading objects"):
        scene_object = scene_file_reader.object_library[object[0].id]
        model = scene_object.mesh.as_trimesh()
        model.apply_transform(np.array(object[1]).reshape(4, 4))
        oriented_models.append(model)
    return oriented_models


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Reproject models to create annotation images.")
    parser.add_argument("-c", "--config", type=str, required=True,
                        help="Path to reconstructed data")
    parser.add_argument("-s", "--scene_id", type=str, required=True,
                        help="Scene identifier to visualize.")
    parser.add_argument("-b", "--background", action='store_true',
                        help="Combine rendered depth with existing scene depth maps.")
    parser.add_argument("-o", "--output", type=str, default='',
                        help="Output directory for masked images.")
    parser.add_argument("-v", "--visualize", action='store_true',
                        help="Visualize scene and optionally save to file.")
    parser.add_argument("-r", "--rotate", action='store_true', default='',
                        help="Rotate image.")
    args = parser.parse_args()

    if args.output:
        if not os.path.exists(args.output):
            print(f"Output path {args.output} does not exist.")
            sys.exit()

    if not args.output and not args.visualize:
        print("You have to specify option --output or --visualize or both.\n")
        parser.print_help()
        sys.exit(1)

    scene_file_reader = v4r.io.SceneFileReader.create(args.config)
    camera_poses = scene_file_reader.get_camera_poses(args.scene_id)
    intrinsic = scene_file_reader.get_camera_info_scene(args.scene_id)
    objects = scene_file_reader.get_object_poses(args.scene_id)
    oriented_models = load_object_models(scene_file_reader)

    if(args.background):
        depth_sensor_imgs = scene_file_reader.get_images_depth(args.scene_id)

    orig_imgs = scene_file_reader.get_images_rgb(args.scene_id)
    camera_poses = [pose.tf for pose in camera_poses]
    depth_imgs = project_mesh_to_2d(
        oriented_models, camera_poses, intrinsic)

    if args.visualize:
        cv2.namedWindow('Object Depth Visualization',
                        flags=cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_EXPANDED)
        stop = False
        for pose_idx, depth_img in enumerate(depth_imgs):
            if stop or not cv2.getWindowProperty('Object Depth Visualization', cv2.WND_PROP_VISIBLE):
                break

            if(args.background):
                depth_sensor = np.asarray(depth_sensor_imgs[pose_idx])
                blended = depth_sensor.copy()
                blended[depth_img != 0] = depth_img[depth_img != 0]
                blended[depth_sensor != 0] = np.minimum(blended[depth_sensor != 0], depth_sensor[depth_sensor != 0])
            else:
                blended = depth_img

            print(f"Scene: {pose_idx}")

            cv2.imshow('Object Depth Visualization',
                       cv2.normalize(blended.astype(np.float32), None, norm_type=cv2.NORM_MINMAX))

            outimg = blended
            if args.output:
                output = os.path.join(args.output, f"depth_{pose_idx:03d}.png")
                cv2.imwrite(output, outimg)

            while cv2.getWindowProperty('Object Depth Visualization', cv2.WND_PROP_VISIBLE):
                key = cv2.waitKey(1)
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    stop = True
                    break
                elif key == ord('n'):
                    break
    else:
        filepaths = scene_file_reader.get_images_rgb_path(args.scene_id)
        pbar = tqdm(enumerate(depth_imgs), desc=f"Saving")
        for pose_idx, depth_img in pbar:
            filename = f"{objects[i][0].name}_" + \
                    f"{i:03d}_" + os.path.basename(filepaths[pose_idx])
            output_path = os.path.join(
                    args.output, filename)
