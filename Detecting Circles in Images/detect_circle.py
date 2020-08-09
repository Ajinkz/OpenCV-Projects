# import the necessary packages
from Helpers import *
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = Helpers.resize(image, width=500)
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("gray",gray)
cv2.waitKey(0)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)


if circles is not None:
	circles = np.round(circles[0, :]).astype("int")
	for (x,y,r) in circles:
		cv2.circle(output, (x,y), r, (255,0,0), 4)
		cv2.rectangle(output, (x-5, y-5), (x+5, y+5), (128,128,128), -1)
	cv2.imshow("output", np.hstack([image, output]))
	cv2.imwrite('output/output-{}.jpeg'.format(args["image"].split('\\')[1].split(".")[0]), output)
	cv2.waitKey(0)


"""
HoughCircles Paramaters:
image: 8-bit, single channel image. If working with a color image, convert to grayscale first.
method: Defines the method to detect circles in images.
	 	Currently, the only implemented method is cv2.HOUGH_GRADIENT, 
	 	which corresponds to the Yuen et al. paper.
dp: This parameter is the inverse ratio of the accumulator resolution 
	to the image resolution (see Yuen et al. for more details). 
	Essentially, the larger the dp gets, the smaller the accumulator array gets.
minDist: Minimum distance between the center (x, y) coordinates of detected circles.
		 If the minDist is too small, multiple circles in the same neighborhood as 
		 the original may be (falsely) detected. If the minDist is too large, then 
		 some circles may not be detected at all.
param1: Gradient value used to handle edge detection in the Yuen et al. method.
param2: Accumulator threshold value for the cv2.HOUGH_GRADIENT method. The smaller 
		the threshold is, the more circles will be detected (including false circles).
		The larger the threshold is, the more circles will potentially be returned.
minRadius: Minimum size of the radius (in pixels).
maxRadius: Maximum size of the radius (in pixels).
"""