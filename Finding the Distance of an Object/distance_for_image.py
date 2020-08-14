# import the necessary packages
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-mi", "--main_image", help = "image file")
ap.add_argument("-ds", "--distance_image", help = "image file")
ap.add_argument("-r", "--radius", type = int,help = "gaussian blur")
args = vars(ap.parse_args())

img1 = cv2.imread(args['main_image'])
img2 = cv2.imread(args['distance_image'])
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)
cv2.waitKey(0)