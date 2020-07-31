# import the necessary packages
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cv2.imshow("threshold", thresh)
cv2.waitKey(0)

def grap_contours(cnts):
	# if the length of the contours tuple is '2'
	if len(cnts) == 2:
		cnts = cnts[0]
	# if the length of the contours tuple is '3'
	elif len(cnts) == 3:
		cnts = cnts[1]
	else:
		raise Exception('The length of the contour must be 2 or 3.')
	return cnts

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = grap_contours(cnts)

# loop over the contours
for c in cnts:
	M = cv2.moments(c)
	if (M["m00"] != 0):
		# compute the center of the contour
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		# draw the contour and center of the shape on the image
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
		cv2.putText(image, "center", (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

		# show the image
		cv2.imshow("Image", image)
		cv2.waitKey(0)