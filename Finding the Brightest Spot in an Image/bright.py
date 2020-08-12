# import the necesarry packages
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "image file")
ap.add_argument("-r", "--radius", type = int,help = "gaussian blur")
args = vars(ap.parse_args())

img = cv2.imread(args['image'])
orig = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
cv2.circle(img, maxLoc, 5, (255,0,0), 2)
cv2.imshow("before", img)

gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
img = orig.copy()
cv2.circle(img, maxLoc, args["radius"], (255, 0, 0), 2)
cv2.imshow("After", img)
cv2.waitKey(0)