# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

# find all the 'black' shapes in the image
lower = np.array([0, 0, 0])
upper = np.array([18, 18, 18])
shapeMask = cv2.inRange(image, lower, upper)

cv2.imshow("original", image)
cv2.waitKey(0)

def grab_contours(cnts):
	# if the length of the contours tuple is '2'
	if len(cnts) == 2:
		cnts = cnts[0]
	# if the length of the contours tuple is '3'
	elif len(cnts) == 3:
		cnts = cnts[1]
	else:
		raise Exception('The length of the contour must be 2 or 3.')
	return cnts

cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = grab_contours(cnts)
print("I found {} black shapes".format(len(cnts)))
cv2.imshow("Mask", shapeMask)

# loop over the contours
for c in cnts:
	# draw the contour and show it
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)