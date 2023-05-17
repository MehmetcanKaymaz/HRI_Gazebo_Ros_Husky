#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys, select, termios, tty
import time
import threading
import cv2
import torch
import torchvision
from torchvision import models, transforms
import numpy as np
from PIL import Image

settings = termios.tcgetattr(sys.stdin)

class SimpleControl:
    def __init__(self):
        self.velx=0
        self.vely=0
        self.velz=0
        self.rotz=0
        self.rotx=0
        self.roty=0

        self.run_rose=True

        # Load the pre-trained ResNet-18 model
        self.model = torch.load('models/model_noise_5.pth')

        self.model.to('cpu')

        # Set the model to evaluation mode
        self.model.eval()

        # Define the data transformations to be applied to the images
        self.data_transforms = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # Open a connection to the default webcam
        self.cap = cv2.VideoCapture(0)        

        rospy.init_node('husky_teleop')
        self.pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)

        self.t=threading.Thread(target=self.run_ros_node)

        self.t.start()

    def single_update(self):
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
        label = predicted.item()

        self.apply_control(label=label)

        # Display the predicted class label on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        cv2.putText(frame, 'Predicted Class: ' + str(label), org, font,
                    fontScale, color, thickness, cv2.LINE_AA)

        # Display the frame
        cv2.imshow('frame', frame)


        
    def run_main(self):
        statu=True
        while statu:
            self.single_update()

            # Exit if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close the window
        self.cap.release()
        cv2.destroyAllWindows()

        self.run_rose=False
        self.t.join()

    def apply_control(self,label):
        if label==0:
            self.rotz=0
        elif label==1:
            self.velx+=0.5
            self.velx=min(self.velx,1.)
        elif label==2:
            self.velx+=-0.5
            self.velx=max(self.velx,-1.)  
        elif label==3:
            self.rotz=-.5
        elif label==4:
            self.rotz=.5
        else:
            print("Unknown label ",label)


    def run_ros_node(self):
        while self.run_rose:
            self.sent_ros_node()
    
    def sent_ros_node(self):
        twist=Twist()
        twist.linear.x = self.velx
        twist.linear.y = self.vely
        twist.linear.z = self.velz
        twist.angular.x = self.rotx
        twist.angular.y = self.roty
        twist.angular.z = self.rotz

        self.pub.publish(twist)


#sc=SimpleControl()
#sc.run_main()


