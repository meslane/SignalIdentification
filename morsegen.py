import os
import sys
import random

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

def morseToWav(wpm, freq, noise, message):
    sampleRate = 8000 #.wav stuff
    amp_high = 0.5
    amp_low = 0.0001
    bandw = 20 #filter params
    degree = 2
    #noise = 100 #noise param

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
                    dur = BEAT * DIT
                elif sym == '-':
                    dur = BEAT * DAH
                
                sections.append(createWave(dur, freq, amp_high, sampleRate))
                sections.append(createWave(BEAT * DIT, freq, amp_low, sampleRate)) #do space
            sections.append(createWave(BEAT * (DAH - DIT), freq, amp_low, sampleRate)) #do inter-char
        sections.append(createWave(BEAT * (BREAK - DAH - DIT), freq, amp_low, sampleRate)) #do inter-word

    #post-processing
    wave = []

    for sect in sections: #concatenate all sections
        wave = np.concatenate([wave, sect.astype(np.int16)])

    b, a = signal.butter(degree, Wn = [(freq - bandw) / (0.5 * sampleRate), (freq + bandw) / (0.5 * sampleRate)], btype = 'band')
    wave = signal.lfilter(b, a, wave).astype(np.int16) #filter
    wave = wave + np.random.normal(0, noise, wave.shape).astype(np.int16) #apply noise

    #write to file
    wavfile.write("sin.wav", sampleRate, wave)
    
morseToWav(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), str(sys.argv[4]))