# import the necessary packages
from scipy.spatial import distance as dist
from Helpers import *
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-mi", "--main_image", help = "image file")
ap.add_argument("-ds", "--distance_image", help = "image file")
ap.add_argument("-r", "--radius", type = int,help = "gaussian blur")
args = vars(ap.parse_args())

def distance(a,b):
	return int(dist.euclidean(a,b))


def configure_picture(name):
	img = cv2.imread(args[name])
	resize = Helpers.resize(img, width=500)
	gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5,5), 0)
	edged = cv2.Canny(gray, 0, 100)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
	closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

	(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in cnts:
		box = cv2.minAreaRect(c)
		box = cv2.boxPoints(box)
		box = np.array(box, dtype="int")
		box = Helpers.orders(box)
		(tl, tr, br, bl) = box
		cv2.drawContours(resize, [box.astype("int")], -1, (199, 214, 66), 4)

		width = distance(tl, tr)
		height = distance(tl, bl)

	print("width: ", width/21.25)
	print("height: ", height/21.25)
	return resize,width,height


main_image, mw, mh = configure_picture("main_image")


 
cv2.imshow("main_image", main_image)
cv2.waitKey(0)