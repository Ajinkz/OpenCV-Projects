## Object Tracking
The goal here is to follow the color object we identified in the video. This shows the path followed during the tracking in red.

**The following steps will be followed in this project:**
- First we need to determine the color scale. For this, you can look at the color codes of the object in the shadow and the light in the object. It will be written in the second parameter of the inRange method in the shadow, and in the third parameter of the inRange method in the light. The 1st parameter of the inRange method is the HSV transformed image.
- FindContours method detects the objects in the image. The detected objects are circled. The object whose radius is more than the length we specify is the object that we want to detect. Until this part, we were able to detect the object in the image.
- The detected object is indicated by a circle with colored edges around it. Likewise, the center point of the object is indicated by a dot.
- The coordinates that the object passes are kept in an array up to a certain point and the points where the object passes are shown in red.
