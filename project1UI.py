#! python3
# displaying images using pillow. Learned from http://stackoverflow.com/questions/28139637/how-can-i-display-an-image-using-pillow
# Thread with call back. Learned from http://stackoverflow.com/questions/8887408/about-threads-and-callbacks

# Ahh, submitting too close for comfort. I would need more time to get a 'fade in' effect.
# I appologize for the lack of comments in this file. I don't feel I have time to 'clean up' the code as much as I'd like and explain the 'what' 'why' 'how' that comments should provide. The code is short enough I hope it's 'self explanatory' enough. Sorry again.

from PIL import Image, ImageTk
import tkinter as tk
import threading
import project1
from time import sleep

def callback_func(image):
    global canvas, imageLoop, root, finalTkImage
    root.after_cancel(imageLoop)

    # image.convert(mode='RGBA')
    
    finalTkImage = ImageTk.PhotoImage(image)

    canvas.create_image(0,0, image=finalTkImage, anchor='nw')

def threaded_func(callback):
    global imageFiles
    finalImage = project1.calculateMedianImage(imageFiles)
    callback(finalImage)

imageIndex = 0;
timerTime = 300
def changeImage():
    global imageIndex, canvas, timerTime, tkImages, imageLoop
    imageIndex += 1;
    imageIndex = imageIndex % len(tkImages)
    canvas.create_image(0,0, image=tkImages[imageIndex], anchor='nw')
    imageLoop = canvas.after(timerTime, changeImage)
    timerTime -= 25
    if (timerTime <= 0):
        timerTime = 25

def onClosing():
    exit()

def main():
    global canvas, root, tkImages, imageLoop, imageFiles

    imageFiles = project1.chooseFolder()

    root = tk.Tk()

    sourceImages = [ Image.open(image) for image in imageFiles ]
    tkImages = [ ImageTk.PhotoImage(img) for img in sourceImages ]

    imageWidth = sourceImages[0].width
    imageHeight = sourceImages[0].height

    canvas = tk.Canvas(root, width = imageWidth, height = imageHeight)
    canvas.pack()
    imageLoop = canvas.after(50, changeImage)

    # bring to top
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

    # set up the thread and start it
    thr = threading.Thread(target=threaded_func, args=(callback_func,)).start()
    
    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.mainloop()

if __name__ == "__main__":
    main()