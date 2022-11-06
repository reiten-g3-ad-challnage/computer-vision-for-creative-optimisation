<<<<<<< HEAD
from pathlib import Path

from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt

class ObjectDetector:
    def init(self,mode,net=None) -> None:
        self.mode = mode
        self.net = net
    def load_yolo(self):
        self.net = model_zoo.get_model('yolo3_darknet53_voc', pretrained=True)
        return self.net
     
    def detect_from_image(self,image_path,net):
        x, img = data.transforms.presets.yolo.load_test(image_path, short=512)
        print('Shape of pre-processed image:', x.shape)
        class_IDs, scores, bounding_boxs = net(x)
        
        return class_IDs, scores, bounding_boxs,img
        
    def plot_detection(self,img,class_IDs, scores, bounding_boxs):
       ax = utils.viz.plot_bbox(img, bounding_boxs[0], scores[0],
                                class_IDs[0], class_names=self.net.classes)
       plt.show()
=======
#object detection using SSD and opencv

#importing required libraries
from imutils.video import FPS
import numpy as np
import imutils
import cv2

#Defining some constants and
use_gpu = True
live_video = False
confidence_level = 0.5
fps = FPS().start()
ret = True
#Initialize Objects and corresponding colors which the model can detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

#Defining colors array where each class is randomly assigned a color.
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

#Reading the network in a variable called net using cv2.dnn.readNetFromCaffe.
net = cv2.dnn.readNetFromCaffe('models/caffe/MobileNetSSD_deploy.prototxt', 
                               'ssd_files/MobileNetSSD_deploy.caffemodel')

#If the parameter use_gpu is set to TRUE, set the backend and target to Cuda.
if use_gpu:
    print("[INFO] setting preferable backend and target to CUDA...")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

#Initialize the VideoCapture object either with 0 for live video or with the video file name.
print("[INFO] accessing video stream...")
if live_video:
    vs = cv2.VideoCapture(0)
else:
    vs = cv2.VideoCapture('sample.mp4')

#Let’s get in the infinite array and read the frames
while ret:
    ret, frame = vs.read()
    if ret:  #if the VideoCapture object is returning True, then only proceed.
        frame = imutils.resize(frame, width=400) #Resize the frame and get its height and width.
        (h, w) = frame.shape[:2]
        
        #Create a blob from the image, set it as input, and pass it forward through the network using cv2.blobFromImage.
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        #Let’s traverse in the detections we got.
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2] #check the confidence of each and every detection
            if confidence > confidence_level: 
                idx = int(detections[0, 0, i, 1])
                
                #Calculate the coordinates of the box and convert them to int
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2) #Drawing the rectangle around the found object

                #putting this label onto the original frame 
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_DUPLEX, 0.5, COLORS[idx], 1)
        
        frame = imutils.resize(frame,height=400)
        cv2.imshow('Live detection',frame) # show final result

        # Break if someone hits the ESC key 
        if cv2.waitKey(1)==27:
            break

        fps.update()

fps.stop()

#Printing FPS metrics
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
>>>>>>> e09727509ad03c2c227608932a7f553ac3ea0ba3
