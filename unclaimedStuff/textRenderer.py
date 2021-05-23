
from PIL import Image, ImageDraw, ImageFont
import math
import os

class TextImage():
    """Creates an image of rendered Minecraft text which supports bold, italics, bold italics, color codes and line breaks"""
    def __init__(self, text, fontSize=48, background=False, width=None, height=None, margin=0, textShadow=True):
        
        self.colors = colors = {
            "&0":"#000000",
            "&1":"#0000AA",
            "&2":"#00AA00",
            "&3":"#00AAAA",
            "&4":"#AA0000",
            "&5":"#AA00AA",
            "&6":"#FFAA00",
            "&7":"#AAAAAA",
            "&8":"#555555",
            "&9":"#5555FF",
            "&a":"#55FF55",
            "&b":"#55FFFF",
            "&c":"#FF5555",
            "&d":"#FF55FF",
            "&e":"#FFFF55",
            "&f":"#FFFFFF" }
        self.shadowColors = {
            "&0":"#000000",
            "&1":"#00002A",
            "&2":"#002A00",
            "&3":"#002A2A",
            "&4":"#2A0000",
            "&5":"#2A002A",
            "&6":"#2A2A00",
            "&7":"#2A2A2A",
            "&8":"#151515",
            "&9":"#15153F",
            "&a":"#153F15",
            "&b":"#153F3F",
            "&c":"#3F1515",
            "&d":"#3F153F",
            "&e":"#3F3F15",
            "&f":"#3F3F3F" }
        
        thisDir, this_filename = os.path.split(__file__)
        fontsDir = os.path.join(thisDir, "fonts")

        self.normalFont = ImageFont.truetype(fontsDir + '/regular.otf', fontSize)
        self.boldFont = ImageFont.truetype(fontsDir + '/bold.otf', fontSize)
        self.italicFont = ImageFont.truetype(fontsDir + '/italics.otf', fontSize)
        self.boldItalicFont = ImageFont.truetype(fontsDir + '/bold-italics.otf', fontSize)
        self.arialFont = ImageFont.truetype(fontsDir + '/ArialUnicodeMS.ttf', fontSize)

        self.font = self.normalFont
        self.fontSize = fontSize
        self.textShadow = textShadow

        self.rowHeight = self.fontSize
        self.width = width
        self.margin = margin


        self.text = text.replace("§", "&").replace("\n", "\\n")
        self.textLength = self.getTextLength(self.text)
        self.wrapText = False
        if width == None:
            self.width = self.getMaxWidth(self.text)
        else:
            self.width = width
            self.wrapText = True
        
        self.rows = self.text.count(r"\n") + 1
        if self.rows == 1:
            self.rows = math.ceil(self.textLength / self.width)
        
        if height == None:
            self.height = self.rows * self.rowHeight
        else:
            self.height = height

        self.currPos = [self.margin, 0]
        self.currRow = 1

        self.color = "&f"
        self.bold = False
        self.italic = False
        self.background = background

        self.words = [i + " " for i in self.text.split(" ")]
    
    def getTextLength(self, text):
        """Gets the length of the text in pixels"""
        length = self.margin
        bold = False
        italic = False
        for letter in range(len(text)):
            if text[letter] == "&" and text[letter + 1] in "abcdef0123456789lorkmn":
                continue
            elif text[letter] == "\\" and text[letter + 1] == "n":
                continue
            elif text[letter - 1] == "\\" and text[letter] == "n":
                continue
            elif text[letter-1] == "&":
                if "&" + text[letter] in self.colors:
                    continue
                elif text[letter] == "l":
                    bold = True
                    continue
                elif text[letter] == "o":
                    italic = True
                    continue
                elif text[letter] == "r":
                    bold = False
                    italic = False
                    continue
                elif text[letter] in "kmn":
                        continue
            if text[letter].lower() not in "abcdefghijklmnopqrstuvwxyz0123456789`~-_=+[{]}\|;:'\",<.>/?!@#$%^&*()":
                length += self.arialFont.getsize(text[letter])[0]
            elif bold == True and italic == True:
                length += self.boldItalicFont.getsize(text[letter])[0]
            elif bold == True:
                length += self.boldFont.getsize(text[letter])[0]
            elif italic == True:
                length += self.italicFont.getsize(text[letter])[0]
            else:
                length += self.normalFont.getsize(text[letter])[0]
        if self.textShadow == True:
            length += math.floor(self.fontSize / 7) - 1
        return length

    def getMaxWidth(self, text):
        """Returns the width of the longest line in the text"""

        width = self.margin
        bold = False
        italic = False
        widths = []
        for letter in range(len(text)):
            if text[letter] == "&" and text[letter + 1] in "abcdef0123456789lorkmn":
                continue
            elif text[letter] == "\\" and text[letter + 1] == "n":
                continue
            elif text[letter - 1] == "\\" and text[letter] == "n":
                widths.append(width)
                width = self.margin
                continue
            elif text[letter-1] == "&":
                if "&" + text[letter] in self.colors:
                    continue
                elif text[letter] == "l":
                    bold = True
                    continue
                elif text[letter] == "o":
                    italic = True
                    continue
                elif text[letter] == "r":
                    bold = False
                    italic = False
                    continue
                elif text[letter] in "kmn":
                    continue
            if text[letter].lower() not in "abcdefghijklmnopqrstuvwxyz0123456789`~-_=+[{]}\|;:'\",<.>/?!@#$%^&*()":
                width += self.arialFont.getsize(text[letter])[0]
            elif bold == True and italic == True:
                width += self.boldItalicFont.getsize(text[letter])[0]
            elif bold == True:
                width += self.boldFont.getsize(text[letter])[0]
            elif italic == True:
                width += self.italicFont.getsize(text[letter])[0]
            else:
                width += self.normalFont.getsize(text[letter])[0]
        widths.append(width)
        if len(widths) == 0:
            return width
        maxWidth = max(widths)
        if self.textShadow == True:
            maxWidth += math.floor(self.fontSize / 7) - 1
        return maxWidth
        
    def drawText(self):
        """Draw the text onto an image"""
        if self.background == True:
            backgroundColor = (0, 0, 0, 128)
        else:
            backgroundColor = (0, 0, 0, 0)

        image = Image.new("RGBA", (self.width, self.height), backgroundColor)

        draw = ImageDraw.Draw(image)

        for word in self.words:
            if self.currPos[0] + self.getTextLength(word) > self.width and self.wrapText == True:
                self.currRow += 1
                self.currPos = [self.margin, self.currRow]
            for letter in range(len(word)):
                if word[letter] == "&" and word[letter + 1] in "abcdef0123456789lorkmn":
                    continue
                elif word[letter] == "\\" and word[letter + 1] == "n":
                    continue
                elif word[letter - 1] == "\\" and word[letter] == "n":
                    self.currRow += 1
                    self.currPos = [self.margin, self.currRow]
                    self.bold = False
                    self.italic = False
                    letter += 1
                    continue
                elif word[letter - 1] == "&":
                    if "&" + word[letter] in self.colors:
                        self.color = "&" + word[letter]
                        continue
                    elif word[letter] == "l":
                        self.bold = True
                        continue
                    elif word[letter] == "o":
                        self.italic = True
                        continue
                    elif word[letter] == "r":
                        self.bold = False
                        self.italic = False
                        self.color = "&f"
                        continue
                    elif word[letter] in "kmn":
                        continue
                heightBump = 0
                if word[letter].lower() not in "abcdefghijklmnopqrstuvwxyz0123456789`~-_=+[{]}\|;:'\",<.>/?!@#$%^&*()":
                    self.font = self.arialFont
                    heightBump = self.fontSize / 4
                elif self.bold == True and self.italic == True:
                    self.font = self.boldItalicFont
                elif self.bold == True:
                    self.font = self.boldFont
                elif self.italic == True:
                    self.font = self.italicFont
                else:
                    self.font = self.normalFont

                if self.textShadow == True:
                    draw.text((self.currPos[0] + math.floor(self.fontSize / 7) - 1, ((self.currRow-1) * self.rowHeight - heightBump) + math.floor(self.fontSize / 7) - 1), word[letter], font=self.font, fill=self.shadowColors[self.color])
                draw.text((self.currPos[0], ((self.currRow-1) * self.rowHeight - heightBump)), word[letter], font=self.font, fill=self.colors[self.color])
                self.currPos[0] += self.font.getsize(word[letter])[0]

        return image
        


#testData = "&2Guild > &6[MVP&0++&6] UnclaimedBloom6 &2[DL]&f: Noob"
#abc = TextImage("formatted", background=True, margin=6).drawText()
#abc.show()

