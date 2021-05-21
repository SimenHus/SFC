from PIL import Image, ImageDraw, ImageFont
from personalization import *
from datetime import datetime
import time
import sys

class ImageObject:

    def __init__(self, frame, background, textColor, font):
        self.backgroundColor = background #Saves background color choice
        self.textColor = textColor #Saves font color choice
        self.frameSize = frame #Saves frame dimensions
        self.rect = (int(frame[0]/5), int(frame[1]*2/3), 0, 0) #Saves cell rectangle dimensions
        self.cellFont = ImageFont.truetype("{}.ttf".format(font), size=int(self.rect[0]/5)) #Saves font and fontsize for cell number
        self.actionFont = ImageFont.truetype("{}.ttf".format(font), size=int(self.rect[0]/10)) #Saves font and fontsize for action text
        self.img = Image.new('RGB', (frame[0], 1), background) #Creates the baseline for img object
        self.draw = ImageDraw.Draw(self.img) #Defines drawing environment
        self.actionBox = [int(self.rect[0]*(1/20 + 1/2)), int(self.actionFont.getsize("0")[1]*3)] #Define action box size. Padding included

    def addSequence(self):
        width, height = self.img.size #Read current image dimensions
        oldImage = self.img #Local copy of image object
        self.img = Image.new('RGB', (width, height + self.frameSize[1]), self.backgroundColor) #Creates a new, expanded image
        self.img.paste(oldImage, (0, 0)) #Pastes the old image at the start of the new image
        self.draw = ImageDraw.Draw(self.img) #Recreates drawing environment

        slowPrint("Step name:\n(S1, S2, M0, M1 etc.)")
        cell = input()


        initiationCell = False
        slowPrint("Is this an initiation step?\n(yes or true to add initiation marker)")
        initInput = input().lower()
        if initInput == "true" or initInput == "yes":
            initiationCell = True
        rectCords = self.cellRectangle(cell, initiationCell) #Calls function to create cell rectangle

        actionList = self.requestAction() #List of actions from user
        #Creates action rectangles if user has inputed an action
        if len(actionList) > 0:
            actionLineEnd = self.actionLine(rectCords)
            self.actions(actionLineEnd, actionList)

        slowPrint("Criteria to exit step:\n(X0, X1 etc.)")
        criteria = input()
        self.nextStep(rectCords, criteria)

        slowPrint("SFC updated")

    def cellRectangle(self, cell, initiationCell):
        width, height = self.img.size #Read current image dimensions
        rectWidth, rectHeight, rectStartX, rectStartY = self.rect #Read saved rectangle dimensions
        rectStartY += int(height - self.frameSize[1]) #Repositions y start for rectangle to fit new image

        rectCords = self.defineRectangle([rectWidth, rectHeight, rectStartX, rectStartY]) #Set coordinates for the cell rectangle
        self.centerText(rectCords, cell, self.cellFont)

        if initiationCell: #Creates an extra square to indicate initiation cell
            padding = int(rectWidth/10)
            initiationRectCords = (rectCords[0] + padding, rectCords[1] + padding,
            rectCords[2] - padding, rectCords[3] - padding)
            self.draw.rectangle(initiationRectCords, fill=None, outline="black")
        return rectCords

    def actionLine(self, rectCords):
        x0, y0, x1, y1 = rectCords #Read rectangle dimensions
        actionLineLength = int((x1 - x0)/5) #Define length af line between rectangle and action description
        actionLineCords = (x1, int(y0 + (y1 - y0)/2)) #Define anchor points for action line
        self.draw.line((actionLineCords[0], actionLineCords[1], #Line break to save space
        actionLineCords[0] + actionLineLength, actionLineCords[1]), fill="black", width=1) #Draw line
        return (actionLineCords[0] + actionLineLength, actionLineCords[1]) #Return ending coordinates

    def actions(self, actionLineEnd, actionList):
        rectWidth, rectHeight = self.actionBox
        startingCorner = (int(actionLineEnd[0]), int(actionLineEnd[1] - rectHeight*len(actionList)/2)) #Defines the starting corner to create boxes
        for i in range(len(actionList)): #Loop to create boxes and text
            currentCorner = [startingCorner[0], startingCorner[1] + i*rectHeight]
            endX = startingCorner[0] + rectWidth*4
            if actionList[i][0] != None:
                typeDimensions = (rectWidth, rectHeight,
                currentCorner[0], currentCorner[1])
                typeRect = self.defineRectangle(typeDimensions)
                typeText = actionList[i][0]
                multiline = False
                if actionList[i][1] != None:
                    typeText = "{}\nt#{}{}".format(actionList[i][0], actionList[i][1], actionList[i][2])
                    multiline = True
                self.centerText(typeRect, typeText, multiline = multiline)
                currentCorner[0] += rectWidth

            if actionList[i][4] != None:
                connectedCellDimensions = (rectWidth, rectHeight,
                startingCorner[0] + rectWidth*3, startingCorner[1] + i*rectHeight)
                connectedCellRect = self.defineRectangle(connectedCellDimensions)
                self.centerText(connectedCellRect, actionList[i][4])
                endX -= rectWidth

            actionRect = self.defineRectangle([endX - currentCorner[0], rectHeight, currentCorner[0], currentCorner[1]])
            actionText = actionList[i][3]
            actionWidth, actionHeight = self.actionFont.getsize(actionText)
            multiline = False
            if actionWidth > endX - currentCorner[0]:
                actionText = "{}\n{}".format(actionText[:int(len(actionText)/2)], actionText[int(len(actionText)/2):])
                multiline = True
            self.centerText(actionRect, actionText, multiline = multiline)


    #Function to center text in a given rectangle
    def centerText(self, rectangle, text, font = None, multiline = False):
        if font == None: font = self.actionFont
        x0, y0, x1, y1 = rectangle
        textWidth, textHeight = font.getsize(text)
        if multiline:
            textHeight*=2
            sections = text.split("\n")
            if len(sections[1]) > len(sections[0]): sections.reverse()
            textWidth = font.getsize(sections[0])[0]
        textCords = (
        int(x0 + (x1 - x0)/2 - textWidth/2),
        int(y0 + (y1 - y0)/2 - textHeight/2))
        self.draw.text(textCords, text, fill=self.textColor, font=font, align="center")
        return textCords

    #Function to get rectangle cords given top left corner and dimensions
    def defineRectangle(self, specifications):
        width, height, x0, y0 = specifications
        cords = (int(x0), int(y0), int(width + x0 - 1), int(height + y0 - 1))
        self.draw.rectangle(cords, fill=self.backgroundColor, outline="black")
        return cords

    def nextStep(self, rectCords, criteria):
        width, height = self.img.size #Read current image dimensions
        rectWidth, rectHeight, rectStartX, rectStartY = self.rect #Read saved rectangle dimensions
        criteriaWidth, criteriaHeight = self.actionFont.getsize(criteria) #Calculate text size

        finalLineCords = (int(rectCords[0] + rectWidth/2), int(rectCords[3]),
        int(rectCords[0] + rectWidth/2), int(height)) #Coordinates for the line to next sequence
        criteriaTextCords = (finalLineCords[0] + 4,
        finalLineCords[1] + int((finalLineCords[3] - finalLineCords[1])/2 - criteriaHeight/2)) #Coordinates for criteria text

        self.draw.line(finalLineCords, fill="black", width=1) #Draw line that connects to next sequence segment
        self.draw.text(criteriaTextCords, criteria, fill=self.textColor, font=self.actionFont) #Draw criterias


    def requestAction(self):
        actionList = []
        while True:
            slowPrint("Do you want to add another action to the cell?\n(yes to add, no to continue)")
            actionCheck = input().lower()
            if actionCheck == "yes":
                newAction = [None for i in range(5)]
                slowPrint("Type of action (N, R, L, D etc.)\nBlank for no particular type")
                type = input()
                if type != "": newAction[0] = type
                if type.upper() == "L" or type.upper() == "D":
                    slowPrint("Time constant:")
                    newAction[1] = input()
                    slowPrint("Unit of time:")
                    newAction[2] = input()
                slowPrint("Describe the action:")
                newAction[3] = input()
                slowPrint("Connected cells (CS0, TS0 etc.)\nBlank if no connected cells")
                connectedCell = input()
                if connectedCell != "": newAction[4] = connectedCell
                actionList.append(newAction)
                continue
            if actionCheck == "no":
                break
            slowPrint("Bad input, try again.")
        return actionList

    def show(self):
        slowPrint("Image opening...")
        self.img.show() #Preview of the image

    def save(self, destination, format):
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d_%m_%H%M")
        self.img.save("{}{}.{}".format(destination, dt_string, format), format) #Save image file
        slowPrint("Image saved to {}{}.{}".format(destination, dt_string, format))



#Function to print text with a certain flow instead of everything at once
def slowPrint(text):
    delay = 0.02
    text+="\n"
    for x in text:
        print(x, end="")
        time.sleep(delay)
        sys.stdout.flush()



img = ImageObject(frame, background, textColor, font) #Creates image object
availableActions = ["Add sequence", "Save", "Show", "Quit"] #Actions available to user

slowPrint("Actions are not case sensitive")
while True:
    slowPrint("\nAvailable actions:")
    for x in availableActions: slowPrint(x)
    slowPrint("What do you want to do with your SFC?\n")
    userAction = input().lower()
    if userAction == "add sequence": img.addSequence()
    if userAction == "show": img.show()
    if userAction == "save": img.save(path, fileName, fileFormat)
    if userAction == "quit":
        input("Press enter to exit...")
        break
