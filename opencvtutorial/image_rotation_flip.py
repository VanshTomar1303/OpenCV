import cv2

image = cv2.imread('/home/vanshtomar/Documents/guts.webp')

if image is not None:

    # rotation
    h, w, c = image.shape

    center = ((w//2), (h//2))

    matrix_formula_to_rotate_image = cv2.getRotationMatrix2D(center, 40, 1.0)
    rotated_image = cv2.warpAffine(image, matrix_formula_to_rotate_image, (w, h))

    cv2.imshow('Image Viewer', rotated_image)

    # flip
    flip_horizontal = cv2.flip(image, 1)
    flip_vertical = cv2.flip(image, 0)
    flip_both = cv2.flip(image, -1)

    cv2.imshow('Image Viewer1', flip_vertical)
    cv2.imshow('Image Viewer2', flip_horizontal)
    cv2.imshow('Image Viewer3', flip_both)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image is not loaded")