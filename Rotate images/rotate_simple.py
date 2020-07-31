# IMPORT THE NECASSARY PACKAGES
import numpy as np
import argparse
import imutils
import cv2

# CONSTRUCT THE ARGUMENT PARSE AND PARSE THE ARGUMENTS
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help='path to the image file')
args = vars(ap.parse_args())

# LOAD THE IMAGE FROM DISK
image = cv2.imread(args['image'])

# LOOP OVER THE ROTATION ANGLES
for angle in np.arange(0,360,15):
	rotated = imutils.rotate(image, angle)
	cv2.imshow('Rotated (problematic)', rotated)
	cv2.waitKey(0)

# LOOP OVER THE ROTATION ANGLES AGAIN, THIS TIME ENSURING
# NO PART OF THE IMAGE IS CUT OFF
for angle in np.arange(0,360,15):
	rotated = imutils.rotate_bound(image, angle)
	cv2.imshow('Rotated (problematic)', rotated)
	cv2.waitKey(0)