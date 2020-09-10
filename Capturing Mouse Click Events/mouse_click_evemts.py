import cv2
import argparse

refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
	global refPt, cropping

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x,y)]
		cropping = True

	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x,y))
		cropping = False

		cv2.rectangle(image, refPt[0], refPt[1], (0,255,0), 2)
		cv2.imshow('image', image)


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
	dim = None
	(h, w) = image.shape[:2]
	if width is None and height is None:
		return image
	if width is None:
		r = height / float(h)
		dim = (int(w * r), height)
	else:
		r = width / float(w)
		dim = (width, int(h * r))
		resized = cv2.resize(image, dim, interpolation=inter)
	return resized

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = resize(image, 600)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)


while True:
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("r"):
		image = clone.copy()
	elif key == ord("c"):
		break


if len(refPt) == 2:
	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	cv2.imshow("ROI", roi)
	cv2.waitKey(0)
# close all open windows
cv2.destroyAllWindows()