Training data shall be in the form of 5 second audio clips presented to the CNN as spectrograms

Current Data:

-SSB Voice
-CW
-FT8

(will add more as it becomes feisable to farm)

audiotospec.py:
=================================
-This script converts .wav files of arbirtary length into .png files of spectrograms
-Each spectrogram is of a 3 second interval of the recording
-Image dimensions are 492x365 (this is a function of matplotlib's graph handling) and grayscale
-The first command line argument is the source file and the second is the destination folder
-The script automatically names output files as a function of the folder contents so don't mess
with the naming convention or this could break
