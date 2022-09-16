import cv2
from datetime import datetime
import time
import os
import pytesseract
import shutil
from paddleocr import PaddleOCR
from langdetect import detect_langs
pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class Read():
    def __init__(self):
        self.ocr = PaddleOCR(lang="en" , show_log=False)
        print("Loaded: Read engine")

    def detectlang(self,txt):
        lang = str(detect_langs(txt)[0])
        result = lang.split(":")
        return result[0]
    def Sort_Tuple(self, tup):
        tup.sort(key = lambda x: x[1], reverse = True)
        return tup
    def find_specific(self, img_path):
        result = self.ocr.ocr(img_path, cls=True)
        result = [res[1] for res in result]
        result = self.Sort_Tuple(result)
        specifics = [result[x][0] for x in range(0, len(result)) if x < 8]
        os.remove(img_path)
        return specifics
    def push(self, frame):
        now = datetime.now()
        dtString = now.strftime('%H.%M.%S')
        path = f'temp/temp{dtString}.jpg'
        cv2.imwrite(path, frame)
        return path

        
    def recognize_text(self):
        print("Read Mode Activated")
        camera = cv2.VideoCapture(0)
        if (camera.isOpened()):
            return_value,img = camera.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            custom_config = r'-l eng+tam+hin --psm 6'
            txt = pytesseract.image_to_string(img, config= custom_config)
            current_lang = self.detectlang(txt)
            x = txt.replace("\u200c", "")
            camera.release()
        return x.replace("\n",""), current_lang

        
    def recognize_phonenumbers(self):
        camera = cv2.VideoCapture(0)
        if (camera.isOpened()):
            return_value,img = camera.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cong = r'--oem 3 --psm 6 outputbase digits'
            txt = pytesseract.image_to_string(img, config=cong)
            camera.release()
        return [x for x in txt.split() if len(x)>7]

    def recognize_specific(self):
        camera = cv2.VideoCapture(1)
        if (camera.isOpened()):
            return_value,image = camera.read()
            path = self.push(image)
            camera.release()
        return self.find_specific(path)


if __name__ == "__main__":
    Read()

# img = cv2.imread("images/read1.png")
# read = Read()
# result = read.recognize_phonenumbers(img)
# print(result)