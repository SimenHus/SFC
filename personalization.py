import os

#Color definition
grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)
background = white #Variable to be passed to Image class
textColor = black #Variable to be passed to Image class

#Define image
fileName = "SFC" #Picture filename
fileFormat = "png" #Picture file format. PNG recommended

#Standard values
frame = (1000, 300) #(width, height)
font = "arial"


#Create folder to save pictures
folderName = "Bilder" #Folder that will be created for image storing
path = "{}\{}".format(os.getcwd(), folderName) #Variable where the picture will be saved
try:
    os.mkdir(path) #Creates folder
    print("Created folder {} in directory {}".format(folderName, path))
except:
    pass #If folder excists, pass
finally:
    path+= "\\"
