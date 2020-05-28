import cv2
import numpy as np


def detect_faces():
        '''
        Detecting faces on pictures,
        and draws a rect on them;
        '''

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

        video = cv2.VideoCapture('rtsp://192.168.178.99:554/11')
        video.set(3, 640)   # First stream: 1280; Second: 640
        video.set(4, 352)   # First: 720; Second: 352

        minW = 0.1 * video.get(3)
        minH = 0.1 * video.get(4)
        #print(minW)
        #print(minH)

        #while video.isOpened():
        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                    gray,
                    #frame,
                    scaleFactor=1.3,
                    minNeighbors=3,
                    minSize=(int(minW), int(minH)),
                    #minSize=(40, 40),
                    #flags=cv2.CASCADE_SCALE_IMAGE,
                    )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255,0,0),1)

                glasses = glasses_cascade.detectMultiScale(roi_gray)
                for (gx, gy, gw, gh) in glasses:
                    cv2.rectangle(roi_color, (gx, gy), (gx+gw, gy+gh), (0,0,255),1)

            cv2.imshow('Video', frame)

            k = cv2.waitKey(10)
            if k == 27:
                break

                video.release()
                cv2.destroyAllWindows()


if __name__ == '__main__':

    detect_faces()
