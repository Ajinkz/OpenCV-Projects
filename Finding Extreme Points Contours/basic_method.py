# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

lower = np.array([0, 0, 0])
upper = np.array([20, 20, 20])
shapeMask = cv2.inRange(image, lower, upper)


cv2.imshow("shapeMask", shapeMask)
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

for c in cnts:
	# draw the contour and show it
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)