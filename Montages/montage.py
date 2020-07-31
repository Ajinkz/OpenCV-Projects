# import the necassary packages
import numpy as np
from imutils import paths
import argparse
import cv2
import random

# construct the arguments parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i","--images",required=True,help="path to input directory of images")
ap.add_argument("-s", "--sample", type=int, default=21, help="# of images to sample")
args = vars(ap.parse_args())
"""
--images : The path to your directory containing the images you want to build a montage
		   out of.
--samples : An optional command line argument that specifies the number of images to
            sample (we default this value to 21  total images).
"""

def montage(image_list, image_shape, montage_shape):
	if len(image_shape) != 2:
		raise Exception('image shape must be list or tuple of length 2 (rows, cols)')
	if len(montage_shape) != 2:
		raise Exception('montage shape must be list or tuple of length 2 (rows, cols)')

	image_montages = []
	montage_image = np.zeros(shape=(image_shape[1] * montage_shape[1], 
		image_shape[0] * montage_shape[0], 3),dtype=np.uint8)
	cursor_pos = [0, 0]
	start_new_img = False
	for img in image_list:
		if type(img).__module__ != np.__name__:
			raise Exception('input of type {} is not a valid numpy array'.format(type(img)))
		start_new_img = False
		img = cv2.resize(img, image_shape)
		montage_image[cursor_pos[1]:cursor_pos[1]+image_shape[1], cursor_pos[0]:cursor_pos[0]+image_shape[0]] = img
		cursor_pos[0] += image_shape[0]
		if cursor_pos[0] >= montage_shape[0] * image_shape[0]:
			cursor_pos[1] += image_shape[1]
			cursor_pos[0] = 0
			if cursor_pos[1] >= montage_shape[1] * image_shape[1]:
				cursor_pos = [0, 0]
				image_montages.append(montage_image)
				montage_image = np.zeros(shape=(image_shape[1] * (montage_shape[1]),
					image_shape[0] * montage_shape[0], 3),dtype=np.uint8)
				start_new_img = True
	if start_new_img is False:
		image_montages.append(montage_image)
	return image_montages

imagePaths = list(paths.list_images(args["images"]))
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]

# initialize the list of images
images = []
# loop over the list of image paths
for imagePath in imagePaths:
	# load the image and update the list of images
	image = cv2.imread(imagePath)
	images.append(image)
# construct the montages for the images
montages = montage(images, (128, 196), (7, 3))

for montage in montages:
	cv2.imshow("Montage", montage)
	cv2.waitKey(0)