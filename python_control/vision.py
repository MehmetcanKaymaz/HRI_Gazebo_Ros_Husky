#!/usr/bin/env python

import cv2
import torch
import torchvision
from torchvision import models, transforms
import numpy as np
from PIL import Image

class Vision:
    def __init__(self):

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

        """# Display the predicted class label on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        cv2.putText(frame, 'Predicted Class: ' + str(label), org, font,
                    fontScale, color, thickness, cv2.LINE_AA)

        # Display the frame
        cv2.imshow('frame', frame)"""

        return label


        
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





#sc=SimpleControl()
#sc.run_main()


