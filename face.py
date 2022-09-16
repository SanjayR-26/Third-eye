import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import pickle
import time
import sys

import speak as s
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
np.set_printoptions(threshold=sys.maxsize)

class Face():
    def __init__(self):
        self.pickle_off = open("datafile.txt", "rb")
        self.data = pickle.load(self.pickle_off)
        self.known_face_names = list(self.data.keys())
        self.known_face_encodings = list(self.data.values())
        self.names =[] 
        self.speak_engine = s.Speak()
        print("Loaded: Face engine")

    def encode(self):
        self.path = 'faces'
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)
        for cl in self.myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
        print(self.classNames)
        self.encodeList = self.findEncodings(self.images)
        self.dictionary = dict(zip(self.classNames, self.encodeList))
        with open('datafile.txt', 'wb') as fh:
            pickle.dump(self.dictionary, fh)
    def findEncodings(self, images):
        self.encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.encode = face_recognition.face_encodings(img)[0]
            self.encodeList.append(self.encode)
        return self.encodeList
    
    def recognize_face(self, img=None): 
        if img is not None:
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.facesCurFrame = face_recognition.face_locations(imgS)
            self.encodesCurFrame = face_recognition.face_encodings(imgS,self.facesCurFrame)    
            if self.facesCurFrame:
                for encodeFace,faceLoc in zip(self.encodesCurFrame,self.facesCurFrame):
                    self.matches = face_recognition.compare_faces(self.known_face_encodings,encodeFace)
                    self.faceDis = face_recognition.face_distance(self.known_face_encodings,encodeFace)
                    #print(faceDis)
                    self.matchIndex = np.argmin(self.faceDis)                    
                    if self.faceDis[self.matchIndex]< 0.50:  
                        self.names.append(str(self.known_face_names[self.matchIndex]))
                    else: 
                        return "Cannot recognize person"           
                return self.names
            else:
                return "No faces Detected"   
        else:  
            self.speak_engine.speak("Stay Steady.")
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
            time.sleep(0.5)
            if cap.isOpened():
                success, img = cap.read()
                imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.facesCurFrame = face_recognition.face_locations(imgS)
                self.encodesCurFrame = face_recognition.face_encodings(imgS,self.facesCurFrame)    
                if self.facesCurFrame:
                    for encodeFace,faceLoc in zip(self.encodesCurFrame,self.facesCurFrame):
                        self.matches = face_recognition.compare_faces(self.known_face_encodings,encodeFace)
                        self.faceDis = face_recognition.face_distance(self.known_face_encodings,encodeFace)
                        #print(faceDis)
                        self.matchIndex = np.argmin(self.faceDis)                    
                        if self.faceDis[self.matchIndex]< 0.50:  
                            self.names.append(str(self.known_face_names[self.matchIndex]))
                        else: 
                            return "Cannot recognize person"           
                    return self.names
                else:
                    return "No faces Detected"   
            cap.release()
      
            

    def add_face(self, name):
        self.speak_engine.speak("Stay still, taking photo")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
        time.sleep(0.5)
        if self.cap.isOpened():
            success, img = self.cap.read()
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.path = 'faces'
        cv2.imwrite(f'{self.path}/{name}.jpg', imgS)
        print('Pushed')
        self.encode()

if __name__ == "__main__":
    Face()