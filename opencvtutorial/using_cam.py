import cv2

cap = cv2.VideoCapture(0) # read data from camera

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

codec = cv2.VideoWriter_fourcc(*'XVID')

recoder = cv2.VideoWriter("helllo.avi", codec, 20, (frame_width, frame_height))

while True:

    success, frame = cap.read() # success = True/False ,frame = image

    if not success:
        print("Couldn't capture the camera.")
        break

    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    recoder.write(frame)

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
recoder.release()
cv2.destroyAllWindows()