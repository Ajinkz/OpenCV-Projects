# import the necessary packages
from Helpers import *
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True,help='path to the image file')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = Helpers.grab_contours(cnts)
mask = np.ones(image.shape[:2], dtype='uint8') * 255

def detect_shape(c):
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02*peri, True)
	if not len(approx) == 4:
		cv2.drawContours(image, [c], -1, (0, 0, 0), -1)
		cv2.drawContours(mask, [c], -1, (0,0,0), -1)
		
for (i,c) in enumerate(cnts):
	detect_shape(c)
	

cv2.imshow("Original Image", original)
cv2.imshow('Deleted Shapes',mask)
cv2.imshow("Output Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()