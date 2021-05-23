from PIL import Image, ImageDraw, ImageFont
from unclaimedStuff import textRenderer as tr
import math
import json


testData = [
    "&e#1: &6[MVP&0++&6] UnclaimedBloom6 &f- &3153,680,203 XP &6(60)",
    "&f#2: &a[VIP] HiEthane &f- &371,597,486 XP &6(53)",
    "&6#3: &b[MVP&d+&b] mestariess &f- &369,982,138 XP &6(53)",
    "&7#4: &a[VIP] AverageScyllaFan - &357,048,477 XP &6(50)",
    "&7#5: &b[MVP&2+&b] _Marwan_ &f- &347,066,047 XP &6(47)",
    "&7#6: &c[&fYOUTUBE&c] MrIcyTea &f- &330,983,935 XP &6(42)",
    "&7#7: &b[MVP&9+&b] dieler &f- &330,650,455 XP &6(42)",
    "&7#8: &b[MVP&3+&b] Shockser &f- &330,438,862 XP &6(42)",
    "&7#9: &b[MVP&9+&b] Waterflames &f- &327,888,797 XP &6(41)",
    "&7#10: &b[MVP&f+&b] Snoobledorf &f- &325,166,755 XP &6(39)",    
]

def makeLb(title, data, centered=False, margin=0, background=False):
    images = [tr.TextImage(data[i].replace("#1:", "&e#1").replace("#2:", "&f#2").replace("#3:", "&6#3"), background=background, margin=margin).drawText() for i in range(len(data))]
    title = tr.TextImage(title, background=background, margin=margin).drawText()

    width = int(max([i.width for i in images]) * 1.1)
    height = 48 * (len(images) + 2)

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    if centered == True:
        titlePos = int((width - title.width) / 2)
    else:
        titlePos = margin

    img.paste(title, (titlePos, 0))
    for i in range(len(images)):
        if centered == True:
            xPos = int((width - images[i].width) / 2)
        else:
            xPos = margin
        img.paste(images[i], (xPos, (i + 2) * 48))
    return img

#a = makeLb("&3Combat Leaderboard", data, centered=True)
#a.show()
#a.save("LB.png")