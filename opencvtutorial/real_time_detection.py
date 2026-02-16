import cv2

face_detector = cv2.CascadeClassifier('opencvtutorial/haarcascade_frontalface_default.xml')
smile_detector = cv2.CascadeClassifier('opencvtutorial/haarcascade_smile.xml')
eye_detector = cv2.CascadeClassifier('opencvtutorial/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if not success:
        break
    
    faces = face_detector.detectMultiScale(gray, 1.1, 5)
    eyes = eye_detector.detectMultiScale(gray, 1.1, 20)
    smiles = smile_detector.detectMultiScale(gray, 1.1, 40)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, x+y), (255, 0, 0), 2)
    
    for (x, y, w, h) in eyes:
        cv2.rectangle(image, (x, y), (x+w, x+y), (0, 255, 0), 2)
    
    for (x, y, w, h) in smiles:
        cv2.rectangle(image, (x, y), (x+w, x+y), (0, 0, 255), 2)

    cv2.imshow("Detection: ", image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()