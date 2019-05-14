# Nick van Santen, vansantennick@gmail.com  

# Be sure the images are jpg

print( "Importing...")

import func
import os

# Input, these files have to be in the "Images" folder
files = []

def manipulations(path):
    """The manipulations made on the images"""

    print ("\n   Working on %s\n" %(path))

    # Creates a folder with the results for the current image
    if not os.path.exists("Results\\%s" %(path)):
        os.makedirs("Results\\%s" %(path))

    # The variations made of the image
    func.pixelImage(path, 10, 10)
    func.animate(path)
    func.colorScale(path, 0)
    func.colorScale(path, 1)
    func.colorScale(path, 2)
    func.scan(path, 280)
    func.greyImage(path)
    func.colorSteps(path, 1)
    func.inverted(path)

print( "Starting...")

if os.path.exists("Images") and len(files) == 0:
    files = os.listdir("Images")
elif not os.path.exists("Images"):
    os.makedirs("Images")
    print("Please put the images in the 'Images' folder")

for file in files:
    
    # Checks if "file" is a map or folder
    extension = file[len(file) - 4:len(file)]
    if not(extension == ".jpg"):

        # Grabs all files in folder
        newFiles = os.listdir("Images\\%s"%(file))

        for file2 in newFiles:
            manipulations("%s\\%s"%(file, file2))
    else:

        manipulations(file)

os.startfile("Results")
