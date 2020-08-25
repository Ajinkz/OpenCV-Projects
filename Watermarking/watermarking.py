from Helpers import Helpers
import numpy as np
import argparse
import glob
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--watermark", required=True, help="png image - watermark")
ap.add_argument("-i", "--images", required=True, help="images folder")
args = vars(ap.parse_args())


watermark = cv2.imread(args["watermark"], cv2.IMREAD_UNCHANGED)
watermark = Helpers.resize(watermark, width=200)
(wH, wW) = watermark.shape[:2]

(B, G, R, A) = cv2.split(watermark)
B = cv2.bitwise_and(B, B, mask=A)
G = cv2.bitwise_and(G, G, mask=A)
R = cv2.bitwise_and(R, R, mask=A)
watermark = cv2.merge([B, G, R, A])

for imagePath in glob.glob(args["images"] + "/*.jpeg"):
	image = cv2.imread(imagePath)
	(h, w) = image.shape[:2]
	image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])
	overlay = np.zeros((h, w, 4), dtype="uint8")
	overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark
	output = image.copy()
	cv2.addWeighted(overlay, 0.33 , output, 1.0, 0, output)
	filename = imagePath[imagePath.rfind(os.path.sep) + 1:]
	p = os.path.sep.join(("output", filename))
	cv2.imwrite(p, output)