# import the necessary packages
from Helpers import *
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Image path")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
image = Helpers.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Using the Sobel method, horizontal and vertical gray scales are applied
gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

cv2.imshow("gradX", Helpers.resize(gradX, width=250))
cv2.imshow("gradY", Helpers.resize(gradY, width=250))
cv2.imshow("gradient", Helpers.resize(gradient, width=250))
cv2.waitKey(0)
cv2.destroyAllWindows()



blurred = cv2.blur(gradient, (9,9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
cv2.imshow("thresh", Helpers.resize(thresh, width=250))

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)
cv2.imshow("closed", Helpers.resize(closed, width=250))
cv2.waitKey(0)
cv2.destroyAllWindows()



cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = Helpers.grab_contours(cnts)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box = np.int0(box)

cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)