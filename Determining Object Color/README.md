## DETERMINING OBJECT COLOR

The following steps will be followed in this project:
- Setting the picture size to 300px width.
- With GaussianBlur, the picture is blurred a bit.
- With the cvtColor method, the picture is first converted to gray and then to the LAB color format.
- With threshold, the threshold values ​​in the picture are determined.
- With findContours, there are the coordinates of the objects in the picture.
- With the moments method, the midpoint of each object is determined.
- The shape of the object is determined by the detect_shape method. [1]
- The color of the object is determined with the detect_color method. [2]
- DrawContours draw the borders of the object.
- With putText, the desired text is entered on the object.

[1] The detect_shape method follows these steps, respectively:
- Curve length is calculated by arcLength.
- The coordinates of the object corners are calculated depending on the curve length calculated with approxPolyDP.
- The shape name is returned depending on the number of corners calculated based on the above operations.

[2] The detect_color method follows these steps, respectively:
- A dict named colors is being created. In this dict, 3 primary colors and valuable ones are entered.
- A 3x1x3 matrix is ​​created with the zeros method.
- The matrix created with the for loop is assigned the values ​​in the dict that we create as colors (lab).
- converting lab matrix from RGB format to LAB format.
- With the zeros method, a mask in image dimensions is created (mask).
- With the location of previously found objects, each object is clipped one by one (other than the selected object is black).
- With the erosion, the edges of the object are made clear.
- Getting the color average of the object (according to the LAB format).
- The euclidean distance is applied between the values ​​in the colors dict created earlier with the received color average.
- According to the Euclidean distance result, the color of the object is closer to which value.
  For example: (137,211,87). According to the values ​​on the side, this object is blue.