## Intelligent Optical Reading

<img src="https://i.ibb.co/xXrtPKZ/d44688da813d35448950d7b3c2ce55b5.jpg" width="100%"/>

**What is an optical reader?** <br>
The optical reader is a computer input unit that transmits information to the computer by reading the ticked boxes in predetermined locations on a printed paper. Thanks to these optical readers, a control process that can take a very long time to read can be completed in seconds.

In this project, the same logic is followed. The boxes marked by the person who takes the exam on optical paper are determined by image-processing methods.
Then correct and incorrect answers are checked and the score is calculated.

---

**The following steps will be followed in this project:**
- First of all, the optical form is detected and converted in perspective. (review this project: [Document Scanner](https://github.com/Furkan-Gulsen/OpenCV-Projects/tree/master/Document%20Scanner))
- Necessary procedures are applied to detect boxes (balloons) on the optical form..
  - threshold
  - boundingRect
  - area constraint (to prevent detection of smaller objects than the box area)
- Then the detected boxes are lined from top to bottom.(review this project: [Sorting Contours](https://github.com/Furkan-Gulsen/OpenCV-Projects/tree/master/Sorting%20Contours))
- Finally, the data from the optical form is compared with the answer key and the result is calculated.
