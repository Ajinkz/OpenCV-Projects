# import the necessary packages
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
	help="path to input directory of images")
ap.add_argument('-t', '--threshold', type=float,
	default=float, help="boundary of blurred")
args = vars(ap.parse_args())

def calculat_laplacian(img):
	return cv2.Laplacian(img, cv2.CV_64F).var()

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
fm = calculat_laplacian(gray)
text = "Not Blurry"

if fm < args["threshold"]:
	text = "Blurry"

cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)
