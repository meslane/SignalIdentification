import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import sounddevice as sd
import cv2 as cv
import os
import sys

print("TensorFlow version: {}".format(tf.__version__))

RATE = 8000
DURATION = 3
MODEL_NAME = "model2" 

model = tf.keras.models.load_model(MODEL_NAME)

def predictLocalImage(model, image, categories):
    iarray = tf.keras.preprocessing.image.img_to_array(image)
    iarray = tf.expand_dims(iarray, 0)

    predict = model.predict(iarray)
    score = tf.nn.softmax(predict[0])
    
    return (categories[np.argmax(score)], 100 * np.max(score))

while True:
    data = sd.rec(int(RATE * DURATION), samplerate = RATE, channels = 1, dtype = 'int16')
    sd.wait()

    data = np.concatenate(data) #make into 1d since sounddevice has a weird format

    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(data, Fs = RATE)
    plt.savefig('temp.png')
    
    temp = cv.imread('temp.png')
    temp = temp [60:425, 82:574] #crop to remove graph stuff
    temp = cv.cvtColor(temp, cv.COLOR_BGR2GRAY)
    
    result = predictLocalImage(model, temp, ["CW", "FT8", "Voice"])
    
    print("Signal is {} with {}% confidence".format(result[0], result[1]))
    
    os.remove('temp.png')
    cv.imshow('spectrogram', temp)
    
    if cv.waitKey(1) == ord('q'):
        sys.exit()