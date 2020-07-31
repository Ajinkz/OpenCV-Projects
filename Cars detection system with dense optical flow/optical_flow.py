import cv2
import numpy as np

video = cv2.VideoCapture("traffic.mp4")

# read first frame
ret, first_frame = video.read()

# scale and resize image
resize_dim = 720
max_dim = max(first_frame.shape) # 1280
scale = resize_dim/max_dim

# fx => scale factor along the horizontal axis
# fy => scale factor along the vertical axis
first_frame = cv2.resize(first_frame, None, fx=scale, fy=scale, interpolation = cv2.INTER_AREA)

# convert to gray scale
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# create mask 
mask = np.zeros_like(first_frame) # example: 1. 2. 3. => np.zeros_like => 0. 0. 0.
mask[...,1] = 255 # 255:white

# save video
out = cv2.VideoWriter("video.mp4",-1,1,(500,500))

while(video.isOpened()):
    # read a frame video
    ret, frame = video.read()
    
    # convert new frame format's to gray scale and resize gray frame obtained
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=scale, fy=scale)
    
    # calculate dense optical flow by farneback method
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, pyr_scale = 0.5, levels = 5, winsize = 11, 
                                        iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
    # prev:     :	first 8-bit single-channel input image.
    # next:     :	second input image of the same size and the same type as prev.
    # flow:     :	computed flow image that has the same size as prev and type CV_32FC2.
    # pyr_scale :	parameter, specifying the image scale (<1) to build pyramids for each image; 
    #               pyr_scale=0.5 means a classical pyramid, where each next layer is twice smaller 
    #               than the previous one.
    # levels	  : number of pyramid layers including the initial image; levels=1 means that no 
    #               extra layers are created and only the original images are used.
    # winsize	  : averaging window size; larger values increase the algorithm robustness to image
    #               noise and give more chances for fast motion detection, but yield more blurred 
    #               motion field.
    # iterations:	number of iterations the algorithm does at each pyramid level.
    # poly_n	  : size of the pixel neighborhood used to find polynomial expansion in each pixel;
    #               larger values mean that the image will be approximated with smoother surfaces,
    #               yielding more robust algorithm and more blurred motion field, typically poly_n =5 or 7.
    # poly_sigma:	standard deviation of the Gaussian that is used to smooth derivatives used as a basis
    #               for the polynomial expansion; for poly_n=5, you can set poly_sigma=1.1, for poly_n=7, 
    #               a good value would be poly_sigma=1.5.
    
    # calculates the magnitude and angle of 2D vectors
    magnitude, angle = cv2.cartToPolar(flow[...,0],flow[...,1])
    # x – array of x-coordinates; this must be a single-precision or double-precision floating-point array.
    # y – array of y-coordinates, that must have the same size and same type as x.
    # magnitude – output array of magnitudes of the same size and type as x.
    # angle – output array of angles that has the same size and type as x; the angles are measured in 
    #         radians (from 0 to 2*Pi) or in degrees (0 to 360 degrees).
    # angleInDegrees – a flag, indicating whether the angles are measured in radians (which 
    #         is by default), or in degrees.
    
    # set image hue according to the optical flow direction
    mask[...,0] = angle * 180 / np.pi / 2
    
    # set image value according to the optical flow magnitude
    mask[...,2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    
    # convert HSV to RGB (BGR) color representation
    rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    
    # resize frame size to match dimensions
    frame = cv2.resize(frame, None, fx=scale, fy=scale)
    
    # open a new window and displays the output frame
    dense_flow = cv2.addWeighted(frame, 1, rgb, 2, 0)
    cv2.imshow("Video", dense_flow)
    out.write(dense_flow)
    
    # Update previous frame
    prev_gray = gray
    
    # Frame are read by intervals of 1 millisecond. The programs breaks out of the while loop when the user presses the 'q' key
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
# The following frees up resources and closes all windows
video.release()
cv2.destroyAllWindows()
    

    