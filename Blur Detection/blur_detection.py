import cv2
import argparse
import glob


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', required=True,
	help="path to input directory of images")
ap.add_argument('-t', '--threshold', type=float,
	default=float, help="boundary of blurred")
args = vars(ap.parse_args())

images = [cv2.imread(file) for file in glob.glob("{}/*.jpeg".format(args['images']))]

for image in images:
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = cv2.Laplacian(gray, cv2.CV_64F).var()
	text = "Not Blurry"

	if fm < args["threshold"]:
		text = "Blurry"

	cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	cv2.waitKey(0)