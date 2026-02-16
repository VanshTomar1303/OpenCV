# ================= IMPORTS =================

import cv2                         # OpenCV for camera + drawing
import mediapipe as mp             # MediaPipe main package
from mediapipe.tasks import python # New MediaPipe Tasks API
from mediapipe.tasks.python import vision  # Vision models (HandLandmarker)
import numpy as np                 # For creating canvas (array operations)
import os                          # For handling file paths
import math                        # For distance calculation
import time                        # For color change delay & saving filename


# ================= LOAD MODEL =================

# Build full path to hand_landmarker.task file
model_path = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")

# Configure base options and tell MediaPipe where model file is
base_options = python.BaseOptions(model_asset_path=model_path)

# Configure HandLandmarker settings
options = vision.HandLandmarkerOptions(
    base_options=base_options,   # Load our model
    num_hands=1                  # Detect only one hand
)

# Create actual hand detector from options
detector = vision.HandLandmarker.create_from_options(options)


# ================= CAMERA SETUP =================

cap = cv2.VideoCapture(0)  # Open default webcam (0 = primary camera)
cap.set(3,1280)
cap.set(4,720)

ret, frame = cap.read()    # Capture one frame to get resolution
canvas = np.zeros_like(frame)  # Create blank black canvas same size as frame


# ================= DRAWING VARIABLES =================

prev_x, prev_y = 0, 0      # Store previous finger position (for smooth lines)

draw_color = (255, 0, 255) # Default drawing color (purple in BGR)
brush_thickness = 5        # Thickness of drawing line
eraser_thickness = 40      # Thickness of eraser circle

last_color_change = 0      # Timestamp of last color change
colors = [(255,0,255),(255,0,0),(0,255,0),(0,255,255)]  # Available colors
color_index = 0            # Current color index


# ================= HELPER FUNCTIONS =================

def finger_up(lm_list, tip, joint):
    # Returns True if finger tip is above joint (finger is up)
    return lm_list[tip][1] < lm_list[joint][1]


def distance(p1, p2):
    # Calculate Euclidean distance between two points
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])


# ================= MAIN LOOP =================

while True:

    ret, frame = cap.read()  # Capture frame from webcam
    if not ret:
        break                # Stop if camera fails

    frame = cv2.flip(frame, 1)  # Mirror image (more natural interaction)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR → RGB (MediaPipe needs RGB)

    # Convert numpy image to MediaPipe Image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    # Run hand detection
    result = detector.detect(mp_image)


    # ================= IF HAND DETECTED =================

    if result.hand_landmarks:

        hand_landmarks = result.hand_landmarks[0]  # Get first detected hand

        h, w, _ = frame.shape  # Get frame height & width

        # Convert normalized landmarks (0–1) to pixel coordinates
        lm_list = [(int(lm.x*w), int(lm.y*h)) for lm in hand_landmarks]


        # Check each finger state (True or False)
        thumb_up  = finger_up(lm_list, 4, 3)
        index_up  = finger_up(lm_list, 8, 6)
        middle_up = finger_up(lm_list, 12, 10)
        ring_up   = finger_up(lm_list, 16, 14)
        pinky_up  = finger_up(lm_list, 20, 18)

        # Count how many non-thumb fingers are up
        total_fingers = sum([index_up, middle_up, ring_up, pinky_up])


        # ================= PINCH TO DRAW =================

        # Measure distance between thumb tip and index tip
        pinch_distance = distance(lm_list[4], lm_list[8])

        x, y = lm_list[8]  # Index finger tip coordinates

        if pinch_distance < 40:   # If thumb & index are close → drawing mode

            cv2.circle(frame, (x,y), 10, (0,255,0), -1)  # Draw green dot on finger

            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y  # Initialize previous position

            # Draw line from previous position to current position
            cv2.line(canvas, (prev_x, prev_y), (x,y), draw_color, brush_thickness)

            prev_x, prev_y = x, y  # Update previous position

        else:
            prev_x, prev_y = 0, 0  # Reset if not pinching


        # ================= CHANGE COLOR (2 Fingers) =================

        if index_up and middle_up and not ring_up:
            # Prevent rapid switching using 1-second delay
            if time.time() - last_color_change > 1:
                color_index = (color_index + 1) % len(colors)  # Cycle colors
                draw_color = colors[color_index]
                last_color_change = time.time()


        # ================= ERASER MODE (3 Fingers) =================

        if index_up and middle_up and ring_up:
            cv2.circle(frame, (x,y), 15, (0,0,0), -1)  # Show eraser circle
            cv2.circle(canvas, (x,y), eraser_thickness, (0,0,0), -1)  # Erase on canvas


    # ================= MERGE CANVAS WITH FRAME =================

    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)  # Convert canvas to grayscale

    _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)  # Create mask

    mask_inv = cv2.bitwise_not(mask)  # Invert mask

    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)  # Remove drawing from frame
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)   # Extract drawing

    final = cv2.add(frame_bg, canvas_fg)  # Combine both images


    # ================= DRAW UI BAR =================

    cv2.rectangle(final, (0,0), (640,60), (50,50,50), -1)  # Top UI bar

    # Draw color circles
    for i, color in enumerate(colors):
        cv2.circle(final, (50 + i*60, 30), 20, color, -1)

    # Instructions text
    cv2.putText(final, "S: Save  C: Clear  Q: Quit",
                (200,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)


    # ================= SHOW WINDOW =================

    cv2.imshow("AI Paint App", final)


    # ================= KEY CONTROLS =================

    key = cv2.waitKey(1) & 0xFF  # Capture key press

    if key == ord('c'):
        canvas = np.zeros_like(frame)  # Clear drawing

    if key == ord('s'):
        filename = f"drawing_{int(time.time())}.png"
        cv2.imwrite(filename, final)   # Save image
        print("Saved as", filename)

    if key == ord('q'):
        break  # Exit program


# ================= CLEANUP =================

cap.release()         # Release webcam
cv2.destroyAllWindows()  # Close all OpenCV windows