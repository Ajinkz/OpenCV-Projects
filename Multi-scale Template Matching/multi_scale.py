# import the necessary packages
import numpy as np
import argparse
import glob
import cv2
from Helpers import * 

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="Path to template image")
ap.add_argument("-i", "--images", required=True,
	help="Path to images where template will be matched")
args = vars(ap.parse_args())

template = cv2.imread(args["template"])
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 200, 235)
(tH, tW) = template.shape[:2]
cv2.imshow("template", template)

for imagePath in glob.glob(args["images"] + "/*.jpg"):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	found = None
	for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		resized = Helpers.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break

		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
	
	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 4)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
