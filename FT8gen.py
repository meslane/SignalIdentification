import os
import sys
import random
import re
import subprocess

#This scrpit generates FT8 training data using https://github.com/kgoba/ft8_lib

f = open(sys.argv[1], "r")
dest = sys.argv[2]

data = f.read().replace('\n', ' ').replace('\t', '').upper()
data = re.sub(' +', ' ', data)

for i in range(len(data) // 13): #FT8 transmissions are at max 13 chars
    freq = random.randint(100, 4900)
    text = data[i * 13:(i * 13) + 13].lstrip()
    subprocess.call(['.\gen_ft8.exe', '"{}"'.format(text), 'temp.wav', '{}'.format(freq)], shell = True) #generate .wav
    print("{} f = {}".format(text,freq))
    
    try:
        flist = [int(i.split('_')[0]) for i in os.listdir(dest)]
        flist.sort()
        nameIndex = flist[-1] + 1
    except IndexError:
        nameIndex = 0
        
    subprocess.call(['python', 'audiotospec.py', 'temp.wav', '{}'.format(dest)], shell = True) #run conversion script
    os.remove("{}/{}_0.png".format(dest, nameIndex)) #delete file with whitespace in it
    os.remove("temp.wav") #delete temporary .wav