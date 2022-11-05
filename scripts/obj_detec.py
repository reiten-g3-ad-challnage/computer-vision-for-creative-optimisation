#requirements:
#pip install tensorflow==2.4.0
#pip install keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0
#pip install imageai --upgrade
#====================================================
#import package
from imageai.Detection import ObjectDetection

detector = ObjectDetection()

#define paths
model_path = "./models/yolo-tiny.h5"
input_path = "./images/image.jpg"
output_path = "./images/newimage.jpg"

#call the methods
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()
detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)

for eachItem in detection:
    print(eachItem["name"] , " : ", eachItem["percentage_probability"])