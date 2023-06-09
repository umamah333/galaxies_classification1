# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MGgRJHPZKtjUI3u7faXkNXxor0E-nZGT
"""

from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import precision_score

from PIL import Image
from multiprocessing import Pool
import warnings
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Set up the data generators to feed the model
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
validation_datagen = ImageDataGenerator(rescale=1./255)

from sklearn.utils import shuffle
## Set up the data generators to feed the model
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(img_width, img_height), 
                                                    batch_size=batch_size,
                                                    color_mode='grayscale',
                                                    class_mode='categorical', shuffle=True)

validation_generator = validation_datagen.flow_from_directory(validation_dir,
                                                              target_size=(img_width, img_height), 
                                                              batch_size=batch_size, 
                                                              color_mode='grayscale',
                                                              class_mode='categorical',  shuffle=True)

from tensorflow.keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, concatenate, AveragePooling2D
from tensorflow.keras.models import Model

input_shape = (img_width, img_height, 1) # specify the input shape for grayscale images

# Stem layers
input_layer = Input(shape=input_shape)
x = Conv2D(32, (3, 3), strides=(2, 2), padding='valid', activation='relu')(input_layer)
x = Conv2D(32, (3, 3), padding='valid', activation='relu')(x)
x = Conv2D(64, (3, 3), padding='same', activation='relu')(x)
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(x)
x = Conv2D(80, (1, 1), padding='valid', activation='relu')(x)
x = Conv2D(192, (3, 3), padding='valid', activation='relu')(x)
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(x)

# Inception blocks
inception_3a = concatenate([Conv2D(64, (1, 1), padding='same', activation='relu')(x),
                            Conv2D(96, (3, 3), padding='same', activation='relu')(x)])
inception_3b = concatenate([Conv2D(64, (1, 1), padding='same', activation='relu')(inception_3a),
                            Conv2D(96, (3, 3), padding='same', activation='relu')(inception_3a)])
inception_3c = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(inception_3b)

inception_4a = concatenate([Conv2D(128, (1, 1), padding='same', activation='relu')(inception_3c),
                            Conv2D(128, (3, 3), padding='same', activation='relu')(inception_3c)])
inception_4b = concatenate([Conv2D(128, (1, 1), padding='same', activation='relu')(inception_4a),
                            Conv2D(128, (3, 3), padding='same', activation='relu')(inception_4a)])
inception_4c = concatenate([Conv2D(128, (1, 1), padding='same', activation='relu')(inception_4b),
                            Conv2D(128, (3, 3), padding='same', activation='relu')(inception_4b)])
inception_4d = concatenate([Conv2D(128, (1, 1), padding='same', activation='relu')(inception_4c),
                            Conv2D(128, (3, 3), padding='same', activation='relu')(inception_4c)])
inception_4e = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(inception_4d)

inception_5a = concatenate([Conv2D(256, (1, 1), padding='same', activation='relu')(inception_4e),
                            Conv2D(256, (3, 3), padding='same', activation='relu')(inception_4e)])
inception_5b = concatenate([Conv2D(256, (1, 1), padding='same', activation='relu')(inception_5a),
Conv2D(256, (3, 3), padding='same', activation='relu')(inception_5a)])
inception_5c = AveragePooling2D(pool_size=(5, 5), strides=(1, 1))(inception_5b)
flatten_layer = Flatten()(inception_5c)
dropout_layer = Dropout(0.4)(flatten_layer)
output_layer = Dense(num_classes, activation='softmax')(dropout_layer)

