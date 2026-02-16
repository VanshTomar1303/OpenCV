import cv2 

image = cv2.imread('/home/vanshtomar/Documents/guts.webp', cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Image not found.")
else:

    success, img = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)

    cv2.imshow("Line", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

