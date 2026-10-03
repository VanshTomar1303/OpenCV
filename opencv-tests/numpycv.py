import cv2
import numpy as np

# black image
img = np.zeros((500,500,3),dtype=np.uint8)

# red image
img[0:] = [0,0,255]

# rectangle
img[250:251,250:251] = [0,255,0]

cv2.imshow("Black", img)

cv2.waitKey(0)
cv2.destroyAllWindows()