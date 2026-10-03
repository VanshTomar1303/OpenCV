import cv2
import numpy as np

# black image
img = np.zeros((500,500,3),dtype=np.uint8)

print(img.shape)

cv2.line(img, (100,100), (400,300), (0,255,0), 2)
cv2.rectangle(img, (50,50), (300,300), (255,0,0), -1)
cv2.circle(img,(200,200),50,(60,132,30),-1)
cv2.ellipse(img,(200,325),(40,50),5,0,360,(255,0,0),-1)

points = np.array([
    [250,50],
    [0,400],
    [400,400]
])

cv2.polylines(img,points,False,(0,255,0),2)
cv2.fillPoly(img,[points],(0,255,0))

cv2.putText(img,"hello",(100,100),cv2.FONT_HERSHEY_COMPLEX,1.5,(125,200,0),3,cv2.LINE_AA)

cv2.imshow("Black", img)

cv2.waitKey(0)
cv2.destroyAllWindows()