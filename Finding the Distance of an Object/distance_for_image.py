# import the necessary packages
from Helpers import *
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-mi", "--main_image", help = "image file")
ap.add_argument("-ds", "--distance_image", help = "image file")
ap.add_argument("-r", "--radius", type = int,help = "gaussian blur")
args = vars(ap.parse_args())

def configure_picture(name):
	img = cv2.imread(args[name])
	resize = Helpers.resize(img, width=500)
	gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5,5), 0)
	edged = cv2.Canny(gray, 0, 85)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
	closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

	(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in cnts:
		box = cv2.minAreaRect(c)
		box = cv2.boxPoints(box)
		box = np.array(box, dtype="int")
		box = Helpers.orders(box)
		(tl, tr, br, bl) = box
		cv2.drawContours(resize, [box.astype("int")], -1, (0, 0, 255), 2)

	return resize


main_image = configure_picture("main_image")
distance_image = configure_picture("distance_image")
# book's width: 12cm


 
cv2.imshow("main_image", main_image)
cv2.imshow("distance_image", distance_image)
cv2.waitKey(0)