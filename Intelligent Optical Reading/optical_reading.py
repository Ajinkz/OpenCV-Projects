# import the necessary packages
from Helpers import *
import numpy as np
import argparse
import cv2

ANSWERS = [1,4,0,3,1]

# image upload part
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "No image path is specified")
args = vars(ap.parse_args())

kernel = np.ones((5,5), np.uint8) 
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
erosion = cv2.erode(gray, kernel, iterations=1)
deliation = cv2.dilate(erosion, kernel, iterations=1)
blurred = cv2.GaussianBlur(deliation, (7,7), 0)
edged = cv2.Canny(blurred, 100, 200)

"""
cv2.imshow("edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

# find contours in the edge image
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = Helpers.grab_contours(cnts)
object_cnts = []

# checking if it detects contours
if len(cnts) > 0:
	# sorting from large to small (field size)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	for c in cnts:
		# find out how many corners the object has
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if len(approx) == 4: # for rectangle
			object_cnts = approx
			break

# print("the document corners: ", object_cnts)

optic_form = Helpers.transform(image, object_cnts.reshape(4,2))

cv2.imshow("optic_form", optic_form)
cv2.waitKey(0)
cv2.destroyAllWindows()

thresh = cv2.threshold(Helpers.transform(gray,object_cnts.reshape(4,2)) , 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = Helpers.grab_contours(cnts)
question_cnts = []

for c in cnts:
	(x, y, w, h) = cv2.boundingRect(c)
	ratio = w / float(h) # for square
	if w >=18 and h >= 20 and ratio >= 0.9 and ratio <= 1.1:
		question_cnts.append(c)

# top->bottom, left->right
question_cnts = Helpers.sort_contours(question_cnts, method="top-to-bottom")[0]
number_of_true = 0
"""
print("number of question_cnts", len(question_cnts))
for c in question_cnts:
	mask = np.zeros(thresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)
	mask = cv2.bitwise_and(thresh, thresh, mask=mask)
	total = cv2.countNonZero(mask)
	cv2.drawContours(optic_form, c, -1, (0,0,255) , -1)

cv2.imshow("optic_form bubbles", optic_form)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""


for (question, i) in enumerate(np.arange(0, len(question_cnts), int(len(question_cnts)/5))):
	cnts = Helpers.sort_contours(question_cnts[i:i + 5])[0] # for each row
	bubbled = None

	for (j, c) in enumerate(cnts):
		mask = np.zeros_like(thresh)
		mask = mask.astype('uint8')
		cv2.drawContours(mask, [c], -1, 255, -1)
		"""
		cv2.imshow("question", mask)
		cv2.waitKey(0)
		"""
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
		# The bubbled value will be None when each row is returned.
		# In each question, the answer with the smallest area will be accepted.
		# This is because when the person draw a balloon, that area is covered 
		# in black. And the white color space is reduced. Here, determination is 
		# made depending on that area.
		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)

	key = ANSWERS[question]
	color = (0, 0, 255)
	if key == bubbled[1]:
		color = (0, 255, 0)
		number_of_true += 1

	cv2.drawContours(optic_form, [cnts[key]], -1, color, 3)

score = (number_of_true/ 5.0) * 100
cv2.putText(optic_form, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Output", optic_form)
cv2.waitKey(0)
cv2.destroyAllWindows()