# import the necessary packages
from __future__ import print_function
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = Helpers.resize(image, width=500)
shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
cv2.imshow("Input", shifted)
cv2.waitKey(0)

gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
