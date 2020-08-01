# import the necessary packages
import cv2
import argparse
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args['image'])
rgb_data = []

for chan in cv2.split(image):
	chan_mean = np.mean(chan)
	rgb_data.append(chan_mean)

print("rgb_data: ", rgb_data)

