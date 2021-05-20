from PIL import Image, ImageDraw, ImageFont
from personalization import *
import time
import sys

class ImageObject:

    def __init__(self, frame, rect, background, textColor, font):
        self.backgroundColor = background #Saves background color choice
        self.textColor = textColor #Saves font color choice
        self.frameSize = frame #Saves frame dimensions
        self.rect = rect #Saves cell rectangle dimensions
        self.cellFont = ImageFont.truetype("{}.ttf".format(font), size=int(rect[0]/5)) #Saves font and fontsize for cell number
        self.actionFont = ImageFont.truetype("{}.ttf".format(font), size=int(rect[0]/10)) #Saves font and fontsize for actions
        self.img = Image.new('RGB', (frame[0], 1), background) #Creates the baseline for img object
        self.draw = ImageDraw.Draw(self.img) #Defines drawing environment

    def addSequence(self, info):
        cell, type, action, criteria, initiationCell, timeConstant = info
        width, height = self.img.size #Read current image dimensions
        oldImage = self.img #Local copy of image object
        self.img = Image.new('RGB', (width, height + self.frameSize[1]), self.backgroundColor) #Creates a new, expanded image
        self.img.paste(oldImage, (0, 0)) #Pastes the old image at the start of the new image
        self.draw = ImageDraw.Draw(self.img) #Recreates drawing environment

        rectWidth, rectHeight, rectStartX, rectStartY = self.rect #Read saved rectangle dimensions
        rectStartY += height #Repositions y start for rectangle to fit new image
        rectCords = (rectStartX, rectStartY, rectStartX + rectWidth, rectStartY + rectHeight) #Set coordinates for the cell rectangle
        self.draw.rectangle(rectCords, fill="white", outline="black") #Draw rectangle

        if initiationCell: #Creates an extra square if the cell is set as initiation cell
            padding = int(rectWidth/10)
            initiationRectCords = (rectCords[0] + padding, rectCords[1] + padding,
            rectCords[2] - padding, rectCords[3] - padding)
            self.draw.rectangle(initiationRectCords, fill=None, outline="black")

        cellWidth, cellHeight = self.cellFont.getsize(cell) #Find cell number dimensions
        cellCordsAnchor = [rectStartX + int(rectWidth/2), rectStartY + int(rectHeight/2)] #Find the base position for the dynamic cell number
        cellCords = (cellCordsAnchor[0] - int(cellWidth/2), cellCordsAnchor[1] - int(cellHeight/2)) #Find starting coordinates for cell number
        self.draw.text(cellCords, cell, fill=self.textColor, font=self.cellFont) #Draw cell number

        actionLineLength = int(rectWidth/5) #Define length og line between rectangle and action description
        actionLineCords = (rectStartX + rectWidth, rectStartY + int(rectHeight/2)) #Define anchor points for action line
        self.draw.line((actionLineCords[0], actionLineCords[1], #Line break to save space
        actionLineCords[0] + actionLineLength, actionLineCords[1]), fill="black", width=1) #Draw line

        blankSpaceX = 0
        blankSpaceY = 0
        actionWidth, actionTextHeight = self.actionFont.getsize(action) #Define rectangle dimensions for action text
        if timeConstant == None:
            actionTypeWidth, actionHeight = self.actionFont.getsize("t#0s")
            typeWidth, typeHeight = self.actionFont.getsize(type)
            blankSpaceX = int(actionTypeWidth/2 - typeWidth/2)
            blankSpaceY = int(actionHeight - typeHeight/2)
        else:
            actionTypeWidth, actionHeight = self.actionFont.getsize(timeConstant)
        actionHeight *=2
        padding = int(actionHeight/4) #Padding/2 is added around all text inside action boxes
        actionWidth += padding
        actionHeight += padding
        actionTypeWidth += padding
        actionXStart = actionLineCords[0] + actionLineLength #Find upper left x for actions
        actionYStart = actionLineCords[1] - int(actionHeight/2) # Find upper left y for actions
        actionTypeRectCords = (actionXStart, actionYStart,
        actionXStart + actionTypeWidth, actionYStart + actionHeight) #Define coordinates for action type rectangle
        actionTextRectCords = (actionTypeRectCords[2], actionTypeRectCords[1],
        actionTypeRectCords[2] + actionWidth, actionTypeRectCords[3]) #Define coordinates for action text rectangle
        self.draw.rectangle(actionTypeRectCords, fill="white", outline="black") #Draw action boxes
        self.draw.rectangle(actionTextRectCords, fill="white", outline="black")
        if timeConstant != None:
            type = """{}
{}""".format(type, timeConstant)
        self.draw.text((actionTypeRectCords[0] + blankSpaceX + int(padding/2), actionTypeRectCords[1]  + blankSpaceY + int(padding/2)),
        type, fill=self.textColor, font=self.actionFont, align="center") #Legger til text

        self.draw.text((actionTextRectCords[0] + int(padding/2), actionTextRectCords[1] + int(actionHeight/2 - actionTextHeight/2)),
        action, fill=self.textColor, font=self.actionFont) #Legger til text

        finalLineCords = (rectCords[0] + int(rectWidth/2), rectCords[3],
        rectCords[0] + int(rectWidth/2), height + self.frameSize[1]) #Coordinates for the line to next sequence
        criteriaWidth, criteriaHeight = self.actionFont.getsize(criteria)
        criteriaTextCords = (finalLineCords[0] + 4,
        finalLineCords[1] + int((finalLineCords[3] - finalLineCords[1])/2 - criteriaHeight/2)) #Coordinates for criteria text
        self.draw.line(finalLineCords, fill="black", width=1) #Draw line that connects to next sequence segment
        self.draw.text(criteriaTextCords, criteria, fill=self.textColor, font=self.actionFont) #Draw criterias

        slowPrint("SFC updated")


    def show(self):
        slowPrint("Image opening...")
        self.img.show() #Preview of the image

    def save(self, destination, name, format):
        self.img.save("{}{}.{}".format(destination, name, format), format) #Save image file
        slowPrint("Image saved to {}{}.{}".format(destination, name, format))


def requestInfo():
    global chosenInit
    slowPrint("Step name (S1, S2, M0, M1 etc.)")
    cell = input()
    slowPrint("Action type (N, R, S, L etc)")
    type = input()
    timeConstant = None
    if type.upper() == "L":
        slowPrint("How long is the limitation?")
        timeConstant = "t#{}s".format(input())
    elif type.upper() == "D":
        slowPrint("How long is the time delay?")
        timeConstant = "t#{}s".format(input())
    slowPrint("Action to perform")
    action = input()
    slowPrint("Criteria to continue (X0, X1 etc.)")
    criteria = input()
    initiationCell = False
    if not chosenInit:
        slowPrint("Is this an initiation step? (yes or true to add initiation marker)")
        initiationCell = input().lower()
        if initiationCell == "true" or initiationCell == "yes":
            initiationCell = True
            chosenInit = True
    return cell, type, action, criteria, initiationCell, timeConstant

def slowPrint(text):
    delay = 0.02
    text+="\n"
    for x in text:
        print(x, end="")
        time.sleep(delay)
        sys.stdout.flush()


chosenInit = False
img = ImageObject(frame, rect, background, textColor, font)
availableActions = ["Add sequence", "Save", "Show", "Quit"]

slowPrint("Actions are not case sensitive")
while True:
    slowPrint("\nAvailable actions:")
    for x in availableActions: slowPrint(x)
    slowPrint("What do you want to do with your SFC?\n")
    userAction = input().lower()
    if userAction == "add sequence": img.addSequence(requestInfo())
    if userAction == "show": img.show()
    if userAction == "save": img.save(path, fileName, fileFormat)
    if userAction == "quit":
        input("Press enter to exit...")
        break
