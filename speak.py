from gtts import gTTS
import os
from playsound import playsound

class Speak():
    def __init__(self):
        print("Loaded: Speak engine")

    def speak(self, message, language='en'):
        tts = gTTS(message, lang=language)
        tts.save('temp/speech.mp3')
        playsound('temp/speech.mp3')
        os.remove('temp/speech.mp3')

    def speak_list(self, list):
        string = ",".join(list)
        tts = gTTS(string, lang='en')
        tts.save('temp/speech.mp3')
        playsound('temp/speech.mp3')
        os.remove('temp/speech.mp3')


if __name__ == "__main__":
    Speak()
# speak = Speak()
# speak.speak("ஒளியாக நீயிருப்பதால் இருளைபற்றிய கவலை எனக்கில்லை...", 'ta')