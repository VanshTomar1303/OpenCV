import cv2

image = cv2.imread('/home/vanshtomar/Documents/guts.webp')

if image is None:
    print('Could not open or find the image.')
else:
    print('Image loaded successfully.')
    h, w, c = image.shape # to get the dimensions of the image (height, width, channels)
    print(f'Image dimensions: {h}x{w} pixels, Channels: {c}')

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # to convert the image to grayscale

    cv2.imshow('Image Viewer', gray_image) # to display the image in a window
    # cv2.imwrite('output_image.jpg', image) # to save the image to disk
    cv2.waitKey(0)
    cv2.destroyAllWindows()