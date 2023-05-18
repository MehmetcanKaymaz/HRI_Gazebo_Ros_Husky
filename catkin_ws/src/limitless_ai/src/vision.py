#!/usr/bin/env python3

import os
import rospy
import cv2
import torch
import statistics
import numpy as np
from PIL import Image
from torchvision import transforms
from std_msgs.msg import Int32
# from sensor_msgs.msg import Image

class Vision_Model():
    """
    BU SINIF YZ MODELINI CALISTIRACAK VE KULLANICININ KAFA POZISYONUNA GORE BIR SINIF TAHMINI YAPACAKTIR
    """

    def __init__(self):
        self.queue = []
        self.cap = cv2.VideoCapture(0)

    def load_model(self):
        """
        MODELI YUKLEYELIM
        :return:
        """
        # Load the pre-trained ResNet-18 model
        self.model = torch.load('models/model_noise_5.pth', map_location=torch.device('cpu'))
        self.model.to('cpu')
        # print("Model: ", self.model)
        # Set the model to evaluation mode
        self.model.eval()
        # Define the data transformations to be applied to the images
        self.data_transforms = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        # print("Data Transform: ", self.data_transforms)

    def predict_label(self):
        """
        MODELDEN TAHMIN SONUCLARI ALALIM
        :return:
        """
        # Open a connection to the default webcam
        # Loop over the frames from the webcam
        # Capture a frame from the webcam
        ret, frame = self.cap.read()
        # Apply the data transformations to the frame
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the NumPy array to a PIL Image
        img = Image.fromarray(np.uint8(img))
        # Apply the data transformations to the image
        img = self.data_transforms(img).unsqueeze(0)
        # Make a prediction with the model
        with torch.no_grad():
            output = self.model(img)
        # Get the predicted class label
        _, predicted = torch.max(output.data, 1)
        self.tahmin_label = predicted.item()
        #print("Tahmin Class: ", self.tahmin_label)
        # Display the predicted class label on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        cv2.putText(frame, 'Predicted Class: ' + str(self.tahmin_label), org, font,
                    fontScale, color, thickness, cv2.LINE_AA)
        
        # Display the frame
        cv2.imshow('frame', frame)
        
        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
        
        self.queue.append(self.tahmin_label)
        if len(self.queue) > 10:
            self.queue.pop(0)

        return self.queue

def start_vision_system():
    # ROS Ayarlari
    rospy.init_node('vision_system', anonymous=True)
    pub1 = rospy.Publisher('tahminler', Int32, queue_size=10)
    rate = rospy.Rate(1) # 1 Hertz
    model = Vision_Model()
    model.load_model()
    while not rospy.is_shutdown():
        son_tahminler = model.predict_label()
        if len(son_tahminler) > 0:
            tahmin = statistics.mode(son_tahminler)
            pub1.publish(tahmin)
            print("Tahmin:", tahmin)
        rate.sleep()

if __name__ == '__main__':
    start_vision_system()
