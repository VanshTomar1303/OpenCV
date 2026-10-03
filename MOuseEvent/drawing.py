import cv2
import numpy as np  

image = np.zeros((800,800,3), dtype=np.uint8)

drawing = False
erase = False
previous_pos = None
color = (0,255,0)

def mouse_callback(event,x,y,flags,param):
    
    global drawing
    global previous_pos
    global color
    global erase
    
    # Erase
    if event == cv2.EVENT_RBUTTONDOWN:
        erases = True
        previous_pos = (x,y)
        
    if event == cv2.EVENT_MOUSEMOVE and erase:
        current_pos = (x,y)
        
        cv2.line(image, previous_pos, current_pos, (0,0,0), 1, cv2.LINE_AA)
        
        previous_pos = current_pos
        
    if event == cv2.EVENT_RBUTTONUP:
        erase = False
        previous_pos = None
        
    # DRAW
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        previous_pos = (x,y)
        
    if event == cv2.EVENT_MOUSEMOVE and drawing:
        current_pos = (x,y)
        
        cv2.line(image, previous_pos, current_pos, color, 1, cv2.LINE_AA)
        
        previous_pos = current_pos
        
    if event == cv2.EVENT_LBUTTONUP:
        drawing = False
        previous_pos = None

cv2.namedWindow("Paint")
cv2.setMouseCallback("Paint",mouse_callback)

while True:
    cv2.imshow("Paint", image)
    
     # Capture the pressed key
    key = cv2.waitKey(1) & 0xFF

    # 3. Listen for color change key presses (OpenCV uses BGR, not RGB!)
    if key == ord('r'):
        color = (0, 0, 255)  # Red
    elif key == ord('g'):
        color = (0, 255, 0)  # Green
    elif key == ord('c'):
        image[0:] = [0,0,0]
    elif key == ord('b'):
        color = (255, 0, 0)  # Blue
    
    # Exit condition
    elif key == ord('q'):
        break
    
cv2.destroyAllWindows()