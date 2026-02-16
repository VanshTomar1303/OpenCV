import cv2 

image = cv2.imread('/home/vanshtomar/Documents/guts.webp', cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Image not found.")
else:

    edges = cv2.Canny(image, 50, 150)

    cv2.imshow("Line", edges)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

