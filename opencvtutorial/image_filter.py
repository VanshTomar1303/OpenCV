import cv2

image = cv2.imread('/home/vanshtomar/Documents/guts.webp')

if image is None:
    print('Could not open or find the image.')
else:
    print('Image loaded successfully.')

    gaussien_blur_image = cv2.GaussianBlur(image, (5, 5), 10)
    median_blur_image = cv2.medianBlur(image, 5)
    sharp_image = cv2.filter2D(image, 2, 6)

    cv2.imshow('Image Viewer', gaussien_blur_image) 
    cv2.imshow('Image Viewer1', median_blur_image) 
    cv2.imshow('Image Viewer3', sharp_image) 

    cv2.waitKey(0)
    cv2.destroyAllWindows()