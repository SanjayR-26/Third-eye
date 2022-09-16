import cv2
import mediapipe as mp
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


class handDetector():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.model = load_model('dependancies/mp_hand_gesture')
        f = open('dependancies/gesture.names', 'r')
        self.classNames = f.read().split('\n')
        f.close()
        print("Loaded: Gesture detection engine")

    def draw_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    def find_hands(self, img, handNo=0):
        lmList = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([cx, cy])
        return lmList
 

    def recognize_gesture(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
        if cap.isOpened():
            success, img = cap.read()
            landmarks = self.find_hands(img)
            if landmarks:
                prediction = self.model.predict([landmarks])
                print(prediction)
                classID = np.argmax(prediction)
                className = self.classNames[classID]
                cap.release()
                return className
            return "No gesture"

if __name__ == "__main__":               
    handDetector()