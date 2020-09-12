import cv2
import argparse
from pyzbar.pyzbar import decode, ZBarSymbol
from Helpers import *

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Image path")
args = vars(ap.parse_args())

im = cv2.imread(args['image'])

codes = decode(im)
print('Decoded:', codes)

for code in codes:
    data = code.data.decode('ascii')
    print('Data:', data)
    print('Code Type:', code.type)
    print('BBox:', code.rect)
    x, y, w, h = code.rect.left, code.rect.top, code.rect.width, code.rect.height
    cv2.rectangle(im, (x,y),(x+w, y+h),(55, 0, 193), 8)

    print('Polygon:', code.polygon)
    txt = '(' + code.type + ')  ' + data
    cv2.putText(im, txt, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 50, 255), 2)

text1 = 'No. Codes: %s' % len(codes)
cv2.putText(im, text1, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow('bounding box', Helpers.resize(im, 600) )
cv2.waitKey(0)
cv2.destroyAllWindows()