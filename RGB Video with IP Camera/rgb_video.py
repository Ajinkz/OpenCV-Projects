# import the necessary packages
import numpy as np
import cv2
import numpy as np
import time

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

url = "http://192.168.1.39:8080/video" # for IP Camera URL
cap = cv2.VideoCapture(url)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

writer = None
(h,w) = (None,None)
zeros = None

while(True):
    ret, frame = cap.read()
    frame = resize(frame,width=300)
    if writer is None:
    	(h,w) = frame.shape[:2]
    	writer = cv2.VideoWriter("./output/deneme.mp4",fourcc,20,(w * 2, h * 2), True)
    	zeros = np.zeros((h,w), dtype='uint8')

    (B,G,R) = cv2.split(frame)
    R = cv2.merge([zeros, zeros, R])
    G = cv2.merge([zeros, G, zeros])
    B = cv2.merge([B, zeros, zeros])

    output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
    output[0:h, 0:w] = frame # TOP-LEFT
    output[0:h, w:w * 2] = R # TOP-RIGHT
    output[h:h * 2, 0:w] = B # BOTTOM-LEFT
    output[h:h * 2, w:w * 2] = G # BOTTOM-RIGHT

    writer.write(output)

    cv2.imshow("Part Time", output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('Finish')
cap.release()
cv2.destroyAllWindows()
writer.release()
