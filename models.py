## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        self.conv_1 = nn.Conv2d(1, 32, 5)
        self.conv_2 = nn.Conv2d(32, 64, 3)
        self.conv_3 = nn.Conv2d(64, 128, 3)
        self.conv_4 = nn.Conv2d(128, 256, 3)
        self.conv_5 = nn.Conv2d(256, 512, 1)

        self.conv1_bn = nn.BatchNorm2d(32)
        self.conv2_bn = nn.BatchNorm2d(64)
        self.conv3_bn = nn.BatchNorm2d(128)
        self.conv4_bn = nn.BatchNorm2d(256)
        self.conv5_bn = nn.BatchNorm2d(512)

        self.pool = nn.MaxPool2d(2,2)
        
        self.dropout = nn.Dropout(0.2)
        
        self.dense_1 = nn.Linear(512*6*6, 1000)
        self.dense_2 = nn.Linear(1000, 1000)
        self.dense_3 = nn.Linear(1000, 136)
        
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        
        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:

        
        x = self.dropout(self.pool(F.selu(self.conv1_bn(self.conv_1(x)))))
        x = self.dropout(self.pool(F.selu(self.conv2_bn(self.conv_2(x)))))
        x = self.dropout(self.pool(F.selu(self.conv3_bn(self.conv_3(x)))))
        x = self.dropout(self.pool(F.selu(self.conv4_bn(self.conv_4(x)))))
        x = self.dropout(self.pool(F.selu(self.conv5_bn(self.conv_5(x)))))
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.dense_1(x)))
        x = self.dropout(F.relu(self.dense_2(x)))
        x = self.dense_3(x)
        
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x
