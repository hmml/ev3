import os
import array
from mmap import mmap, MAP_SHARED, PROT_READ, PROT_WRITE
from . import lms2012
import Image
import ImageDraw
_initialized = False
MEM_WIDTH = 60  # bytes
SCREEN_WIDTH = 178  # pix
SCREEN_HEIGHT = 128
HW_MEM_WIDTH = ((SCREEN_WIDTH + 31)/32)*4
_lcdfile = None
lcdmm=None
image = Image.new('1',(HW_MEM_WIDTH*8,SCREEN_HEIGHT),1)
draw=ImageDraw.Draw(image)
def open_device():
    global _initialized
    if not _initialized:
        global _lcdfile
        _lcdfile = os.open(lms2012.LCD_DEVICE_NAME, os.O_RDWR)
        global lcdmm
        lcdmm = mmap(fileno=_lcdfile, length=MEM_WIDTH * SCREEN_HEIGHT,
                     flags=MAP_SHARED, prot=PROT_READ | PROT_WRITE, offset=0)
    _initialized = True

def black():
    draw.rectangle([0,0,SCREEN_WIDTH-1,SCREEN_HEIGHT-1],fill=0)
    redraw()

def white():
    draw.rectangle([0,0,SCREEN_WIDTH-1,SCREEN_HEIGHT-1],fill=1)
    redraw()

def redraw():
    reversbuffer=array.array('B',[int('{:08b}'.format(~ord(c)&0xff)[::-1], 2) for c in image.tostring()])
    lcdmm.seek(0)
    lcdmm.write(reversbuffer)
    lcdmm.flush()


def close_device():
    global _initialized
    if _initialized:
        lcdmm.close()
        os.close(_lcdfile)
        _initialized = False
