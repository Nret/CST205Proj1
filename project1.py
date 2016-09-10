#! python3
# Coded by Peter Pommer for CST 205 on 9/7/2016
# Github https://github.com/Nret/CST205Proj1
# This program takes some collection of images and spits out the median filter of that image

"""
Plan of Attack:

load all the images into a list
get width and height of the first image
make new image with that width and height
for each x from 0 to width
    for each y from 0 to height
        clear a list for the tuple of all the pixels at this location
        for each image
            store the tuple of that pixel of that image into that list
        calculate median
        assign pixel at x,y in the new image with the result
write the new image to file

"""

from PIL import Image
from statistics import median
from tkinter import filedialog
import tkinter
import os
import time

def calculateMedianOfPixels(pixels):
    # Extract the separate colums from the list of tuples
    red   = [ pixel[0] for pixel in pixels ] # It is also possible to have these as
    green = [ pixel[1] for pixel in pixels ] # red = [ r for (r, g, b) in pixels ]
    blue  = [ pixel[2] for pixel in pixels ]
    # Return a tuple of the medians from the lists of colors
    # It is possible for median to return a float, which will cause a TypeError when trying to assign this tuple.
    return (int(median(red)), int(median(green)), int(median(blue))) # Could use median_low or median_high

def calculateMedianImage(files):
    # Open all the images into a list
    sourceImages = [ Image.open(file) for file in files ]

    # Get the width and height
    width = sourceImages[0].width
    height = sourceImages[0].height

    # .load() all the images to get PixelAccess
    sourceImages = [ img.load() for img in sourceImages ]

    # Create output image to store the result and get PixelAccess
    outputImage = Image.new('RGB', (width, height))
    outputImagePixelAccess = outputImage.load()

    # Loop through all pixels
    for x in range(width):
        for y in range(height):
            pixels = [] # Clear the list of pixels for this x,y iteration
            for image in sourceImages: # Loop through all the images
                pixels.append(image[x, y]) # Store the pixel at x,y from the current image
            medianPixel = calculateMedianOfPixels(pixels) # Do the needful
            outputImagePixelAccess[x, y] = medianPixel # Assign that pixel to the output image

    # Save the results
    outputImage.save('Result.png')

    return outputImage

def chooseFolder():
    tk = tkinter.Tk()

    # print(os.path.abspath(os.curdir))

    tk.withdraw()
    tk.update()

    dir = filedialog.askdirectory(title='Choose folder of source images', initialdir=os.path.abspath(os.curdir))
    # print(dir)

    if (len(dir) == 0):
        exit()

    fileNames = os.listdir(dir)
    # print(fileNames)

    imageFiles = [ '%s/%s' % (dir, fileName) for fileName in fileNames ]
    # print(imageFiles)

    tk.destroy()

    return imageFiles

def main():
    # Ask the user for a folder
    files = chooseFolder()

    # Inform the user that stuff is happening
    print("\nWorking...")

    # Time when program started, used to time how long the program takes.
    startTime = time.clock()

    # Calculate the median image from a list of images
    finalImage = calculateMedianImage(files)

    # 'Stop' the clock. We don't want to time the following print statments too.
    endTime = time.clock()

    # Fanfare
    print("\nDone! Thank you for your patience.")
    # print("I was able to process %s %s x %s images in %.3f seconds.\n" % (len(sourceImages), width, height, endTime - startTime))
    print("I was able to process the %s images in %.3f seconds.\n" % (len(files), (endTime - startTime)))

    return finalImage

if __name__ == "__main__":
    main()
