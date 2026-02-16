import cv2

image_path = None
image = None

while True:
    ch = input("Enter your choice: ")
    print("1. image path")
    print("2. show image")
    print("3. quit")

    if ch == '1':
        image_path = input("Enter image path: ")
    elif ch == '2':
        image = cv2.imread(image_path)

        if image is not None:
            cv2.imshow("Image Viewer", image)


            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else: 
            print("Image is not loaded")
    elif ch == '3':
        break