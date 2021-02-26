import discord
import requests
import math
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
import random
import json

bot = commands.Bot(command_prefix="*")
api_key = open("API_KEY")
api_key = api_key.read()

skillProgression = [50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425, 97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425, 4722425, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425, 17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425, 38072425, 40972425, 44072425, 47472425, 51172425, 55172425];
runecraftingProgression = [0, 50, 150, 275, 435, 635, 885, 1200, 1600, 2100, 2725, 3510, 4510, 5760, 7325, 9325, 11825, 14950, 18950, 23950, 30200, 38050, 47850, 60100, 75400]
dungeonProgression = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640, 3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640, 453559640, 569809640]
skills = [["taming","tamingEXP"],["mining","miningEXP"],["foraging","foragingEXP"],
            ["enchanting","enchantingEXP"],["farming","farmingEXP"],
            ["combat","combatEXP"],["fishing","fishingEXP"],["alchemy","alchemyEXP"],["skillavg"],
            ["runecrafting","runecraftingEXP"],["carpentry","carpentryEXP"]]
catacombs = [["catacombs","catacombsEXP"],["berserker","berserkerEXP"],["mage","mageEXP"],
                ["tank","tankEXP"],["healer","healerEXP"],["archer","archerEXP"]]

class Guild():
    def __init__(self):
        self.guildName = "Caped"
        self.minGEXP = 30000
        self.promoteGEXP = 50000
        self.ranks = []

        self.purgeMode = False
        self.fillingBank = False

        self.footerText = "Unclaimed is cool lol "
        self.footerImage = "https://crafatar.com/avatars/307005e7f5474f46b258c9a8b84276c4"

guild = Guild()

def getPlayerGuild(uuid):
    guildInfo = requests.get(f"https://api.hypixel.net/guild?key={api_key}&player={uuid}").json()
    return guildInfo
def getGuild():
    guildInfo = requests.get(f"https://api.hypixel.net/guild?key={api_key}&name={guild.guildName}").json()
    return guildInfo
def getPlayer(uuid):
    playerInfo = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()
    return playerInfo
def getUUID(playerName):
    playerBank = loadBank()
    for i in range(len(playerBank)):
        try:
            if playerBank["players"][i]["uuid"] == playerName:
                uuid = playerBank["players"][i]["uuid"]
                return uuid
        except:
            continue
    mojangInfo = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{playerName}").json()
    uuid = mojangInfo["id"]
    updateBank(uuid, playerName)
    return uuid  
def getMemberTime(joinDate):
    joinDate = datetime.fromtimestamp(joinDate)
    dateNow = datetime.now()
    memberTime = dateNow - joinDate
    return memberTime
def getPlayerName(uuid):
    playerBank = loadBank()
    
    for i in range(len(playerBank["players"])):
        if playerBank["players"][i]["uuid"] == uuid:
            playerName = playerBank["players"][i]["playerName"]
            return playerName
    
    playerInfo = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
    playerName = playerInfo["name"]
    return playerName
def getPlayerGEXP(guildInfo, uuid):
    for i in range(len(guildInfo["guild"]["members"])):
        if guildInfo["guild"]["members"][i]["uuid"] == uuid:
            weeklyGEXP = sum(guildInfo["guild"]["members"][i]["expHistory"].values())
    return weeklyGEXP
def getWeeklyGEXP():
    guildInfo = getGuild()
    totalXP = 0
    for i in range(len(guildInfo["guild"]["members"])):
        weeklyGEXP = guildInfo["guild"]["members"][i]["expHistory"]
        weeklyGEXP = sum(weeklyGEXP.values())
        totalXP += weeklyGEXP
    totalXP = "{:,}".format(totalXP)
    return totalXP
def loadBank():
    with open("playerBank.json") as playerBank:
        playerBank = json.load(playerBank)
        return playerBank
def loadReports():
    reports = open("offlineReports.json")
    reports = json.load(reports)
    return reports
def updateBank(uuid, playerName):
    playerBank = loadBank()
    for i in range(len(playerBank["players"])):
        if uuid == playerBank["players"][i]["uuid"]:
            return
    playerBank["players"].append({"uuid":uuid,"playerName":playerName})
    with open("playerBank.json","w") as newFile:
        json.dump(playerBank, newFile)
    print(f"Successfully added {playerName} to database (UUID {uuid})")
    return
def validPlayer(player):
    try:
        requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()
    except:
        return False
    return True
def hasReport(playerName):
    offlineReports = json.load(open("offlineReports.json","r"))
    for x in range(len(offlineReports)):
        nameLower = offlineReports[x]["nameLower"]
        if playerName.lower() == nameLower:
            return True
    return False
def getStatus(uuid):

    guildInfo = getGuild()
    for i in range(len(guildInfo["guild"]["members"])):
        if guildInfo["guild"]["members"][i]["uuid"] == uuid:
            memberRank = guildInfo["guild"]["members"][i]["rank"]
            joinDate = guildInfo["guild"]["members"][i]["joined"] / 1000
            memberTime = getMemberTime(joinDate)
            weeklyGEXP = sum(guildInfo["guild"]["members"][i]["expHistory"].values())

    if inCaped(uuid) == True:
        if memberRank == "Guild Master" or memberRank == "Admin" or memberRank == "Moderator":
            status = "Safe"
        elif memberRank == "Member":
            if memberTime.days <= 7:
                status = "New"
            else:
                if weeklyGEXP >= guild.promoteGEXP:
                    status = "Promote"
                else:
                    status = "Kick"
        elif memberRank == "Junior" or memberRank == "Senior":
            if weeklyGEXP <= guild.minGEXP:
                status = "Demote"
            else:
                status = "Safe"
        elif memberRank == "Junior" and weeklyGEXP >= guild.promoteGEXP and memberTime.days >= 30:
            status = "Promote"
    else:
        status = "Not in Caped"

    return status
def inCaped(uuid):
    guildInfo = getPlayerGuild(uuid)
    try:
        if guildInfo["guild"]["name"] == "Caped":
            return True
    except:
        return False
    return False
def getSkin(uuid):
    skin = f"https://crafatar.com/renders/body/{uuid}"
    return skin
def offlineTime(lastLogout, lastLogin, dateNow):
    if lastLogout <= lastLogin:
        lastOnline = "Online"
    else:
        lastOnlineDate = dateNow - lastLogout
        if lastOnlineDate.days < 1:
            lastOnline = f"{int(lastOnlineDate.seconds / 60)} minutes ago"
            if int(lastOnlineDate.seconds / 60) > 60:
                lastOnline = f"{int(lastOnlineDate.seconds / 60 /60)} hours ago"
        else:
            lastOnline = f"{lastOnlineDate.days} days ago"
    return lastOnline
def loadSkillBank():
    with open("storage.json","r") as skillBank:
        skillBank = json.load(skillBank)
        return(skillBank)
def calcSkillLevel(xp):
    if xp >= 55172425:
        return 50
    level = 0
    for i in skillProgression:
        if xp >= i:
            level += 1
        else:
            return level
def calcDungeonLevel(xp):
    if xp >= 569809640:
        return 50
    level = 0
    for i in dungeonProgression:
        if xp >= i:
            level += 1
        else:
            return level 
def calcRunecraftingLevel(xp):
    if xp >= 75400:
        return 25
    level = 0
    for i in runecraftingProgression:
        if xp >= i:
            level += 1
        else:
            return level 
def calcSkillAVG(playerName):
    skillBank = loadSkillBank()
    skillLevelList = []
    for i in range(len(skillBank["players"])):
        if skillBank["players"][i]["playerName"].lower() == playerName.lower():
            for j in range(len(skills) - 3):
                skillLevel = calcSkillLevel(skillBank["players"][i]["skills"][skills[j][1]])
                skillLevelList.append(skillLevel)
            skillAVG = round((sum(skillLevelList)) / (len(skills) - 3),1)
            return skillAVG
def noUnderScores(word):
    word = word.replace("_","\_")
    return word




@bot.event
async def on_ready():
    print("Bot is online!")

@bot.command()
async def nerd(message):
    user = message.author.mention
    messages = [f"{user} is a freaking nerd!",f"Hello, {user}",f"lol {user} is dumb",f"{user} no u.",f"UwU {user} *nuzzle*"]
    msg = random.choice(messages)
    await message.send(msg)

@bot.command()
async def info(message):
    msg = discord.Embed(title="Info",color=discord.Color.dark_red())
    msg.add_field(name="__Configuration:__",value=f"**Guild Name:** `{guild.guildName}`\n**Safe GEXP:** `{guild.minGEXP:,}+`\n**Promote GEXP:** `{guild.promoteGEXP:,}+`\n**Purge Mode:** `{guild.purgeMode}`")

    await message.send(embed=msg)

@bot.command()
async def totalxp(message):
    gexp = getWeeklyGEXP()
    await message.send(f"Total WeeklyGEXP: {gexp}")

@bot.command()
async def kicks(message):

    await message.send(embed=discord.Embed(colour = discord.Color.dark_red(),title=f"Getting kicks for {guild.guildName}..."))

    kickList = []
    names = ""
    names2 = ""
    long = False

    guildInfo = getGuild()

    for i in range(len(guildInfo["guild"]["members"])):
        memberRank = guildInfo["guild"]["members"][i]["rank"]
        joinDate = guildInfo["guild"]["members"][i]["joined"] / 1000
        weeklyGEXP = guildInfo["guild"]["members"][i]["expHistory"]
        uuid = guildInfo["guild"]["members"][i]["uuid"]

        memberTime = getMemberTime(joinDate)
        weeklyGEXP = getPlayerGEXP(guildInfo, uuid)

        if memberRank == "Member":
            if memberTime.days >= 7:
                if weeklyGEXP < guild.minGEXP:
                    playerName = getPlayerName(uuid)
                    if hasReport(playerName) == False:
                        kickList.append(playerName)
                        if len(names) <= 900:
                            names += f"\n - `{playerName}`"
                        else:
                            long = True
                            names2 += f"\n - `{playerName}`"

    msg = discord.Embed(title="__Kicks__ ",
        colour = discord.Color.dark_red()
    )

    if len(kickList) == 0:
        msg.add_field(name=f"__Players__: {len(kickList)}", value="There are no players\n eligible for Kicks!\n All caught up!")
        msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)

    else:
        msg.add_field(name=f"__Players__: {len(kickList)}", value=names)
        if long == True:
            msg2 = discord.Embed(
                colour = discord.Color.dark_red()
            )
            msg2.add_field(name=f"__More__", value=names2)
            msg2.set_footer(text=guild.footerText, icon_url=guild.footerImage)
        else:
            msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)

    await message.send(embed=msg)
    if long == True:
        await message.send(embed=msg2)
    
    if guild.purgeMode == True:
        purgeList = "**Purge List**\n`"
        for i in kickList:
            purgeList += f"{i} "
        purgeList += "`"
        await message.send(purgeList)

@bot.command()
async def demotes(message):
    await message.send(embed=discord.Embed(colour = discord.Color.dark_red(),title=f"Getting Demotes for {guild.guildName}..."))

    demoteList = []
    names = ""
    names2 = ""
    long = False
    guildInfo = getGuild()

    for i in range(len(guildInfo["guild"]["members"])):
        playerRank = guildInfo["guild"]["members"][i]["rank"]
        weeklyGEXP = guildInfo["guild"]["members"][i]["expHistory"]
        uuid = guildInfo["guild"]["members"][i]["uuid"]

        weeklyGEXP = sum(weeklyGEXP.values())

        if playerRank == "Junior" or playerRank == "Senior":
            if weeklyGEXP <= guild.minGEXP:
                playerName = getPlayerName(uuid)
                if hasReport(playerName) == False:
                    demoteList.append(playerName)
                    if len(names) <= 900:
                        if playerRank == "Junior":
                            names += f"\n - `{playerName}` \t\t[Junior] -> [Member]"
                        elif playerRank == "Senior":
                            names += f"\n - `{playerName}` \t\t[Senior] -> [Junior]"
                    else:
                        long = True
                        if playerRank == "Junior":
                            names2 += f"\n - `{playerName}` \t\t[Junior] -> [Member]"
                        elif playerRank == "Senior":
                            names2 += f"\n - `{playerName}` \t\t[Senior] -> [Junior]"

    msg = discord.Embed(title="__Demotes__ ",
        colour = discord.Color.dark_red()
    )

    if len(demoteList) == 0:
        msg.add_field(name=f"__Players__: {len(demoteList)}", value="There are no players\n eligible for demotions!\n All caught up!")
        msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)

    else:
        msg.add_field(name=f"__Players__: {len(demoteList)}", value=names)
        if long == True:
            msg2 = discord.Embed(
                colour = discord.Color.dark_red()
            )
            msg2.add_field(name=f"__More__", value=names2)
            msg2.set_footer(text=guild.footerText, icon_url=guild.footerImage)
        else:
            msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)

    await message.send(embed=msg)
    if long == True:
        await message.send(embed=msg2)

    if guild.purgeMode == True:
        purgeList = "**Purge List**\n`"
        for i in demoteList:
            purgeList += f"{i} "
        purgeList += "`"
        await message.send(purgeList)

@bot.command()
async def promotes(message):
    await message.send(embed=discord.Embed(title="Getting promotes for Caped..."))
    count = 0
    guildInfo = getGuild()
    promoteList = []
    p = ""
    for i in range(len(guildInfo["guild"]["members"])):
        uuid = guildInfo["guild"]["members"][i]["uuid"]
        weeklyGEXP = getPlayerGEXP(guildInfo, uuid)
        memberRank = guildInfo["guild"]["members"][i]["rank"]
        joinDate = guildInfo["guild"]["members"][i]["joined"] / 1000
        if memberRank == "Member" or memberRank == "Junior":
            if weeklyGEXP > guild.promoteGEXP:
                if memberRank == "Member" and getMemberTime(joinDate).days >= 7:
                    playerName = getPlayerName(uuid)
                    promoteList.append(playerName)
                    count += 1
                    p += f"`{playerName}` [Member] -> [Junior]\n"
                if memberRank == "Junior" and getMemberTime(joinDate).days >= 30:
                    playerName = getPlayerName(uuid)
                    promoteList.append(playerName)
                    count += 1
                    p += f"`{playerName}` [Junior] -> [Senior]\n"
    if len(promoteList) == 0:
        p = "There are no players\n eligible for promotions!\n All caught up!"
    msg = discord.Embed(title="__**Promotes**__",colour = discord.Color.dark_red())
    msg.add_field(name=f"__Players:__ {count}",value=p)
    msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)

    await message.send(embed=msg)
    if guild.purgeMode == True:
        purgeList = "**Purge List**\n`"
        for i in promoteList:
            purgeList += f"{i} "
        purgeList += "`"
        await message.send(purgeList)

@bot.command()
async def offline(message, playerName, duration, *, reason):
    if validPlayer(playerName) == False:
        await message.send(embed=discord.Embed(title=f"{playerName} is not a real player!",colour = discord.Color.dark_red()))
        return 
    try:
        float(duration)
    except:
        error = discord.Embed(title=f"__Error__",colour = discord.Color.dark_red())
        error.add_field(name="Enter a valid time!",value="For example:\n `*offline UnclaimedBloom6 10 School`")
        await message.send(embed=error)
        return
    uuid = getUUID(playerName)
    if inCaped(uuid) == False:
        await message.send(embed=discord.Embed(title=f"{playerName} is not in Caped!",colour = discord.Color.dark_red()))
        return
    msg = discord.Embed(title=f"__Offline Report__",colour = discord.Color.dark_red())
    msg.add_field(name="__IGN__",value=f"`{playerName}`",inline=False)
    msg.add_field(name="__Duration__",value=f"`{duration} days`",inline=False)
    msg.add_field(name="__Reason__",value=f"`{reason}`",inline=False)

    offlineReports = json.load(open("offlineReports.json","r"))

    leaveDate = datetime.now().strftime("%d/%m/%Y")
    dateBack = datetime.now() + timedelta(days=int(duration))
    dateBack = dateBack.strftime("%d/%m/%Y")
    nameLower = playerName.lower()

    newReport = {"playerName":playerName,"nameLower":nameLower,"leaveDate":leaveDate,"duration":duration,"dateBack":dateBack,"reason":reason}
    offlineReports.append(newReport)

    updatedReports = open("offlineReports.json","w")
    json.dump(offlineReports, updatedReports)

    await message.send(embed=msg)

@bot.command()
async def removeReport(message, playerName):
    offlineReports = json.load(open("offlineReports.json","r"))
    if hasReport(playerName) == True:
        for i in range(len(offlineReports)):
            if offlineReports[i]["playerName"] == playerName:
                with open("offlineReports.json","w") as newReports:
                    del offlineReports[i]
                    json.dump(offlineReports, newReports)
                    await message.send(embed=discord.Embed(title=f"Successfully removed {playerName} from offline reports."))
                    return
    else:
        await message.send(embed=discord.Embed(title=f"{playerName} Does not have an active offline report!"))
        return

@bot.command(aliases=["m","mem"])
async def member(message, *, playerName):
    await message.send(embed=discord.Embed(title=f"Getting guild stats for {noUnderScores(playerName)}...",color=discord.Color.dark_red()))
    if validPlayer(playerName) == False:
        await message.send(embed=discord.Embed(title=f"Error: {noUnderScores(playerName)} is not a real player",color=discord.Color.dark_red()))
        return
    uuid = getUUID(playerName)
    guildInfo = getPlayerGuild(uuid)
    try:
        guildName = guildInfo["guild"]["name"]
    except:
        await message.send(embed=discord.Embed(title=f"Error: {noUnderScores(playerName)} is not in a guild!",color=discord.Color.dark_red()))
        return
    for i in range(len(guildInfo["guild"]["members"])):

        if guildInfo["guild"]["members"][i]["uuid"] == uuid:
            
            weeklyGEXPall = guildInfo["guild"]["members"][i]["expHistory"]
            weeklyGEXP = getPlayerGEXP(guildInfo, uuid)

            playerRank = guildInfo["guild"]["members"][i]["rank"]
            status = getStatus(uuid)
            joinDate = guildInfo["guild"]["members"][i]["joined"] / 1000
            memberTime = getMemberTime(joinDate)
            joinDate = datetime.fromtimestamp(joinDate)
            dailyGEXP = ""
            for x in weeklyGEXPall:
                day = guildInfo["guild"]["members"][i]["expHistory"][x]
                dailyGEXP += "**{}**: `{:,}`\n".format(x, day)
                
    msg = discord.Embed(
        title=f"__{noUnderScores(playerName)} [{guildName}]__",
        colour = discord.Color.dark_red()
    )
    msg.set_thumbnail(url="https://crafatar.com/avatars/" + str(uuid))
    msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)

    msg.add_field(name="__Joined__", value="`" + str(joinDate.strftime("%d %b %Y")) +  f"\n({memberTime.days} days ago)`")
    msg.add_field(name=f"__Rank__", value=f"`[{playerRank}]`")
    msg.add_field(name=f"__Weekly GEXP__", value="`{:,}`".format(weeklyGEXP))
    msg.add_field(name=f"__GEXP By Day__", value=f"{dailyGEXP}", inline=True)
    msg.add_field(name=f"Status:", value=f"`{status}`", inline=True)

    await message.send(embed=msg)

@bot.command(aliases=["p"])
async def player(message, *, player):
    await message.send(f"Looking up info for {player}...")
    try:
        mojangInfo = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()
    except:
        await message.send(f"Error: {player} is not a real player")
        return
    uuid = mojangInfo["id"]

    mojangInfo = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
    playerName = mojangInfo["name"]

    guildInfo = requests.get(f"https://api.hypixel.net/guild?key={api_key}&player={uuid}").json()
    try:
        guildTag = "[" + str(guildInfo["guild"]["tag"]) + "]"
    except:
        guildTag = ""
    try:
        guildName = guildInfo["guild"]["name"]
        guildURL = f"https://plancke.io/hypixel/guild/player/{playerName}"
    except:
        guildName = "`Not in\na Guild!`"
        guildURL = ""

    playerInfo = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()

    lastLogin = datetime.fromtimestamp(playerInfo["player"]["lastLogin"] / 1000)
    lastLogout = datetime.fromtimestamp(playerInfo["player"]["lastLogout"] / 1000)
    dateNow = datetime.now()
    
    previousNames = playerInfo["player"]["knownAliases"]
    previousNames.reverse()
    knownAliases = ""
    for i in previousNames:
        knownAliases += f"` - {i}`\n"

    playerKarma = "{:,}".format(playerInfo["player"]["karma"])
    playerAP = "{:,}".format(playerInfo["player"]["achievementPoints"])
    playerXP = playerInfo["player"]["networkExp"]
    playerLevel = math.floor((math.sqrt((2 * playerXP) + 30625) / 50) - 2.5)

    fancy = discord.Embed(
        title = f"__{playerName}__ {guildTag}",
        colour = discord.Color.dark_red()
    )
    fancy.set_image(url="")
    fancy.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}")
    fancy.add_field(name="__Level__", value=f"`{playerLevel}`")
    fancy.add_field(name="__Karma__", value=f"`{playerKarma}`")
    fancy.add_field(name="__AP__", value=f"`{playerAP}`")
    fancy.add_field(name="__Previous Names:__", value=f"{knownAliases}", inline=True)
    fancy.add_field(name="__Last Online__", value=f"`{offlineTime(lastLogout, lastLogin, dateNow)}`")
    fancy.add_field(name="__Guild__", value=f"[{guildName}]({guildURL})")
    
    fancy.set_footer(text=guild.footerText, icon_url=guild.footerImage)

    await message.send(embed=fancy)

@bot.command()
async def purge(message):
    if guild.purgeMode == True:
        guild.purgeMode = False
        await message.send(embed=discord.Embed(title="Set purge mode to False"))
    else:
        guild.purgeMode = True
        await message.send(embed=discord.Embed(title="Set purge mode to True"))

@bot.command()
async def fillBank(message):
    await message.send(embed=discord.Embed(title="Filling bank with names of guild members...",color=discord.Color.dark_red()))
    playerBank = loadBank()
    beforeLength = len(playerBank["players"])
    guildInfo = getGuild()
    for i in range(len(guildInfo["guild"]["members"])):
        uuid = guildInfo["guild"]["members"][i]["uuid"]
        playerName = getPlayerName(uuid)
        updateBank(uuid, playerName)
    afterLength = len(playerBank["players"])
    a =  afterLength - beforeLength
    await message.send(f"Finished updating the bank! Added {a} entries!")

@bot.command()
async def reports(message):
    count = 0
    offlineReports = loadReports()
    r = discord.Embed(title="__**Offline Reports**__",color=discord.Color.dark_red())
    if len(offlineReports) == 0:
        await message.send(embed=discord.Embed(title="There are no offline reports!",color=discord.Color.dark_red()))
        return
    for i in range(len(offlineReports)):
        count += 1
        playerName = offlineReports[i]["playerName"]
        playerName = playerName.replace("_","\_")
        start = offlineReports[i]["leaveDate"]
        duration = offlineReports[i]["duration"]
        end = offlineReports[i]["dateBack"]
        reason = offlineReports[i]["reason"]

        r.add_field(name=f"#{count} __**{playerName}**__",value=f"Start: `{start}`\nDuration: `{duration} days`\nEnd: `{end}`\nReason: `{reason}`")

    await message.send(embed=r)
    
@bot.command()
async def bully(message, user):
    bullyMessages = [f"lol {user} smells!", f"{user} has the stupid dumb head disease", 
                    f"{user} has the unsmart", f"does {user} hav r retarded?",
                    f"{user} is so ugly, they scared the crap out of the toilet",
                    f"If I had a face like {user}, I'd sue my parents.",
                    f"{user} your birth certificate is an apology letter from the condom factory."]
    await message.send(random.choice(bullyMessages))

@bot.command()
async def skin(message, *, player):
    await message.send(embed=discord.Embed(title=f"Getting skin for {player}...",color=discord.Color.dark_red()))
    print(f"{player}")
    if validPlayer(player) == False:
        await message.send(embed=discord.Embed(title=f"{player} is not a real player!",color=discord.Color.dark_red()))
        return
    uuid = getUUID(player)
    msg = discord.Embed(title=f"{player}'s Skin:",color=discord.Color.dark_red())
    msg.set_image(url=getSkin(uuid))
    await message.send(embed=msg)

@bot.command(aliases=["lb"])
async def leaderboard(message, *, skill):
    msg = discord.Embed(title="Caped Skills Leaderboard",color=discord.Color.dark_red())
    stuff = ""
    typeSkill = False
    typeCatacombs = False
    skillsPosition = 0
    tempList = []
    skill = skill.lower()
    skillBank = loadSkillBank()
    for i in range(len(skills)):
        if skills[i][0] == skill:
            typeSkill = True
            skillsPosition = i
            break
    for i in range(len(catacombs)):
        if catacombs[i][0] == skill:
            typeCatacombs = True
            skillsPosition = i
            break
    if typeSkill == True or typeCatacombs == True:
        for i in range(len(skillBank["players"])):
            if skill == "skillavg":
                skillLevelList = []
                for j in range(len(skills) -3):
                    dictName = skills[j][1]
                    skillLevel = calcSkillLevel(skillBank["players"][i]["skills"][dictName])
                    skillLevelList.append(skillLevel)
                skillLevel = round((sum(skillLevelList)) / (len(skills) - 3),1)

            elif typeSkill == True:
                dictName = skills[skillsPosition][1]
                skillXP = skillBank["players"][i]["skills"][dictName]
                if skill == "runecrafting":
                    skillLevel = calcRunecraftingLevel(skillXP)
                else:
                    skillLevel = calcSkillLevel(skillXP)
            elif typeCatacombs == True:
                dictName = catacombs[skillsPosition][1]
                skillXP = skillBank["players"][i]["skills"]["catacombs"][dictName]
                skillLevel = calcDungeonLevel(skillXP)

            playerName = skillBank["players"][i]["playerName"]
            playerName = playerName.replace("_","\_")
            if skill == "skillavg":
                tempList.append([playerName,skillLevel])
            else:
                tempList.append([playerName,skillXP,skillLevel])

        tempList.sort(key = lambda x: x[1],reverse=True)
        skillName = skill.capitalize()
        if skill == "skillavg":
            skillName = "Skill Average"
            for i in range(10):
                stuff += f"**#{i + 1}** {tempList[i][0]} - {tempList[i][1]}\n"
        else:
            for i in range(10):
                stuff += f"**#{i + 1}** {tempList[i][0]} - {tempList[i][1]:,} ({tempList[i][2]})\n"
        msg.add_field(name=f"__{skillName} Leaderboard__",value=f"{stuff}")
        msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)
        await message.send(embed=msg)

    else:
        await message.send(embed=discord.Embed(title="That is not a skill!"))

@bot.command()
async def rank(message, *, player):
    try:
        uuid = getUUID(player)
    except:
        await message.send(embed=discord.Embed(title=f"{player} is not a real player!",color=discord.Color.dark_red()))
        return
    skillBank = loadSkillBank()
    playerRankings = []
    rankings = ""
    try:
        for i in range(len(skillBank["players"])):
            if skillBank["players"][i]["playerName"].lower() == player.lower():
                player = skillBank["players"][i]["playerName"]
                for j in skills:
                    skillStuff = []
                    for i in range(len(skillBank["players"])):
                        playerName = skillBank["players"][i]["playerName"].lower()
                        if j[0] == "skillavg":
                            skillLevel = calcSkillAVG(playerName)
                            skillStuff.append([playerName,skillLevel,skillLevel])
                        else:
                            skillXP = skillBank["players"][i]["skills"][j[1]]
                            if j[0] == "runecrafting":
                                skillLevel = calcRunecraftingLevel(skillXP)
                            else:
                                skillLevel = calcSkillLevel(skillXP)
                            skillStuff.append([playerName,skillXP,skillLevel])
                    skillStuff.sort(key = lambda x: x[1],reverse=True)
                    for x in range(len(skillStuff)):
                        if skillStuff[x][0] == player.lower():
                            rankings += f"{j[0].capitalize()}: `#{x+1} ({skillStuff[x][2]})`\n"
        msg = discord.Embed(title=f"Caped Skill Rankings",color=discord.Color.dark_red())
        msg.add_field(name=f"__Placings for {noUnderScores(player)}__",value=f"{rankings}")
        msg.set_footer(text=guild.footerText, icon_url=guild.footerImage)
        await message.send(embed=msg)
    except:
        if inCaped(uuid) == True:
            await message.send(embed=discord.Embed(title=f"{player} doesn't play SkyBlock or doesn't have their API enabled!",color=discord.Color.dark_red()))
        else:
            await message.send(embed=discord.Embed(title=f"{player} is not in Caped!",color=discord.Color.dark_red()))
        




bot.run("NzQwNDgxNzgyOTMwOTk3MjU4.XyppZg.1BWGr-ZkE_0me4KcLOjuY-VhZcw")