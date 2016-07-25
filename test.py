import ctypes
import sys
import os
from PIL import Image, ImageDraw, ImageFilter, ImageMath
from PIL import features
import gc
libc = ctypes.CDLL("libc.so.6")

from StringIO import StringIO
scaler = 'ANTIALIAS'
resample = {
    'ANTIALIAS': Image.ANTIALIAS,
    'BILINEAR': Image.BILINEAR,
    'BICUBIC': Image.BICUBIC
}

with open("Tests/images/hopper.ppm") as hop:
    hopper = StringIO(hop.read())
os.write(1, "PRE\n")
im = Image.open(hopper)
im.resize((8192, 8192), resample[scaler])
im = None
os.write(1, "GC: DO YOUR WORST\n")
gc.collect()
ret = libc.syscall(157, 22, 1, 0) #Turn on seccomp1
assert ret == 0
os.write(1, "PRE: DONE -- LOAD\n")
im = Image.open(hopper)
im.filter(ImageFilter.BLUR)
os.write(1, "RDY\n")
im.resize((8192, 8192), resample[scaler])
os.write(1, "HELLOTE\n")
im.resize((1024, 1024),)
libc.syscall(60) # die die die!
