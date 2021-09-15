import os
import sys
import random
import re
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy import signal

def table(x):
    return {
        'a': '.-',
        'b': '-...',
        'c': '-.-.',
        'd': '-..',
        'e': '.',
        'f': '..-.',
        'g': '--.',
        'h': '....',
        'i': '..',
        'j': '.---',
        'k': '-.-',
        'l': '.-..',
        'm': '--',
        'n': '-.',
        'o': '---',
        'p': '.--.',
        'q': '--.-',
        'r': '.-.',
        's': '...',
        't': '-',
        'u': '..-',
        'v': '...-',
        'w': '.--',
        'x': '-..-',
        'y': '-.--',
        'z': '--..',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        '@': '.--.-.',
        ',': '--..--',
        '.': '.-.-.-',
        '?': '..--..',
        '"': '.-..-.',
        "'": '.----.',
        '/': '-..-.',
        ':': '---...',
        ' ': '/' 
    }.get(x, ' ')

def convert(input):
    output = ''
    for char in input.lower():
        output = output + table(char) + ' '
        
    #output = output + '.-.-.'
    return output
    
def createWave(dur, freq, ampl, sampleRate):
    t = np.linspace(0, dur, int(sampleRate * dur), endpoint=False)
    return ampl * np.iinfo(np.int16).max * np.sin(freq * 2 * np.pi * t)
    
def getJitter(jitter, dur):
    return dur + random.uniform(-1 * jitter * dur, jitter * dur)

def morseToWav(wpm, freq, noise, amp, bandwidth, sampleRate, jitter, filename, message):
    #sampleRate = 8000 #.wav stuff
    amp_high = amp #0.5
    amp_low = 0.0001
    bandw = bandwidth #20 #filter params
    degree = 2

    DIT = 1
    DAH = 3
    SPACE = 3
    BREAK = 7
    BEAT = float(60/(50 * wpm)) #arg 1 = wpm

    sections = []
    for word in message.split():
        for char in word:
            for sym in table(char.lower()):
                dur = 0
                
                if sym == '.':
                    dur = getJitter(jitter, BEAT * DIT)
                elif sym == '-':
                    dur = getJitter(jitter, BEAT * DAH)
                
                sections.append(createWave(dur, freq, amp_high, sampleRate))
                sections.append(createWave(getJitter(jitter, BEAT * DIT), freq, amp_low, sampleRate)) #do space
            sections.append(createWave(getJitter(jitter, BEAT * (SPACE - DIT)), freq, amp_low, sampleRate)) #do inter-char
        sections.append(createWave(getJitter(jitter, BEAT * (BREAK - SPACE - DIT)), freq, amp_low, sampleRate)) #do inter-word

    #post-processing
    wave = []

    for sect in sections: #concatenate all sections
        wave = np.concatenate([wave, sect.astype(np.int16)])

    b, a = signal.butter(degree, Wn = [(freq - bandw) / (0.5 * sampleRate), (freq + bandw) / (0.5 * sampleRate)], btype = 'band')
    wave = signal.lfilter(b, a, wave).astype(np.int16) #filter
    wave = wave + np.random.normal(0, noise, wave.shape).astype(np.int16) #apply noise

    #write to file
    wavfile.write(filename, sampleRate, wave)


def main():
    f = open(sys.argv[1], "r")
    dest = sys.argv[2]
    
    data = f.read().replace('\n', ' ').replace('\t', '').lower()
    data = re.sub(' +', ' ', data)
    
    blocksize = 32
    
    for i in range(len(data) // blocksize):
        wpm = random.randint(7, 35)
        freq = random.randint(100, 4000)
        noise = random.randint(0, 4800)
        amp = random.uniform(0.1, 0.9)
        sampleRate = 8000
        bandw = random.randint(1, 20) * 10
        jitter = random.uniform(0, 0.3)
        
        text = data[i * blocksize:(i * blocksize) + blocksize].lstrip()
        
        print("{} {} {} {} {} {} {} {}".format(wpm, freq, noise, amp, bandw, sampleRate, jitter, text))
        
        morseToWav(wpm, freq, noise, amp, bandw, sampleRate, jitter, "temp.wav", text)
        
        try:
            flist = [int(i.split('_')[0]) for i in os.listdir(dest)]
            flist.sort()
            nameIndex = flist[-1] + 1
        except IndexError:
            nameIndex = 0
            
        subprocess.call(['python', 'audiotospec.py', 'temp.wav', '{}'.format(dest)], shell = True) #run conversion script
        os.remove("temp.wav") #delete temporary .wav
    
if __name__ == "__main__":
    main()

#morseToWav(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), str(sys.argv[7]))