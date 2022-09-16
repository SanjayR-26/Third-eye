import speech_recognition as sr
import speak as sp

class Listen():
    def __init__(self):
        self.r=sr.Recognizer()
        self.m=sr.Microphone()
        self.speak = sp.Speak()
        print("Loaded: listening engine")

    def listen(self):
        try:
            with self.m as source:
                self.r.adjust_for_ambient_noise(source)
                self.speak.speak("Listening")
                audio = self.r.listen(source, phrase_time_limit=5)
                said = self.r.recognize_google(audio)
                self.speak.speak("Recognized")
                return said.lower()
        except Exception as e:
            print("Exception: " + "Not able to recognize anything")
            return "None"

if __name__ == "__main__":
     Listen()




    # listen = Listen()
    # while True:
    #     result = listen.listen()
    #     if result == "None":
    #         continue
    #     else:
    #         print(result)
