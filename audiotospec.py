from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import sys
import cv2 as cv

samplerate, wave = wavfile.read(sys.argv[1])

try:
    flist = [int(i.split('_')[0]) for i in os.listdir(sys.argv[2])]
    flist.sort()
    nameIndex = flist[-1] + 1
except IndexError:
    nameIndex = 0
#print(nameIndex)

for i in range(0, len(wave) // int(samplerate*3)): #split into 3 sec samples
    section = wave[i * int(samplerate*3): (i + 1) * int(samplerate*3)]

    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(section, Fs=samplerate)
    plt.savefig('temp.png') #cache temp for openCV (this is super hacky but it's the easiest way)

    temp = cv.imread('temp.png')
    temp = temp [60:425, 82:574] #crop to remove graph stuff
    temp = cv.cvtColor(temp, cv.COLOR_BGR2GRAY)
    
    filename = '{}/{}_{}.png'.format(sys.argv[2], nameIndex, i)
    cv.imwrite(filename, temp, [cv.IMWRITE_PNG_COMPRESSION, 0])
    print("Wrote file {}".format(filename))
    
    os.remove('temp.png') #wash our hands of our sins