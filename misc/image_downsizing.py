from PIL import Image
import glob
import os

# new folder path (may need to alter for Windows OS)
# change path to your path
path = '/home/julius/Documents/Julius_03_960x540/scenes/006_lying_empty_960x540/rgb' #the path where to save resized images
# create new folder
if not os.path.exists(path):
    os.makedirs(path)

# loop over existing images and resize
# change path to your path
for filename in glob.glob('/home/julius/Documents/Julius_03/scenes/006_lying_empty/rgb/*.png'): #path of raw images
    img = Image.open(filename).resize((960,540))
    # save resized images to new folder with existing filename
    img.save('{}{}{}'.format(path,'/',os.path.split(filename)[1]))