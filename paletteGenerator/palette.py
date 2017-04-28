from colour import Color
import random
import math
from enum import IntEnum

class PType(IntEnum):
    ADJACENT = 1
    ANALOGOUS = 2
    COMPLEMENTARY = 3
    MONOCHROMATIC = 4
    SPLIT_COMPLEMENTARY = 5
    TETRADIC = 6
    TRIADIC = 7


# precondition: there are enough tokens to allow all recipients to receive minimumtokens
def distributedtokenarray(tokencount, recipientcount, minimumtokens):

    if tokencount < minimumtokens * recipientcount:
        raise Exception("TokenUnderflow")

    # declres an integer list where each token recipient receives the minimum token number
    tokens = []
    for i in range(recipientcount):
        tokens.append(minimumtokens)

    tokencount -= minimumtokens * recipientcount

    while tokencount > 0:
        tokens[random.randint(0, len(tokens) - 1)] += 1
        tokencount -= 1

    return tokens


# returns a color with the same hue as existingcolor
# but randomly changed brightness and saturation
def differentcolorwithsamehue(existingcolor):
    return Color(existingcolor, saturation=random.random(), luminance=random.random())


def monochromaticpalette(basecolor, size):
    palette = []

    palette.append(basecolor)
    for i in range(size - 1):
        palette.append(basecolor.differentcolorwithsamehue(palette[0]))


def colorcast(colour):
    floats = colour.get_rgb()
    red = int(round(floats[0] * 255))
    blue = int(round(floats[1] * 255))
    green = int(round(floats[2] * 255))
    integers = (red, blue, green)
    return integers


def colorwithchangedhue(color, hueshift):
    return Color(color, hue=(color.get_hue() + hueshift) % 1)


def similarcolorexists(palette, color):
    for existingcolor in palette:
        colourdifference = math.sqrt(math.pow(color.red - existingcolor.red, 2) + math.pow(color.blue - existingcolor.blue, 2) + math.pow(color.green - existingcolor.green, 2))
        if colourdifference < 0.2:
            return True
    return False


def colourswillcontrast(colorone, colortwo):
    # finds the difference of the colours brightness indexes
    brightnessone = (299 * 255 * colorone.red + 587 * 255 * colorone.green + 114 * 255 * colorone.blue) / 1000
    brightnesstwo = (299 * 255 * colortwo.red + 587 * 255 * colortwo.green + 114 * 255 * colortwo.blue) / 1000
    if abs(brightnessone - brightnesstwo) > 125:
        brightnessdiff = True
    else:
        brightnessdiff = False

    huescore = abs(colorone.red - colortwo.red) + abs(colorone.green - colortwo.green) + abs(colorone.blue - colortwo.blue)
    if huescore > 500 and brightnessdiff is True:
        return True
    else:
        return False


def findstandoutcolour(palette, basecolor):
    for color in palette:
        if colourswillcontrast(color, basecolor):
            return color

    if basecolor.luminance < 0.5:
        return Color("white")
    else:
        return Color("black")


# returns a list of colours following a algorithm for picking complimenting colours.
# chosentype : PType - The palette style to be produced
# seedColor : Color - The colour to base the palette on.
# size : int - The length of the colour list
def styledpalette(chosentype, seedcolor, size):

    if chosentype == PType.ADJACENT:
        hueshift = random.uniform(0.1, 0.3)
        seedcolors = [seedcolor, Color(seedcolor, hue=(seedcolor.get_hue() + hueshift) % 1)]
        return randomisedpalette(seedcolors, size)

    elif chosentype == PType.ANALOGOUS:
        hueshift = random.uniform(0.1, 0.3)
        seedcolors = [seedcolor, Color(seedcolor, hue=(seedcolor.get_hue() + hueshift) % 1),
                      Color(seedcolor, hue=(seedcolor.get_hue() - hueshift) % 1)]
        return randomisedpalette(seedcolors, size)

    elif chosentype == PType.COMPLEMENTARY:
        seedcolors = [seedcolor, Color(seedcolor, hue=(seedcolor.get_hue() + 0.5) % 1)]
        return randomisedpalette(seedcolors, size)

    elif chosentype == PType.MONOCHROMATIC:
        seedcolors = [seedcolor]
        return randomisedpalette(seedcolors, size)

    elif chosentype == PType.SPLIT_COMPLEMENTARY:
        hueshift = random.uniform(0.1, 0.3)
        complement = Color(seedcolor, hue=(seedcolor.get_hue() + 0.5) % 1)
        split_comp_left = Color(complement, hue=complement.get_hue() - hueshift)
        split_comp_right = Color(complement, hue=complement.get_hue() + hueshift)
        seedcolors = [seedcolor, split_comp_left, split_comp_right]
        return randomisedpalette(seedcolors, size)

    elif chosentype == PType.TETRADIC:
        seedcolors = [seedcolor]
        seedcolors.append(colorwithchangedhue(seedcolor, 0.25))
        seedcolors.append(colorwithchangedhue(seedcolor, 0.5))
        seedcolors.append(colorwithchangedhue(seedcolor, 0.75))
        return randomisedpalette(seedcolors, size)

    elif chosentype == PType.TRIADIC:
        seedcolors = [seedcolor]
        seedcolors.append(colorwithchangedhue(seedcolor, 0.33))
        seedcolors.append(colorwithchangedhue(seedcolor, 0.66))
        return randomisedpalette(seedcolors, size)
    else:
        print("ChosenType invalid")


def randomisedpalette(colors, size):
    slotdistribution = distributedtokenarray(size, len(colors), 1)
    palette = []
    i = 0
    for color in colors:
        palette.append(color)
        for colorcount in range(slotdistribution[i]-1):
            newcolor = differentcolorwithsamehue(color)
            while similarcolorexists(palette, newcolor):
                newcolor = differentcolorwithsamehue(color)
            palette.append(newcolor)
        i += 1
    return palette
