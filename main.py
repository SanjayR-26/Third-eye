import datetime
import wikipedia
from twilio.rest import Client
import time
import keyboard 

import listen as l
import speak as s
import handDetector as h
import detect as d
import face as f 
import read as r



class Main():
    def __init__(self):
        self.listen_engine = l.Listen()
        self.speak_engine = s.Speak()
        self.gesture_engine = h.handDetector()
        self.detection_engine = d.objectDetection()
        self.face_engine = f.Face()
        self.read_engine = r.Read()
        account_sid = 'ACfe31272fc48d208b3c68e77de8961e96'
        auth_token = '8157a821bda9b0b02cc7a6e8a1f1ca69'
        self.client = Client(account_sid, auth_token)

    def listen_background(self):
        while True:
            result = self.listen_engine.listen()
            if result == "None":
                continue
            else:
                return result
    def listen_name(self):
        self.speak_engine.speak("Say the name clearly.")
        result = self.listen_engine.listen()
        if result == "None":
                self.listen_name()
        return result
    def wishMe(self):
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            self.speak_engine.speak("Good Morning")
            print("Good Morning")
        elif hour>=12 and hour<18:
            self.speak_engine.speak("Good Afternoon")
            print("Good Afternoon")
        else:
            self.speak_engine.speak("Good Evening")
            print("Good Evening")
    def helpme(self):
        self.speak_engine.speak("Hold on!, sending message to your friends.")
        numlist = ['+919789056970']
        for i in numlist:
                message = self.client.messages.create(
                    body = "I'm in danger   Location : Easwari Engineering college, Ramapuram, Chennai, Tamilnadu, India",
                    from_='+17312514349',
                    to= i
                )
    
    def detect(self):
        results = self.detection_engine.detect_objects()
        if results == "No objects detected":
            self.speak_engine.speak(results)
        else:
            self.speak_engine.speak("Objects infront of you are: ")
            self.speak_engine.speak_list(results)

    def read(self):
        self.speak_engine.speak("Stay still, taking photo")
        string, lang = self.read_engine.recognize_text()
        print(string)
        self.speak_engine.speak(string, language = lang)


    def startAssistant(self):
        self.wishMe()
        while True: 
            command = self.listen_background()
            print("User command: " + command)
            if "good bye" in command or "ok bye" in command or "stop" in command or "goodbye" in command:
                self.speak_engine.speak('Turning off: Voice assistance')
                break
            if "hello" in command or "hi" in command or "good" in command :
                self.wishMe()
            elif 'time' in command:
                strTime=datetime.datetime.now().strftime("%H:%M:%S")
                self.speak_engine.speak(f"the time is {strTime}")
            elif 'help' in command:
                self.helpme()
            elif "who" in command:
                faces = self.face_engine.recognize_face()
                if faces == "Cannot recognize person" or faces == "No faces Detected" :
                    self.speak_engine.speak(faces)
                else:
                    self.speak_engine.speak("People infront of you are: ")
                    self.speak_engine.speak_list(faces)
            elif  "add" in command:
                name = self.listen_name()
                self.face_engine.add_face(name)
                self.speak_engine.speak("Added face successfully.")
            elif 'about' in command or "tell" in command:
                self.speak_engine.speak('Searching Wikipedia...')
                command =command.replace("tell me about", "")
                results = wikipedia.summary(command, sentences=3)
                self.speak_engine.speak("According to Wikipedia")
                print(type(results))
                self.speak_engine.speak(results)
            elif "detect objects" in  command or "object" in command or "objects" in command:
                self.detect()
            elif "read" in command:
                self.read()
            elif "phone number" in command or "phone" in command or "number" in command:
                number = self.read_engine.recognize_phonenumbers()
                print(number)
                self.speak_engine.speak_list(number)
            elif "medicine" in command or "board" in command or "product" in command or "menu" in command or "invoice" in ccommand or "bill" in command:
                specific = self.read_engine.recognize_specific()
                print(specific)
                self.speak_engine.speak_list(specific)

    def gesture_detector(self):
        self.speak_engine.speak("Gesture mode: Activated")
        while True: 
            result = self.gesture_engine.recognize_gesture()
            if result == 'stop':
                time.sleep(0.5)
                self.read()
            elif result == 'call me':
                time.sleep(0.5)
                self.helpme()
            elif result =="fist":
                break
        
            


if __name__ == "__main__":
    app = Main()
    speak = s.Speak()
    while True: 
        try: 
            speak.speak("System awaken, Select the mode!")
            key = keyboard.read_key()
            if key == "a":  
                app.startAssistant()
            elif key == "g":
                app.gesture_detector()  
        except:
            break 