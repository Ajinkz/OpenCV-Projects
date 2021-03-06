# import the necessary packages
from scipy import ndimage
from skimage.morphology import watershed
from skimage.feature import peak_local_max
import numpy as np
from Helpers import *
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

D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=30, labels=thresh)
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

for label in np.unique(labels):
	if label == 0:
		continue
	mask = np.zeros(gray.shape, dtype="uint8")
	mask[labels == label] = 255
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
	c = max(cnts, key=cv2.contourArea)
	((x, y), r) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 6)
	cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
		cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    

cv2.imshow("Output", image)
cv2.waitKey(0)