# import the necessary packages
import numpy as np
import argparse
import cv2

"""
- boundingBoxes: we use it to find the center of mass
- moments: Calculates all of the moments up to the third order of a polygon or rasterized shape.
- zip: The zip() function returns a zip object, which is an iterator of tuples where the first 
	   item in each passed iterator is paired together, and then the second item in each passed 
	   iterator are paired together etc.

"""

# FUNCTIONS 
def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False

	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)


def draw_contour(image, c, i):
	# compute the center of the contour area and draw a circle
	# representing the center
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	# draw the countour number on the image
	cv2.putText(image, "{}".format(i + 1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.85, (0, 0, 0), 2)
	# return the image with the contour number drawn on it
	return image


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





# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image")
ap.add_argument("-m", "--method", required=True, help="Sorting method")
args = vars(ap.parse_args())

# load the image and initialize the accumulated edge image
image = cv2.imread(args["image"])
accumEdged = np.zeros(image.shape[:2], dtype="uint8")

# loop over the blue, green, and red channels, respectively
for chan in cv2.split(image):
	# blur the channel, extract edges from it, and accumulate the set
	# of edges for the image
	chan = cv2.GaussianBlur(chan, (5,5), 0)
	edged = cv2.Canny(chan, 50, 150)
	accumEdged = cv2.bitwise_or(accumEdged, edged)
# show the accumulated edge map
cv2.imshow("Edge Map", accumEdged)


# find contours in the accumulated image, keeping only the largest
# ones
cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:len(cnts)]
orig = image.copy()
# loop over the (unsorted) contours and draw them
for (i, c) in enumerate(cnts):
	orig = draw_contour(orig, c, i)
# show the original, unsorted contour image
cv2.imshow("Unsorted", orig)
# sort the contours according to the provided method
(cnts, boundingBoxes) = sort_contours(cnts, method=args["method"])
# loop over the (now sorted) contours and draw them
for (i, c) in enumerate(cnts):
	draw_contour(image, c, i)
# show the output image
cv2.imshow("Sorted", image)
cv2.waitKey(0)