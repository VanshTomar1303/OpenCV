import cv2

image = cv2.imread('/home/vanshtomar/Documents/guts.webp')

if image is not None:

    cropped_image = image[10:80, 10:50]

    cv2.imshow('Image Viewer', cropped_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image is not loaded")