import numpy as np
import cv2

img = cv2.imread('balon.jpg')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,150,205,1)

image, contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
img = cv2.drawContours(img, contours, -1, (0,255,0), 5)


diff = cv2.absdiff(image, img)
_ , thresholded = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
conv_hull = cv2.convexHull(thresholded)

for cnt in contours:
    (x, y, w, h) = cv2.boundingRect(cnt);
    print("x: ", x)
    print("y: ", y)
    print("w: ", w)
    print("h: ", h)


cv2.imshow("conv_hull",conv_hull)
cv2.imshow("balon",img)