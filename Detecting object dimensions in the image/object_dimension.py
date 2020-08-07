# import the necessary packages
from scipy.spatial import distance as dist
from Helpers import *
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
resize = Helpers.resize(image, width=800)
gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(gray, 0, 70)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0

def draw_circle(xy,r,color):
	cv2.circle(resize, (int(xy[0]), int(xy[1])) , r, color, -1)

def mid_point(a,b):
	return ((a[0] + b[0]) / 2 , (a[1] + b[1]) / 2)
 

def draw_line(a,b):
	cv2.line(resize, (int(a[0]),int(a[1])), (int(b[0]), int(b[1])), (255,0,0), thickness=2)

def distance(a,b):
	return int(dist.euclidean(a,b))


for c in cnts:
  box = cv2.minAreaRect(c)
  box = cv2.boxPoints(box)
  box = np.array(box, dtype="int")
  box = Helpers.orders(box)
  (tl, tr, br, bl) = box

  cv2.drawContours(resize, [box.astype("int")], -1, (0, 0, 255), 2)


  for xy in box:
  	draw_circle(xy,4,(0,255,0))
  
  tltr = mid_point(tl,tr)
  tlbl = mid_point(tl,bl)
  trbr = mid_point(tr,br)
  blbr = mid_point(bl,br)

  draw_circle(tltr,4,(255,0,0))
  draw_circle(tlbl,4,(255,0,0))
  draw_circle(trbr,4,(255,0,0))
  draw_circle(blbr,4,(255,0,0))

  draw_line(tltr, blbr)
  draw_line(tlbl, trbr)

  dA = distance(tltr, blbr)/23.08
  dB = distance(tlbl, trbr)/23.08


  cv2.putText(resize, "{:.1f}cm".format(dA), (int(tltr[0]-20), int(tltr[1]-10)) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
  cv2.putText(resize, "{:.1f}cm".format(dB), (int(trbr[0]+10), int(trbr[1])) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)


  total += 1
  cv2.imshow("Output", resize)
  cv2.waitKey(0)


cv2.destroyAllWindows()
cv2.putText(resize, "Total Object: {}".format(total), ( resize.shape[1]-200, resize.shape[0]-15) , cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 2)
cv2.imshow("Output", resize)
cv2.waitKey(0)
