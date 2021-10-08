#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
===============================================================================
Interactive Image Segmentation using GrabCut algorithm.
This sample shows interactive image segmentation using grabcut algorithm.
USAGE:
    python grabcut.py <filename>
README FIRST:
    Two windows will show up, one for input and one for output.
    At first, in input window, draw a rectangle around the object using the
right mouse button. Then press 'n' to segment the object (once or a few times)
For any finer touch-ups, you can press any of the keys below and draw lines on
the areas you want. Then again press 'n' to update the output.
Key '0' - To select areas of sure background
Key '1' - To select areas of sure foreground
Key '2' - To select areas of probable background
Key '3' - To select areas of probable foreground
Key 'n' - To update the segmentation
Key 'r' - To reset the setup
Key 's' - To save the results
===============================================================================
'''

# Python 2/3 compatibility
from __future__ import print_function
# All imports
import numpy as np
import cv2 as cv
import os
from PIL import Image
import sys

# Main class
class App():
    BLUE = [255,0,0]        # rectangle color
    RED = [0,0,255]         # PR BG
    GREEN = [0,255,0]       # PR FG
    BLACK = [0,0,0]         # sure BG
    WHITE = [255,255,255]   # sure FG

    DRAW_BG = {'color' : BLACK, 'val' : 0}
    DRAW_FG = {'color' : WHITE, 'val' : 1}
    DRAW_PR_BG = {'color' : RED, 'val' : 2}
    DRAW_PR_FG = {'color' : GREEN, 'val' : 3}

    # setting up flags
    rect = (0,0,1,1)
    drawing = False         # flag for drawing curves
    rectangle = False       # flag for drawing rect
    rect_over = False       # flag to check if rect drawn
    rect_or_mask = 100      # flag for selecting rect or mask mode
    value = DRAW_FG         # drawing initialized to FG
    thickness = 3           # brush thickness

    def onmouse(self, event, x, y, flags, param):
        # Draw Rectangle
        if event == cv.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x,y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.rectangle == True:
                self.img = self.img2.copy()
                cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
                self.rect_or_mask = 0

        elif event == cv.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
            self.rect_or_mask = 0
            print(" Now press the key 'n' a few times until no further change \n")

        # draw touchup curves
        if event == cv.EVENT_LBUTTONDOWN:
            if self.rect_over == False:
                print("first draw rectangle \n")
            else:
                self.drawing = True
                cv.circle(self.img, (x,y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x,y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)
    # Scale function for images with big resolution
    def scale_image(self,
                    input_image_path,
                    width=None,
                    height=None
                    ):
        original_image = Image.open(input_image_path)
        w, h = original_image.size
        if (((w > 800) or (h > 800)) and ((h > 800) or (w > 800))):
            if width and height:
                max_size = (width, height)
            elif width:
                max_size = (width, h)
            elif height:
                max_size = (w, height)
            else:
                # No width or height specified
                raise RuntimeError('Width or height required!')

            original_image.thumbnail(max_size, Image.ANTIALIAS)
            original_image.save('Saves/scaled.jpg')

            scaled_image = Image.open('Saves/scaled.jpg')
            width, height = scaled_image.size
            # Create txt
            my_file = open("AsistFiles\ScaleOrNot.txt", "w+")
            my_file.write("1")
            my_file.close()
            print('The scaled image size is {wide} wide x {height} '
                  'high'.format(wide=width, height=height))
        else:
            print('The original image size is {wide} wide x {height} '
                  'high'.format(wide=w, height=h))
            # Create txt
            my_file = open("AsistFiles\ScaleOrNot.txt", "w+")
            my_file.write("0")
            my_file.close()

    def run(self):
        # Loading images
        if len(sys.argv) == 2:
            filename = sys.argv[1] # for drawing purposes
        else:
            print("No input image given \n")
            print("Correct Usage: python grabcut.py <filename> \n")
            f = open('AsistFiles/FileWay.txt', 'r')
            filename = f.read()
            print(filename)
            f.close()
            self.scale_image(input_image_path = filename, width = 800, height=800)
            f = open('AsistFiles/ScaleOrNot.txt', 'r')
            scalefile = f.read()
            print(scalefile)
            zero = "0"
            # Filename and directory without scale
            if (scalefile == zero):
                l = list(filename)
                size = len(l) - 5
                sizeoffilename = size
                filenamecopy = ''
                slash = "/"
                while (size > 0):
                    checkstring = l[size]
                    if (checkstring == slash):
                        break
                    filenamecopy = filenamecopy + l[size]
                    size -= 1
                print(filenamecopy)
                l = list(filenamecopy)
                size = len(l) - 1
                sizeofname = size
                print(len(l))
                filenamecopy2 = ''
                while (size >= 0):
                    filenamecopy2 = filenamecopy2 + l[size]
                    size -= 1
                print(filenamecopy2)

                sizeofdirectory = sizeoffilename - sizeofname - 1
                nameofdirectory = ''
                l = list(filename)
                i = 0
                while (i <= sizeofdirectory):
                    nameofdirectory = nameofdirectory + l[i]
                    i += 1
                testpath = nameofdirectory + "grubcut"

                if os.path.exists(testpath):
                    if os.path.isdir(testpath):
                        print('КАТАЛОГ')
                else:
                    sizeofdirectory = sizeoffilename - sizeofname - 1
                    nameofdirectory = ''
                    l = list(filename)
                    i = 0
                    while (i <= sizeofdirectory):
                        nameofdirectory = nameofdirectory + l[i]
                        i += 1
                    print(nameofdirectory)
                    os.mkdir(nameofdirectory + "grubcut")
            # Filename and directory with scale
            else:
                l = list(filename)
                size = len(l) - 5
                sizeoffilename = size
                filenamecopy = ''
                slash = "/"
                while (size > 0):
                    checkstring = l[size]
                    if (checkstring == slash):
                        break
                    filenamecopy = filenamecopy + l[size]
                    size -= 1
                print(filenamecopy)
                l = list(filenamecopy)
                size = len(l) - 1
                sizeofname = size
                print(len(l))
                filenamecopy2 = ''
                while (size >= 0):
                    filenamecopy2 = filenamecopy2 + l[size]
                    size -= 1
                print(filenamecopy2)

                sizeofdirectory = sizeoffilename - sizeofname - 1
                nameofdirectory = ''
                l = list(filename)
                i = 0
                while (i <= sizeofdirectory):
                    nameofdirectory = nameofdirectory + l[i]
                    i += 1
                testpath = nameofdirectory + "grubcut"

                if os.path.exists(testpath):
                    if os.path.isdir(testpath):
                        print('КАТАЛОГ')
                else:
                    sizeofdirectory = sizeoffilename - sizeofname - 1
                    nameofdirectory = ''
                    l = list(filename)
                    i = 0
                    while (i <= sizeofdirectory):
                        nameofdirectory = nameofdirectory + l[i]
                        i += 1
                    print(nameofdirectory)
                    os.mkdir(nameofdirectory + "grubcut")
                filename = 'Saves/scaled.jpg'


        self.img = cv.imread(cv.samples.findFile(filename))
        self.img2 = self.img.copy()                               # a copy of original image
        self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
        self.output = np.zeros(self.img.shape, np.uint8)           # output image to be shown

        # input and output windows
        cv.namedWindow('output')
        cv.namedWindow('input')
        cv.setMouseCallback('input', self.onmouse)
        cv.moveWindow('input', self.img.shape[1]+10,90)

        print(" Instructions: \n")
        print(" Draw a rectangle around the object using right mouse button \n")

        while(1):

            cv.imshow('output', self.output)
            cv.imshow('input', self.img)
            k = cv.waitKey(1)

            # key bindings
            if k == 27:         # esc to exit
                break
            elif k == ord('0'): # BG drawing
                print(" mark background regions with left mouse button \n")
                self.value = self.DRAW_BG
            elif k == ord('1'): # FG drawing
                print(" mark foreground regions with left mouse button \n")
                self.value = self.DRAW_FG
            elif k == ord('2'): # PR_BG drawing
                self.value = self.DRAW_PR_BG
            elif k == ord('3'): # PR_FG drawing
                self.value = self.DRAW_PR_FG
            elif k == ord('d'):  # Close all windows
                cv.DestroyAllWindows()
            elif k == ord('s'): # save image
                bar = np.zeros((self.img.shape[0], 5, 3), np.uint8)
                res = np.hstack((self.img2, bar, self.img, bar, self.output))
                cv.imwrite('Saves/' + filenamecopy2 + '_grabcut_stages.png', res)
                res2 = np.stack(self.output)
                cv.imwrite('Saves/' + filenamecopy2 + '_grabcut_output.png', res2)
                testpath = testpath + '/'
                os.replace('Saves/' + filenamecopy2 + '_grabcut_stages.png', testpath + filenamecopy2 + '_grabcut_stages.png')
                os.replace('Saves/' + filenamecopy2 + '_grabcut_output.png', testpath + filenamecopy2 + '_grabcut_output.png')
                print(" Result saved as image \n")
            elif k == ord('r'): # reset everything
                print("resetting \n")
                self.rect = (0,0,1,1)
                self.drawing = False
                self.rectangle = False
                self.rect_or_mask = 100
                self.rect_over = False
                self.value = self.DRAW_FG
                self.img = self.img2.copy()
                self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
                self.output = np.zeros(self.img.shape, np.uint8)           # output image to be shown
            elif k == ord('n'): # segment the image
                print(""" For finer touchups, mark foreground and background after pressing keys 0-3
                and again press 'n' \n""")
                try:
                    bgdmodel = np.zeros((1, 65), np.float64)
                    fgdmodel = np.zeros((1, 65), np.float64)
                    if (self.rect_or_mask == 0):         # grabcut with rect
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_RECT)
                        self.rect_or_mask = 1
                    elif (self.rect_or_mask == 1):       # grabcut with mask
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_MASK)
                except:
                    import traceback
                    traceback.print_exc()

            mask2 = np.where((self.mask == 1) + (self.mask == 3), 255, 0).astype('uint8')
            self.output = cv.bitwise_and(self.img2, self.img2, mask = mask2)

        print('Done')


if __name__ == '__main__':
    print(__doc__)
    App().run()
    cv.destroyAllWindows()