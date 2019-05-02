# Be sure the images are jpg

print( "Importing...")

import func
import os
import time

# Input, these files have to be in the "Images" folder
files = []

def name(path):
    
    print ("\n   Working on %s\n" %(path))

    # Creates a folder with the results for the current image
    if not os.path.exists("Results\\%s" %(path)):
        os.makedirs("Results\\%s" %(path))

    # The variations made of the image
    func.pixelImage(path, 10, 10)
    func.animate(path)
    # func.colorScale(path, 0)
    # func.colorScale(path, 1)
    # func.colorScale(path, 2)
    func.scan(path, 280)
    func.grey(path)


print( "Starting...")


if os.path.exists("Images") and len(files) == 0:
    files = os.listdir("Images")
elif not os.path.exists("Images"):
    os.makedirs("Images")
    print("Please put the images in the 'Images' folder")

for file in files:
    
    # Checks if "file" is a map or folder
    extension = file[len(file) - 4:len(file)]
    if not(extension == ".jpg" or extension == ".png"):

        # Grabs all files in folder
        newFiles = os.listdir("Images\\%s"%(file))

        for file2 in newFiles:
            name("%s\\%s"%(file, file2))
    else:

        name(file)



os.startfile("Results")