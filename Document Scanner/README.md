## DOCUMENT SCANNER


**The following steps will be followed in this project:**
- First, necessary adjustments are made to detect the document in the photo.
  - resize (width:500px)
  - cvtColor --> gray
  - GaussianBlur
  - Canny
- Contours in the photo are determined.
- Objects are detected with the determined contours.
- The object with 4 edges among the detected objects is determined as document.
- The 4 corners of the specified document have coordinates.
- Flattening adjustment is made by using the getPerspectiveTransform method ie found coordinates.
- Finally, the scanner operation is successfully performed with the warpPerspective method.

**Output Images:**
<img src="https://i.ibb.co/FHK4mwn/output1.jpg" />
<img src="https://i.ibb.co/6v6x92H/output2.jpg" />
<img src="https://i.ibb.co/qsv5NN1/output3.jpg" />
