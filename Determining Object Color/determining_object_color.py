# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import argparse
import cv2


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())


def grab_contours(cnts):
	if len(cnts) == 2:
		cnts = cnts[0]
	elif len(cnts) == 3:
		cnts = cnts[1]
	else:
		raise Exception('The length of the contour must be 2 or 3.')
	return cnts

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized


def detect_color(image,c):
	# initialize the colors dictionary, containing the color
	# name as the key and the RGB tuple as the value
	colors = OrderedDict({
		"red": (255, 0, 0),
		"green": (0, 255, 0),
		"blue": (0, 0, 255)})

	# allocate memory for the L*a*b* image, then initialize
	# the color names list
	lab = np.zeros((len(colors), 1, 3), dtype="uint8")
	colorNames = []

	# loop over the colors dictionary
	for (i, (name, rgb)) in enumerate(colors.items()):
		# update the L*a*b* array and the color names list
		lab[i] = rgb
		colorNames.append(name)

	# convert the L*a*b* array from the RGB color space
	# to L*a*b*
	lab = cv2.cvtColor(lab, cv2.COLOR_RGB2LAB)
	mask = np.zeros(image.shape[:2], dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)
	mask = cv2.erode(mask, None, iterations=2)
	mean = cv2.mean(image, mask=mask)[:3]

	cv2.imshow("mask", mask)
	cv2.waitKey(0)


	minDist = (np.inf, None)

	for (i, row) in enumerate(lab):
		d = dist.euclidean(row[0], mean)
		if d < minDist[0]:
			minDist = (d, i)
	return colorNames[minDist[1]]


def detect_shape(c):
	# initialize the shape name and approximate the contour
	shape = "unidentified"
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * peri, True)

	# if the shape is a triangle, it will have 3 vertices
	if len(approx) == 3:
		shape = "triangle"
	# if the shape has 4 vertices, it is either a square or
	# a rectangle
	elif len(approx) == 4:
		# compute the bounding box of the contour and use the
		# bounding box to compute the aspect ratio
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)
		# a square will have an aspect ratio that is approximately
		# equal to one, otherwise, the shape is a rectangle
		shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
	# if the shape is a pentagon, it will have 5 vertices
	elif len(approx) == 5:
			shape = "pentagon"
	# otherwise, we assume the shape is a circle
	else:
		shape = "circle"
	# return the name of the shape
	return shape


# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# blur the resized image slightly, then convert it to both
# grayscale and the L*a*b* color spaces
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = grab_contours(cnts)

# loop over the contours
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	if M["m00"] != 0:
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
	else:
	    cX, cY = 0, 0
	
	# detect the shape of the contour and label the color
	shape = detect_shape(c)
	color = detect_color(lab, c)

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape and labeled
	# color on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	text = "{} {}".format(color, shape)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, text, (cX - 25, cY),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)