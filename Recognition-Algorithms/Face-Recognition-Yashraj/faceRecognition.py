import numpy as np
import cv2
import os

data_path = 'C:/Users/Yashraj/Desktop/faces/'
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


labels = []
faces = []

for i, images in enumerate(os.listdir(data_path)):
    img_path = data_path + images
    face = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    faces.append(np.asarray(face, dtype=np.uint8))
    labels.append(i)

model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(faces), np.asarray(labels))
print("Model Training Completed")


def face_detection(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray, 1.5, 5)
    
    if face is ():
        return img, []
    
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi = gray[y:y + h, x:x + w]
    return img, roi


def probability(img):

    result = model.predict(img)
    probability = (1 - (result[1]/500))*100;
    return probability;



cap = cv2.VideoCapture(0)

while True:

    _, frame = cap.read()
    frame, face = face_detection(frame)

    try:
        confidence = probability(face)
        if int(confidence) > 80:
            cv2.putText(frame, str(confidence)+"% Same User", (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        else:
            cv2.putText(frame, str(confidence) + "Not a same User", (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

    except:
        cv2.putText(frame, "Face not Found", (100, 200),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow('img', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

