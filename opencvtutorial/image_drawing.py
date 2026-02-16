import cv2

image = cv2.imread('/home/vanshtomar/Documents/guts.webp')

if image is None:
    print('Could not open or find the image.')
else:
    print('Image loaded successfully.')
 
    cv2.line(image, (10, 20), (300, 30), (67, 200, 60), 20)
    cv2.rectangle(image, (10, 300), (300, 50), (67, 100, 60), 20)
    cv2.circle(image, (100, 50), 50, (167, 100, 60), 10)
    cv2.putText(image, "Berserk", (100, 200), 2, 4, (167, 100, 60), 10)

    cv2.imshow('Image Viewer', image) 

    cv2.waitKey(0)
    cv2.destroyAllWindows()