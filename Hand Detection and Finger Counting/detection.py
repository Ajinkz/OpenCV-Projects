# import the necessary packages
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True,help="path to the image file")
args = vars(ap.parse_args())

img = cv2.imread(args['image'])
cv2.imshow("image", img)
cv2.waitKey(0)