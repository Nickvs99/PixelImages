import numpy as np
from PIL import Image
import imageio
import os
import shutil
import math

def determineEdges(image, pixelsX, pixelsY):
    """ Returns the edges depending on the imageSize and the number of pixels in the x and y direction"""
    
    imageWidth = float(image.size[0])
    imageHeigth = float(image.size[1])

    
    pixelWidth = (imageWidth / pixelsX)
    pixelHeigth = (imageHeigth / pixelsY)

    # Gets the edge for the x direction
    imageXEdges = []
    for i in range(pixelsX + 1):
        xCor = i * pixelWidth

        imageXEdges.append(int(np.round(xCor)))

    # Gets the edge for the y direction
    imageYEdges = []
    for i in range(pixelsY  + 1):
        yCor = i * pixelHeigth

        imageYEdges.append(int(np.round(yCor)))
    
    # Removes duplicates, necessary for rounding
    imageXEdges = removeDupes(imageXEdges)
    imageYEdges = removeDupes(imageYEdges)

    # Return the edges
    return imageXEdges, imageYEdges

def removeDupes(array):
    """Removes duplicates in a sorted array"""

    i = len(array) - 1
    while i > 0:
        if array[i] == array[i - 1]:
            del array[i - 1]
        i -= 1
    return array

def animate(path):
    """ Creates an animation of a image which becomes sharper every frame
        Each frame is created through PixelImage()"""

    image = Image.open('Images\\%s' %(path))

    size = image.size
    # Determines how many frames have to be made
    if size[0] > size[1]:
        maxPower = math.log(size[0], 2)
    else:
        maxPower = math.log(size[1], 2)

    power = int(math.floor(maxPower))



    # Creates a frame, pixelizes the images for each step, the previous image gets passed on as a 
    # variable for optimizing
    while power >= 0:
        print("\nPower: ", power)
        image = pixelImage(image, 2 ** power, 2 ** power, animation = True, frame = power)
        power -= 1

    # Grabs all images from the temp directory
    images = []
    for filename in os.listdir("Results\\tempImages"):
        images.append(imageio.imread("Results\\tempImages\\%s" %(filename)))

    # Save the images as a gif
    imageio.mimsave("Results\\%s\\video.gif" %(path), images, fps = 1)

    # Deletes the tempimages folder
    shutil.rmtree('Results\\tempImages')

    return maxPower

def averageArea(pix, x1, x2, y1, y2):
    """ Returns the average color from an area rectangular given by x1, x2, y1 and y2"""

    RGBValues = [0] * 3
    for x in range(x1,x2):
        for y in range(y1,y2):
            for k in range(3):

                RGBValues[k] += pix[x,y][k]        

    area = (x2 -x1)*(y2-y1)
    RGBAvg = [0] * 3
    for i in range(3):
        RGBAvg[i] = RGBValues[i] / area

    avgColor = (int(RGBAvg[0]), int(RGBAvg[1]), int(RGBAvg[2]))
    
    return avgColor

def average(pix, pixels):
    """ Returns the average color from the list of pixels"""

    RGBValues = [0] * 3
    for pixel in pixels:

        x = pixel[0]
        y = pixel[1]

        for i in range(3):
            RGBValues[i] += pix[x,y][i]        
            
    RGBAvg = [0] * 3
    for i in range(3):
        RGBAvg[i] = RGBValues[i] / len(pixels)

    avgColor = (int(RGBAvg[0]), int(RGBAvg[1]), int(RGBAvg[2]))
    
    return avgColor

def colorIn(pix, color, x1, x2, y1, y2):
    """" All pixels in the area given by x1, x2, y1, y2 get the same color"""

    for x in range(x1,x2):
        for y in range(y1,y2):
            pix[x,y] = tuple([color[0],color[1],color[2]])

def pixelImage(path, pixelsX, pixelsY, **kwargs):
    """Creates a pixelized image"""

    # Checks if the function is used for making an animation
    if 'animation' in kwargs:
        animation = kwargs['animation']
        frame = kwargs['frame']
        im = path
    else:
        animation = False
        im = Image.open('Images\\%s' %(path))

    pix = im.load()
    edgesX, edgesY = determineEdges(im, pixelsX, pixelsY)

    # Colors an area determined by the edges with the same color
    for i in range(len(edgesX) - 1):
        for j in range(len(edgesY) - 1):
            
            pixels = []
            pixels.append([edgesX[i]       , edgesY[j]      ])
            pixels.append([edgesX[i + 1] - 1 , edgesY[j]       ])
            pixels.append([edgesX[i]       , edgesY[j + 1] - 1   ])
            pixels.append([edgesX[i + 1] - 1, edgesY[j + 1] - 1     ])

            avg2 = average(pix, pixels)
            
            colorIn(pix, avg2, edgesX[i], edgesX[i + 1] , edgesY[j], edgesY[j + 1] )


    if animation:
        if not os.path.exists('Results\\tempImages'):
            os.makedirs('Results\\tempImages')
        
        if frame < 10:
            string = "0%i" %(frame)
        else:
            string = frame
        im.save('Results\\tempImages\\Pixel_%s.jpg' %(string))
    else:
        im.save('Results\\%s\\Pixel_%sx%s.jpg' %(path, pixelsX, pixelsY))
    
    return im

def colorScale(path, colorIndex):
    """Creates a images with just one color"""

    image = Image.open('Images\\%s' %(path))

    pix = image.load()

    width = image.size[0]
    heigth = image.size[1]

    for i in range(width):
        for j in range(heigth):
            
            RGBValue = pix[i,j]

            color = [0, 0, 0]
            color[colorIndex] = RGBValue[colorIndex]

            pix[i,j] = tuple(color)

    # Gives the output the right name
    if colorIndex == 0:
        string = "Red"
    elif colorIndex == 1:
        string = "Green"
    else:
         string = "Blue"

    image.save("Results\\%s\\%s.jpg" %(path, string))

def scan(path, value, **kwargs):
    """ White-ish pixels change to 255,255,255 and 
        dark-ish pixels change to 0,0,0"""

    image = Image.open('Images\\%s' %(path))

    pix = image.load()

    width = image.size[0]
    heigth = image.size[1]

    for i in range(width):
        for j in range(heigth):

            RGBValue = pix[i,j]

            if RGBValue[0] + RGBValue[1] + RGBValue[2] > value:
                RGBValue = [255,255,255]
            else:
                RGBValue = [0,0,0]

            pix[i,j] = tuple(RGBValue)

    image.save("Results\\%s\\Scanned_%d.jpg" %(path, value))

def greyImage(path, **kwargs):
    """Creates a grey Image"""

    image = Image.open('Images\\%s' %(path))

    pix = image.load()

    width = image.size[0]
    heigth = image.size[1]

    for i in range(width):
        for j in range(heigth):

            RGBValue = pix[i,j]

            # Gets the average RGBValue
            grey = 1/3*(RGBValue[0] + RGBValue[1] + RGBValue[2])
            grey = int(grey)    
            pix[i,j] = tuple([grey, grey, grey])

    image.save("Results\\%s\\grey.jpg" %(path))
