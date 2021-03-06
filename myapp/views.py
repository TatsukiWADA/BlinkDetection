from django.shortcuts import render
from django.http import HttpResponse
import cv2
from django.http import StreamingHttpResponse
from mysite.settings import BASE_DIR

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        # カメラからフレーム画像を取得
        ret, rgb = self.video.read()

        # cascade_path = "templates" + "\haarcascade_frontalface_default.xml"

        # gry_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # cascade = cv2.CascadeClassifier(cascade_path)

        # face = cascade.detectMultiScale(gry_img, cv2.COLOR_BGR2GRAY)

        # rectange_color = (255,0,0)

        face_cascade_path = 'templates/haarcascade_frontalface_default.xml'
        eye_cascade_path = 'templates/haarcascade_eye.xml'

        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=3, minSize=(100, 100))

        # if len(faces) > 0:
        #     for rect in facerect:
        #         cv2.rectangle(image,tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),rectange_color,thickness=2)

        # for x, y, w, h in faces:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     face = frame[y: y + h, x: x + w]
        #     face_gray = frame_gray[y: y + h, x: x + w]
        #     eyes = eye_cascade.detectMultiScale(face_gray)
        #     for (ex, ey, ew, eh) in eyes:
        #         cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        if len(faces) == 1:
            x, y, w, h = faces[0, :]
            cv2.rectangle(rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 処理高速化のために顔の上半分を検出対象範囲とする
            eyes_gray = gray[y : y + int(h/2), x : x + w]
            eyes = eye_cascade.detectMultiScale(
                eyes_gray, scaleFactor=1.11, minNeighbors=3, minSize=(8, 8))

            for ex, ey, ew, eh in eyes:
                cv2.rectangle(rgb, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 255, 0), 1)

            if len(eyes) == 0:
                cv2.putText(rgb,"BlinDetection",
                    (10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)


        # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', rgb)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def index(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')