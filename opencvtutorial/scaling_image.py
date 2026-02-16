import cv2

image = cv2.imread('/home/vanshtomar/Documents/guts.webp')

if image is not None:

    resized_image = cv2.resize(image, (1280, 720))

    cv2.imshow('Image Viewer', resized_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image is not loaded")