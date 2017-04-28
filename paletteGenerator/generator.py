# Author: John WIllcox-Beney, 2017
from colour import Color
from PIL import Image, ImageDraw, ImageFont
import random
import palette
from palette import randomisedpalette, colorwithchangedhue, colorcast, findstandoutcolour
from time import sleep
import tweepy

# Use Twitter's API to generate these tokens.
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""

PALETTESIZE = 5

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

while True:
    seedColor = Color(rgb=(random.random(), random.random(), random.random()))
    ChosenType = random.randint(1, 7)
    finalColors = palette.styledpalette(ChosenType, seedColor, PALETTESIZE)

    fnt = ImageFont.truetype("Lato-Regular.ttf", 10)
    img = Image.new("RGBA", (500, 200), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i in xrange(PALETTESIZE):
        draw.rectangle((i * 100, 0, (i + 1)*100, 200), fill=colorcast(finalColors[i]))
        draw.text((i * 100 + 7, 180), finalColors[i].hex.upper(), font=fnt,
                  fill=colorcast(findstandoutcolour(finalColors, finalColors[i])))
    draw = ImageDraw.Draw(img)
    print "palette generated..."

    filename = "paletteBotPalette.png"
    img.save(filename)
    print "saved..."
    api.update_with_media(filename)
    print "and uploaded!"
    # waits for 1 hour after posting an image
    sleep(60*60)
