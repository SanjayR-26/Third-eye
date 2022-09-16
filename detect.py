import cv2
import time
from face import Face

class objectDetection():
    classNames= [] #to store the class names
    #now we load the weight and cfg file and make some configurations for our detection
    configPath = "dependancies/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    weightsPath = "dependancies/frozen_inference_graph.pb"
    net = cv2.dnn_DetectionModel(weightsPath,configPath)#USING OPENCV'S OWN FUNCTION  
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    print("Loaded: Object detection engine")
    
    #TO INITIALIZE FIRST WE NEED TO TAKE ALL THE CLASS NAMES FROM THE COCO.NAMES
    def __init__(self):      
      classFile = "dependancies/coco.names"
      self.face = Face()
      with open(classFile,'rt') as f:
        self.classNames = f.read().rstrip('\n').split('\n')

    #function to detect using mobilenet neural network[without any custom training]
    def detect_objects(self, threshold =0.5):
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  
        time.sleep(0.5)
        if cap.isOpened():
            success, img = cap.read()
        class_index, confis, bbox = self.net.detect(img,confThreshold=threshold)
        if len(class_index) !=0:
            # print(class_index)
            names = [self.classNames[x-1] for x in class_index.flatten()]
            if 'person' in names:
                temp_names = self.face.recognize_face(img)
                if temp_names == 'Cannot recognize person' or temp_names == "No faces Detected":
                    return names
                else:
                    names.remove('person')
                    return names + temp_names
            else:
                return names
        cap.release()
        return "No objects detected"

if __name__ == "__main__":
    objectDetection()


# def testMobilenet():
#     detnet = objectDetection()
#     result = detnet.detect_mobilenet()
#     return result

# print(testMobilenet())