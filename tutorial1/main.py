import cv2
import mediapipe as mp
import os
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ===============================
# Load HandLandmarker Model
# ===============================

model_path = os.path.join(os.path.dirname(__file__), "../hand_landmarker.task")

base_options = python.BaseOptions(model_asset_path=model_path)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

# ===============================
# Start Camera
# ===============================

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# ===============================
# Hand Connections
# ===============================

connections = [
    (0,1),(1,2),(2,3),(3,4),      # Thumb
    (0,5),(5,6),(6,7),(7,8),      # Index
    (0,9),(9,10),(10,11),(11,12), # Middle
    (0,13),(13,14),(14,15),(15,16), # Ring
    (0,17),(17,18),(18,19),(19,20)  # Pinky
]

# ===============================
# Drawing Variables
# ===============================

canvas = None
prev_x, prev_y = 0, 0
draw_color = (0, 0, 255)
brush_thickness = 6


def main():
    global canvas, prev_x, prev_y
    cv2.namedWindow("🔥 Air Sketch", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("🔥 Air Sketch",
                      cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)

    print("🔥 Air Sketch App Running... Press Q to quit")

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)

        # Initialize canvas once
        if canvas is None:
            canvas = np.zeros_like(img)

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = detector.detect(mp_image)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:

                h, w, _ = img.shape

                # ===============================
                # Draw Skeleton
                # ===============================
                # for landmark in hand_landmarks:
                #     cx = int(landmark.x * w)
                #     cy = int(landmark.y * h)
                #     cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)

                # for start_idx, end_idx in connections:
                #     x1 = int(hand_landmarks[start_idx].x * w)
                #     y1 = int(hand_landmarks[start_idx].y * h)

                #     x2 = int(hand_landmarks[end_idx].x * w)
                #     y2 = int(hand_landmarks[end_idx].y * h)

                #     cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # ===============================
                # Drawing Logic
                # ===============================

                index_tip = hand_landmarks[8]
                index_joint = hand_landmarks[6]

                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                joint_y = int(index_joint.y * h)

                # If index finger is UP → draw
                if y < joint_y:

                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = x, y

                    cv2.line(canvas, (prev_x, prev_y), (x, y),
                             draw_color, brush_thickness)

                    prev_x, prev_y = x, y

                else:
                    prev_x, prev_y = 0, 0

                # ===============================
                # Clear Canvas (3 fingers up)
                # ===============================

                middle_tip = hand_landmarks[12]
                middle_joint = hand_landmarks[10]

                ring_tip = hand_landmarks[16]
                ring_joint = hand_landmarks[14]

                if (int(middle_tip.y * h) < int(middle_joint.y * h) and
                    int(ring_tip.y * h) < int(ring_joint.y * h)):

                    canvas = np.zeros_like(img)

        # Merge canvas with camera feed
        combined = cv2.addWeighted(img, 0.7, canvas, 1, 0)

        cv2.imshow("🔥 Air Sketch", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()