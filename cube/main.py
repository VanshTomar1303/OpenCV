import cv2
import mediapipe as mp
import numpy as np
import math
import os
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ===============================
# Load HandLandmarker
# ===============================

model_path = os.path.join(os.path.dirname(__file__), "../hand_landmarker.task")

base_options = python.BaseOptions(model_asset_path=model_path)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

# 3D Cube Points
base_points = np.array([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
])

cubes = []  # store cube positions
angle_x = 0
angle_y = 0
last_spawn_time = 0

def rotate(points, ax, ay):
    rx = np.array([
        [1, 0, 0],
        [0, math.cos(ax), -math.sin(ax)],
        [0, math.sin(ax), math.cos(ax)]
    ])
    
    ry = np.array([
        [math.cos(ay), 0, math.sin(ay)],
        [0, 1, 0],
        [-math.sin(ay), 0, math.cos(ay)]
    ])
    
    return np.dot(points, rx).dot(ry)

def project(points, offset_x, offset_y):
    projected = []
    for point in points:
        x = int(point[0] * 80 + offset_x)
        y = int(point[1] * 80 + offset_y)
        projected.append([x, y])
    return projected

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:

            # Landmarks
            index_tip = hand_landmarks[8]
            index_pip = hand_landmarks[6]

            middle_tip = hand_landmarks[12]
            middle_pip = hand_landmarks[10]

            ring_tip = hand_landmarks[16]
            ring_pip = hand_landmarks[14]

            pinky_tip = hand_landmarks[20]
            pinky_pip = hand_landmarks[18]

            # Convert to pixel coords
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            mx, my = int(middle_tip.x * w), int(middle_tip.y * h)

            # Finger up detection
            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y
            ring_up = ring_tip.y < ring_pip.y
            pinky_up = pinky_tip.y < pinky_pip.y

            # 👆 One finger → rotate
            if index_up and not middle_up:
                angle_y = (ix - w // 2) * 0.01
                angle_x = (iy - h // 2) * 0.01

            # ✌️ Two fingers → spawn cube
            if index_up and middle_up and not ring_up and not pinky_up:
                current_time = time.time()
                if current_time - last_spawn_time > 1:  # cooldown
                    cubes.append((ix, iy))
                    last_spawn_time = current_time

    # Draw all cubes
    for cube_pos in cubes:
        rotated = rotate(base_points, angle_x, angle_y)
        projected = project(rotated, cube_pos[0], cube_pos[1])

        edges = [
            (0,1),(1,2),(2,3),(3,0),
            (4,5),(5,6),(6,7),(7,4),
            (0,4),(1,5),(2,6),(3,7)
        ]

        for edge in edges:
            cv2.line(frame, projected[edge[0]], projected[edge[1]], (0,255,0), 2)

    cv2.imshow("Multi Cube Gesture Engine", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()