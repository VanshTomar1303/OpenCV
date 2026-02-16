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
    num_hands=2
)

detector = vision.HandLandmarker.create_from_options(options)


cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

prev_x, prev_y = 0, 0
draw_color = (255, 129, 150)
brush_thickness = 3

def main():
    global prev_x, prev_y
    while True:
        success, image = cap.read()

        if not success:
            break
        
        img = cv2.flip(image, 1)

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = detector.detect(mp_image)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                h, w, _ = img.shape

                index_tip = hand_landmarks[8]
                index_joint = hand_landmarks[6]

                ix = int(index_tip.x * w)
                iy = int(index_tip.y * h)

                ijoint_y = int(index_joint.y * h)

                # If index finger is UP → draw
                if iy < ijoint_y:
                    cv2.circle(img, (ix, iy - 50), 40, (0, 255, 0), -1)

                middle_tip = hand_landmarks[12]
                middle_joint = hand_landmarks[11]

                mx = int(middle_tip.x * w)
                my = int(middle_tip.y * h)

                mjoint_y = int(middle_joint.y * h)

                # If middle finger is UP → draw
                if my < mjoint_y:
                    cv2.rectangle(img, (mx, my - 50), (100, 100), (196, 55, 0), -1)

        cv2.imshow("Shape Maker", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()