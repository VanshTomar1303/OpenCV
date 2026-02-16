"""
Docstring for opencvtutorial.find_draw_contour

contour is nothing but point of a image that holds the sape of the object  like tringle have 3 vertices.

"""

import cv2 

image = cv2.imread('/home/vanshtomar/Documents/triangle.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

if image is None:
    print("Image not found.")
else:

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(image, contours, -1, (67, 30, 100), 10)

    for contour in contours:
    # detect shapes
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        corners = len(approx)
        if corners == 3:
            shape_name = "Triangle"

        cv2.drawContours(image, [approx], 0, (67, 30, 100), 10)

    cv2.putText(image, shape_name, (100, 100), 4, 10, (40, 20, 10), 10)
    cv2.imshow("image", image)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

