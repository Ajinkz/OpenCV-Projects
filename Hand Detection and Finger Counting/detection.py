# import the necessary packages
from Helpers import *
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True,help="path to the image file")
args = vars(ap.parse_args())

img = cv2.imread(args['image'])


hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 48, 80], dtype="uint8")
upper = np.array([20, 255, 255], dtype="uint8")
skin_region_hsv = cv2.inRange(hsv_img, lower, upper)
blurred = cv2.blur(skin_region_hsv, (2,2))
ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)

cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy(),
	cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = Helpers.grab_contours(cnts)
cnts = max(cnts, key=lambda x: cv2.contourArea(x))
cv2.drawContours(img, [cnts], -1, (74, 186, 110), 2)

cv2.imshow("Draw Contours", img)
cv2.waitKey(0)


hull = cv2.convexHull(cnts)
cv2.drawContours(img, [hull], -1, (214, 126, 66), 2)
cv2.imshow("Hull", img)
cv2.waitKey(0)

hull = cv2.convexHull(cnts, returnPoints=False) # convexity 
defects = cv2.convexityDefects(cnts, hull)

if defects is not None:
	cnt = 0

for i in range(defects.shape[0]):
	s, e, f, d = defects[i][0]
	start = tuple(cnts[s][0])
	end = tuple(cnts[e][0])
	far = tuple(cnts[f][0])
	a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
	b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
	c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
	angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
	# cosine theorem
	if angle < np.pi / 2:
		# angle less than 90 degree, treat as finger
		cnt += 1
		cv2.circle(img, far, 4, (74, 40, 247), -1)

if cnt > 0:
	cnt = cnt + 1

cv2.putText(img, "Value: {}".format(cnt), (15,25),
	cv2.FONT_HERSHEY_SIMPLEX, 0.75, (74, 40, 247), 2, cv2.LINE_AA)
cv2.imshow("Output Image", img)
cv2.waitKey(0)