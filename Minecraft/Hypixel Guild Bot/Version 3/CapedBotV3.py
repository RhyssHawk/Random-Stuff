# Version 3 of the bot
#
# Main improvements:
#   - Cleaner Code
#   - Custom help command
#   - More optimization
#   - Better future-proofing

# Commands:
#   - help <command>                (Misc)
#   - config                        (Misc)
#   - purge                         (Guild)
#   - member <player>               (Guild)
#   - promotes                      (Guild)
#   - kicks                         (Guild)
#   - demotes                       (Guild)
#   - leaderboard <category>        (Skyblock)
#   - rank <player>                 (Skyblock)
#   - dungeons <player>             (Skyblock)

import HypixelUtils as hy
import MinecraftUtils as mc
import requests
import json
from datetime import datetime
import discord
from discord.ext import commands

# Import the settings from a json file and create global variables for them
# Run the bot after all of the settings have been set and there are
# no issues with them, eg missing Token, API key etc.
def setupConfig():
    global token, key, botPrefix, guildName, minimumGEXP, promoteGEXP, purgeMode, footerText, footerImage, botColor
    # Open and load the bot token
    try:
        with open("TOKEN","r") as bot_token:
            token = bot_token.read()
    except:
        print("\nERROR: No bot token file.\nMake a new file called \"TOKEN\" with the bot's Discord Token inside!\n")
        return

    # Open and load the API key for Hypixel
    try:
        with open("apiKey","r") as keyFile:
            key = keyFile.read()
    except:
        print("\nERROR: Hypixel API key not set!\nMake a new file called \"apiKey\" with the API Key inside!")
        return

    # Import variables from the config .json file.
    # 
    try:
        with open("botConfig.json","r") as config:
            config = json.load(config)

            botPrefix = config["botPrefix"]
            guildName = config["guildName"]
            minimumGEXP = config["minimumGEXP"]
            promoteGEXP = config["promoteGEXP"]
            purgeMode = config["purgeMode"]
            footerText = config["footerText"]
            footerImage = config["footerImage"]
            botColor = discord.Color.dark_red()
    except:
        print("No config file exists. Creating one with default values.")
        config = ""
        defaultConfig = json.load(open("defaultConfig.json","r"))
        json.dump(defaultConfig, open("botConfig.json","w"))
        setupConfig()

setupConfig()

# Make the bot with the bot Prefix set above ^
bot = commands.Bot(command_prefix=botPrefix, help_command=None)

# Bunch of functions used in the commands

# Get the guild status of a player (Promote, Demote, Kick, Safe etc)
def getStatus(guildInfo, uuid):
    for i in range(len(guildInfo["guild"]["members"])):
        if guildInfo["guild"]["members"][i]["uuid"] == uuid:
            memberRank = guildInfo["guild"]["members"][i]["rank"]
            joinDate = guildInfo["guild"]["members"][i]["joined"] / 1000
            memberTime = datetime.now() - datetime.fromtimestamp(joinDate)
            weeklyGEXP = sum(guildInfo["guild"]["members"][i]["expHistory"].values())

            if memberRank == "Guild Master" or memberRank == "Admin" or memberRank == "Moderator":
                status = "Safe (Staff)"
            elif memberRank == "Member":
                if memberTime.days <= 6:
                    status = "New"
                else:
                    if weeklyGEXP >= promoteGEXP:
                        status = "Promote"
                    else:
                        status = "Kick"
            elif memberRank == "Junior" or memberRank == "Senior":
                if weeklyGEXP <= minimumGEXP:
                    status = "Demote"
                elif memberRank == "Junior" and weeklyGEXP >= promoteGEXP and memberTime.days >= 30:
                    status = "Promote"
                else:
                    status = "Safe"
            

    return status
# Make a purge list out of a list of names (player1 player2 player3)
def makePurgeList(playerList):
    purgeList = "`"
    for i in playerList:
        purgeList += f"{i} "
    purgeList += "`"
    return purgeList
# Get a player's username via uuid by first looking through the PlayerInfo.json file, and then
# using the Mojang API afterwards if it is not found
def getPlayerName(uuid):
    try:
        with open("playerInfo.json","r") as playerInfo:
            playerInfo = json.load(playerInfo)
            for i in range(len(playerInfo["players"])):
                if playerInfo["players"][i]["uuid"] == uuid:
                    playerName = playerInfo["players"][i]["playerName"]
                    return playerName
    except:
        playerName = mc.getPlayerName(uuid)
        return playerName
# Load playerInfo.json and return its contents as a json object
def loadPlayers():
    with open("playerInfo.json","r") as playerInfo:
        playerInfo = json.load(playerInfo)
    return playerInfo


# Say when the bot comes online
@bot.event
async def on_ready():
    print("Bot is Online!")

@bot.command()
async def help(ctx):
    guildStuff = [
        "member <player>` - Shows information about a player in any guild",
        "promotes` - Shows players who should be promoted in the guild",
        "demotes` - Shows players who should be demoted in the guild",
        "kicks` - Shows players who should be kicked in the guild",
        "purge` - Print a list of names after promotes, demotes and kicks"
    ]
    sbStuff = [
        "leaderboard` <category> - Show the top 10 players in the guild for a Skyblock category",
        "rank <player>` - Show the ranks of a player in all recorded categories",
        "dungeons <player>` - Show dungeon stats of a player"
    ]
    msg = discord.Embed(title="Commands:",color=botColor)
    a = ""
    b = ""
    for i in guildStuff:
        a += f"`{botPrefix}{i}\n"
    for i in sbStuff:
        b += f"`{botPrefix}{i}\n"
    msg.add_field(name="Guild Stuff",value=a,inline=False)
    msg.add_field(name="Skyblock Stuff",value=b,inline=False)

    await ctx.send(embed=msg)

#Print the settings of the bot into a channel
@bot.command()
async def config(ctx):
    msg = discord.Embed(title="__Bot Config__",color=botColor)
    msg.add_field(name="**Settings**",value=f"**Bot Prefix:** `{botPrefix}`\n**Guild Name:** `{guildName}`\n**Minimum GEXP:** `{minimumGEXP:,}`\n**Promote GEXP:** `{promoteGEXP:,}`\n**Purge Mode:** `{purgeMode}`\n**Footer Text:** `{footerText}`\n**Footer Image:** `{footerImage}`")

    await ctx.send(embed=msg)

#Toggle the purge mode (Sending names after Promotes, Demotes, Kicks)
@bot.command()
async def purge(ctx):
    #If purgemode is already true then toggle it off
    if purgeMode == True:
        with open("botConfig.json","r") as oldSettings:
            oldSettings = json.load(oldSettings)
            oldSettings["purgeMode"] = False
    else:
        #If it's disabled then set it to true
        with open("botConfig.json","r") as oldSettings:
            oldSettings = json.load(oldSettings)
            oldSettings["purgeMode"] = True
    #Update the new settings in the config file
    with open("botConfig.json","w") as newSettings:
        json.dump(oldSettings, newSettings)
    setupConfig()
    #Tell the user that purgemode has been toggled
    await ctx.send(embed=discord.Embed(title=f"Set new purge mode to {purgeMode}",color=botColor))

#Show detailed guild info about a player
@bot.command(aliases=["mem","m"])
async def member(ctx, *, player):
    await ctx.send(embed=discord.Embed(title=f"Getting guild stats for {player}...",color=botColor))
    #Check if it's a valid player. Returns False if not, returns ["playerName","uuid"] if yes.
    validPlayer = mc.validPlayer(player)
    #If it's not a valid player then send an error message and exit the function
    if validPlayer == False:
        await ctx.send(embed=discord.Embed(title=f"Error: {player} is not a real player!",color=botColor))
        return
    #Otherwise if it's a real player continue
    else:
        #Info from the API
        playerName = validPlayer[0]
        uuid = validPlayer[1]
        #Show that the bot is processing
        #Get guild info via the player's UUID
        guildInfo = hy.getGuildPlayerInfo(key, uuid)
        #Check if the player is actually in a guild
        try:
            guildName = guildInfo["guild"]["name"]
            guildTag = guildInfo["guild"]["tag"]
        #If they're not then send an error message and exit the function
        except:
            await ctx.send(embed=discord.Embed(title=f"Error: {mc.noFormatUnderScores(playerName)} is not in a guild!",color=botColor))
            return
        #Go through every player in the guild to find the right player
        for i in range(len(guildInfo["guild"]["members"])):
            #If matches...
            if guildInfo["guild"]["members"][i]["uuid"] == uuid:
                #Check if the player is in Caped
                if guildName == "Caped":
                    #And get the status of that player (Promote, Demote, Kick...)
                    status = getStatus(guildInfo, uuid)
                else:
                    #If they're not in Caped then just continue
                    status = "Not in Caped"
                #Variables for printing later
                joinDate = guildInfo["guild"]["members"][i]["joined"] / 1000
                playerRank = guildInfo["guild"]["members"][i]["rank"]
                gexpHistory = guildInfo["guild"]["members"][i]["expHistory"]
                msg = discord.Embed(title=f"{playerName} [{guildTag}]",color=botColor)
                dailyGEXP = ""
                #Make a new line for each day of guild experience
                for day in gexpHistory:
                    xp = gexpHistory[day]
                    dailyGEXP += f"**{day}** `{xp:,}`\n"
                #Start constructing the embedded message to send
                msg.add_field(name="__Joined__", value="`" + str(datetime.fromtimestamp(joinDate).strftime("%d %b %Y")) +  f"\n({hy.getGuildMemberTime(joinDate).days} days ago)`")
                msg.add_field(name=f"__Rank__", value=f"`[{playerRank}]`")
                msg.add_field(name=f"__Status__", value=f"`{status}`")
                msg.add_field(name="__Daily GEXP__",value=dailyGEXP)
                msg.add_field(name="__Weekly GEXP__",value=f"`{sum(gexpHistory.values()):,}`")
                msg.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}")
                msg.set_footer(text=footerText, icon_url=footerImage)
                #Send the embedded message with the player's guild info
                await ctx.send(embed=msg)    

@bot.command()
async def promotes(ctx):
    await ctx.send(embed=discord.Embed(title=f"Getting promotes for {guildName}...",color=botColor))
    promoteList = []
    p = ""
    guildInfo = hy.getGuildNameInfo(key, guildName)
    for i in range(len(guildInfo["guild"]["members"])):
        uuid = guildInfo["guild"]["members"][i]["uuid"]
        status = getStatus(guildInfo, uuid)
        if status == "Promote":
            playerName = getPlayerName(uuid)
            if guildInfo["guild"]["members"][i]["rank"] == "Member":
                p += f"`{playerName} [Member] -> [Junior]`\n"
            elif guildInfo["guild"]["members"][i]["rank"] == "Junior":
                p += f"`{playerName} [Junior] -> [Senior]`\n"
            promoteList.append(playerName)
    if len(promoteList) == 0:
        p = "There are no players eligible\n for promotions.\nAll caught up!"
        
    msg = discord.Embed(title="__Promotes__",color=botColor)
    msg.add_field(name=f"Promotes: {len(promoteList)}",value=f"{p}")
    msg.set_footer(text=footerText, icon_url=footerImage)

    await ctx.send(embed=msg)

    if purgeMode == True:
        await ctx.send(f"__**Promotes Purge List**__ \n{makePurgeList(promoteList)}")

@bot.command()
async def kicks(ctx):
    await ctx.send(embed=discord.Embed(title=f"Getting kicks for {guildName}...",color=botColor))
    kickList = []
    p = ""
    p2 = ""
    long = False
    guildInfo = hy.getGuildNameInfo(key, guildName)
    for i in range(len(guildInfo["guild"]["members"])):
        uuid = guildInfo["guild"]["members"][i]["uuid"]
        status = getStatus(guildInfo, uuid)
        if len(p) >= 900:
            long = True
        if status == "Kick":
            playerName = getPlayerName(uuid)
            if long == False:
                p += f"`{playerName}`\n"
            else:
                p2 += f"`{playerName}`\n"
            kickList.append(playerName)

    if len(kickList) == 0:
        p = "There are no players eligible\n for a kick.\nAll caught up!"
        
    msg = discord.Embed(title="__Kicks__",color=botColor)
    msg.add_field(name=f"Kicks: {len(kickList)}",value=p,inline=False)
    #If it's a long message then add another field underneath with the overflow
    if long == True:
        msg.add_field(name=f"__More__ {len(kickList)}",value=p2,inline=False)
    msg.set_footer(text=footerText, icon_url=footerImage)

    await ctx.send(embed=msg)
    if purgeMode == True:
        await ctx.send(f"__**Kick Purge List**__ \n{makePurgeList(kickList)}")
        
@bot.command()
async def demotes(ctx):
    await ctx.send(embed=discord.Embed(title=f"Getting demotes for {guildName}...",color=botColor))
    demoteList = []
    p = ""
    p2 = ""
    long = False
    guildInfo = hy.getGuildNameInfo(key, guildName)
    for i in range(len(guildInfo["guild"]["members"])):
        uuid = guildInfo["guild"]["members"][i]["uuid"]
        status = getStatus(guildInfo, uuid)
        #If message is longer than is allowed by discord embed
        if len(p) >= 900:
            long = True
        if status == "Demote":
            playerName = getPlayerName(uuid)

            if guildInfo["guild"]["members"][i]["rank"] == "Junior":
                if long == False:
                    p += f"`{playerName}` [Junior] -> [Member]\n"
                else:
                    p2 += f"`{playerName}` [Junior] -> [Member]\n"
            elif guildInfo["guild"]["members"][i]["rank"] == "Senior":
                if long == False:
                    p += f"`{playerName}` [Senior] -> [Junior]\n"
                else:
                    p2 += f"`{playerName}` [Senior] -> [Junior]\n"

            demoteList.append(playerName)

    if len(demoteList) == 0:
        p = "There are no players eligible\n for demotions.\nAll caught up!"
        
    msg = discord.Embed(title="__Demotes__",color=botColor)
    msg.add_field(name=f"Demotes: {len(demoteList)}",value=p,inline=False)
    if long == True:
        msg.add_field(name="__More__",value=p2,inline=False)
    msg.set_footer(text=footerText, icon_url=footerImage)
    await ctx.send(embed=msg)
    if purgeMode == True:
        await ctx.send(f"__**Demote Purge List**__ \n{makePurgeList(demoteList)}")

@bot.command(aliases=["lb"])
async def leaderboard(ctx, *, skill):

    #Get list of players and content for leaderboard ready
    playerList = []
    lb = ""

    #Variables ready. Seperate skill and skillName to avoid conflicts with changing skillName manually eg Skill Average
    skill = skill.lower()
    skillName = skill.capitalize()
    dictName = skill + "XP"

    #Load the database with the nerds
    playerInfo = loadPlayers()
    #Cycle through every guild member in the database
    for i in range(len(playerInfo["players"])):
        #Keep going if they have Skyblock data
        if "skyblock" in playerInfo["players"][i]:
            #Shorten stuff to make life easier later on
            skills = playerInfo["players"][i]["skyblock"]["skills"]
            slayers = playerInfo["players"][i]["skyblock"]["slayer"]
            #Get player's name now so don't have to later
            playerName = playerInfo["players"][i]["playerName"]
            #Main skills leaderboard
            if dictName in skills["realSkills"]:
                skillXP = skills["realSkills"][dictName]
                if dictName == "enchantingXP" or dictName == "farmingXP" or dictName == "miningXP":
                    skillLevel = hy.calcSkillLevel60(skillXP)
                else:
                    skillLevel = hy.calcSkillLevel(skillXP)
                playerList.append([playerName, skillXP, skillLevel])
            #Cosmetic skills leaderboards
            elif dictName in skills["cosmeticSkills"]:
                skillXP = skills["cosmeticSkills"][dictName]
                #If runecrafting then calculate the level in a different way 
                if skill == "runecrafting":
                    skillLevel = hy.calcRunecraftingLevel(skillXP)
                #If not runecrafting then calculate the normal way
                else:
                    skillLevel = hy.calcSkillLevel(skillXP)
                playerList.append([playerName, skillXP, skillLevel])
            #Catacombs level or individual class level
            elif dictName in skills["dungeonSkills"]:
                skillXP = skills["dungeonSkills"][dictName]
                skillLevel = hy.calcDungeonLevel(skillXP)
                playerList.append([playerName, skillXP, skillLevel])
            #Individual slayer bosses leaderboard
            elif dictName in slayers:
                skillXP = slayers[dictName]
                skillLevel = hy.calcSlayerLevel(skill, skillXP)
                playerList.append([playerName, skillXP, skillLevel])
            #Total slayer leaderboard
            elif skill == "slayer":
                skillXP = sum(slayers.values())
                playerList.append([playerName, skillXP])
            #If the user wants skill average leaderboard
            elif skill == "skillavg":
                skillLevel = hy.calcSkillAverage(skills)
                playerList.append([playerName, skillLevel])
                skillName = "Skill Average"
            #If the skill isn't caught up here ^ then send an error message
            else:
                await ctx.send(embed=discord.Embed(title=f"Error: {skillName} is not a skill!",color=botColor))
                return
    #Sort the players in order from most skillXP to smallest (skillXP is second value in list so sort like that)
    playerList.sort(key = lambda x: x[1],reverse=True)

    #Add only the top 10 players to a string
    for i in range(10):
        #If there are only two variables (playerName and skillLevel usually)
        if len(playerList[1]) == 2:
            lb += f"**#{i+1}** {mc.noFormatUnderScores(playerList[i][0])} - `{playerList[i][1]:,}`\n"
        #If there are three variables (Usually playerName, skillXP and skillLevel)
        elif len(playerList[1]) == 3:
            lb += f"**#{i+1}** {mc.noFormatUnderScores(playerList[i][0])} - `{playerList[i][1]:,}` ({playerList[i][2]})\n"
        #If there are one, four or more then send this, but it's unlikely.
        else:
            await ctx.send(embed=discord.Embed(title="Lol something went pretty wrong",color=botColor))

    #Get the embedded message ready
    msg = discord.Embed(title=f"Caped Skills Leaderboard",color=botColor)
    msg.add_field(name=f"Top {skillName}",value=f"{lb}")
    msg.set_footer(text=footerText, icon_url=footerImage)
    #Send the embed message into the channel
    await ctx.send(embed=msg)

@bot.command()
async def rank(ctx, *, player):
    validPlayer = mc.validPlayer(player)
    #If not a real player then send an error message and exit
    if validPlayer== False:
        await ctx.send(embed=discord.Embed(title=f"{player} is not a real player!",color=discord.Color.dark_red()))
        return
    playerName = validPlayer[0]
    uuid = validPlayer[1]
    playerInfo = loadPlayers()
    #See if the player is in the database (In Caped with Skyblock API enabled)
    for i in range(len(playerInfo["players"])):
        if playerInfo["players"][i]["playerName"] == playerName:
            if "skyblock" in playerInfo["players"][i]:
                break
            else:
                missingAPIs = ""
                uuid = playerInfo["players"][i]["uuid"]
                sbProfile = hy.getRecentProfile(key, uuid)
                msg = discord.Embed(title=f"Error: {playerName} doesn't have all of their API enabled.",color=botColor)
                await ctx.send(embed=msg)
                return

    #If they're not then error message and exit
    else:
        await ctx.send(embed=discord.Embed(title=f"Error: {playerName} is not in Caped.",color=botColor))
        return

    mainSkills = ""
    dungeonSkills = ""
    slayerSkills = ""
    skillPlacements = []
    dungeonPlacements = []
    slayerPlacements = []

    for i in range(len(playerInfo["players"])):
        if "skyblock" in playerInfo["players"][i]:
            skillStuffList = {}
            skillTypes = playerInfo["players"][i]["skyblock"]["skills"].keys()
            for key in skillTypes:
                skillStuffList[key] = []
                skills = playerInfo["players"][i]["skyblock"]["skills"][key].keys()
                for x in skills:
                    skillStuffList[key].append(x)
            slayerBosses = playerInfo["players"][i]["skyblock"]["slayer"].keys()
            skillStuffList["slayer"] = ["totalXP"]
            for x in slayerBosses:
                skillStuffList["slayer"].append(x)
            break
    #For every skill type
    for skillType in skillStuffList:
        #For every skill in that skilltype
        for skill in skillStuffList[skillType]:
            skillLB = []
            skillName = skill.replace("XP", "")
            #Go through every single player
            for i in range(len(playerInfo["players"])):
                if "skyblock" in playerInfo["players"][i]:
                    player = playerInfo["players"][i]["playerName"]
                    #If the skill type is slayer
                    if skillType == "slayer":
                        #If total xp is called for then get the total XP
                        if skillName == "total":
                            skillXP = sum(playerInfo["players"][i]["skyblock"][skillType].values())
                            skillLevel = 0
                        #If individual bosses are called for then get those and calculate the levelo
                        else:
                            skillXP = playerInfo["players"][i]["skyblock"][skillType][skill]
                            skillLevel = hy.calcSlayerLevel(skillName, skillXP)
                    else:
                        skillXP = playerInfo["players"][i]["skyblock"]["skills"][skillType][skill]
                        #If runecrafting then calculate using its levelling table
                        if skill == "runecraftingXP":
                            skillLevel = hy.calcRunecraftingLevel(skillXP)
                        #If dungeons skill use dungeons levelling table
                        elif skillType == "dungeonSkills":
                            skillLevel = hy.calcDungeonLevel(skillXP)
                        #Normal skill use normal stuff
                        elif skill == "enchantingXP" or skill == "farmingXP" or skill == "miningXP":
                            skillLevel = hy.calcSkillLevel60(skillXP)
                        else:
                            skillLevel = hy.calcSkillLevel(skillXP)
                    skillLB.append([player, skillXP, skillLevel])
            #Sort in order from most to least XP
            skillLB.sort(key = lambda x: x[1],reverse=True)
            for i in range(len(skillLB)):
                if skillLB[i][0] == playerName:
                    #Add the players xp, skill level and placement to a list with their other placements
                    if skillType == "dungeonSkills":
                        dungeonPlacements.append([skillName.capitalize(), i+1, skillLB[i][1],skillLB[i][2]])
                    elif skillType == "slayer":
                        slayerPlacements.append([skillName.capitalize(), i+1, skillLB[i][1],skillLB[i][2]])
                    else:
                        skillPlacements.append([skillName.capitalize(), i+1, skillLB[i][1],skillLB[i][2]])

    #Sort by their best placements first
    skillPlacements.sort(key = lambda x: x[1])
    dungeonPlacements.sort(key = lambda x: x[1])
    #Add the general skills into a string to be sent later in the embed message
    for i in range(len(skillPlacements)):
        mainSkills += f"{skillPlacements[i][0]}: **#{skillPlacements[i][1]}** - `{skillPlacements[i][2]:,} xp` ({skillPlacements[i][3]})\n"
    #Add the dungeon skills to be added later on as well
    for i in range(len(dungeonPlacements)):
        dungeonSkills += f"{dungeonPlacements[i][0]}: **#{dungeonPlacements[i][1]}** - `{dungeonPlacements[i][2]:,} xp` ({dungeonPlacements[i][3]})\n"
    #Add slayer leaderboards to a string
    for i in range(len(slayerPlacements)):
        if slayerPlacements[i][0] == "Total":
            slayerSkills += f"{slayerPlacements[i][0]}: **#{slayerPlacements[i][1]}** - `{slayerPlacements[i][2]:,} xp`\n"
        else:
            slayerSkills += f"{slayerPlacements[i][0]}: **#{slayerPlacements[i][1]}** - `{slayerPlacements[i][2]:,} xp` ({slayerPlacements[i][3]})\n"

    msg = discord.Embed(title=f"{playerName}",color=botColor)
    msg.add_field(name=f"Skills",value=f"{mainSkills}",inline=True)
    msg.add_field(name=f"Catacombs",value=f"{dungeonSkills}",inline=True)
    msg.add_field(name=f"Slayer",value=f"{slayerSkills}",inline=False)
    msg.set_footer(text=footerText, icon_url=footerImage)
    await ctx.send(embed=msg)

def toTime(timestamp):
    if timestamp == 0:
        return "N/A"
    minutes = int(timestamp / 1000 / 60)
    timestamp -= minutes * 1000 * 60
    seconds = int(timestamp / 1000)
    if len(str(seconds)) == 1:
        seconds = str(seconds) + "0"
    return f"{minutes}:{seconds}"

@bot.command(aliases=["d"])
async def dungeons(ctx, *, player):
    #Show that the dumb bot is actually doing something
    await ctx.send(embed=discord.Embed(title=f"Getting dungeons stats for {player}...",color=botColor))
    #Verify that the player is a real player, if it it then store the username and uuid for later
    validPlayer = mc.validPlayer(player)
    if validPlayer == False:
        await ctx.send(embed=discord.Embed(title=f"Error: {player} is not a real player!",color=botColor))
        return
    else:
        playerName = validPlayer[0]
        uuid = validPlayer[1]
    
    #Skyblock profile for most recent profile (Main profile usually)
    sbProfile = hy.getRecentProfile(key, uuid)
    #Just to save the whole "sbProfile["members"][uuid] etc stuff. Quality of life thing.
    dungeonsStats = sbProfile["members"][uuid]["dungeons"]
    catacombsXP = int(dungeonsStats["dungeon_types"]["catacombs"]["experience"])
    catacombsLevel = round(hy.calcDungeonLevel(catacombsXP),2)
    
    selectedClass = dungeonsStats["selected_dungeon_class"]
    playerStats = hy.getPlayerInfo(key, uuid)
    try:
        secretsFound = playerStats["player"]["achievements"]["skyblock_treasure_hunter"]
    except:
        secretsFound = 0
    #Floor stats in the form of [Completions, Fastest Time(Normal), Fastest Time (S), Fastest Time(S+)]
    floorInfo = {}
    for i in range(8):
        floor = str(i)
        if "tier_completions" in dungeonsStats["dungeon_types"]["catacombs"]:
            if floor in dungeonsStats["dungeon_types"]["catacombs"]["tier_completions"]:
                timesCompleted = int(dungeonsStats["dungeon_types"]["catacombs"]["tier_completions"][floor])
            else:
                timesCompleted = "N/A"
        else:
            timesCompleted = "N/A"
        if "fastest_time" in dungeonsStats["dungeon_types"]["catacombs"]:
            if floor in dungeonsStats["dungeon_types"]["catacombs"]["fastest_time"]:
                fastestTime = int(dungeonsStats["dungeon_types"]["catacombs"]["fastest_time"][floor])
            else:
                fastestTime = 0
        else:
            fastestTime = 0
        if "fastest_time_s" in dungeonsStats["dungeon_types"]["catacombs"]:
            if floor in dungeonsStats["dungeon_types"]["catacombs"]["fastest_time_s"]:
                fastestTimeS = int(dungeonsStats["dungeon_types"]["catacombs"]["fastest_time_s"][floor])
            else:
                fastestTimeS = 0
        else:
            fastestTimeSPlus = 0
        if "fastest_time_s_plus" in dungeonsStats["dungeon_types"]["catacombs"]:
            if floor in dungeonsStats["dungeon_types"]["catacombs"]["fastest_time_s_plus"]:
                fastestTimeSPlus = int(dungeonsStats["dungeon_types"]["catacombs"]["fastest_time_s_plus"][floor])
            else:
                fastestTimeSPlus = 0
        else:
            fastestTimeSPlus = 0
        floorInfo[floor] = [timesCompleted, fastestTime, fastestTimeS, fastestTimeSPlus]

    #Make the embedded message to send 
    msg = discord.Embed(title=f"{playerName}'s Dungeon Stats",color=botColor)
    msg.add_field(name="Overall Stats",value=f"Catacombs Level: **{catacombsLevel}** `({catacombsXP:,} XP)`\nHighest Floor Completed: Floor 7\nSecrets Found: `{secretsFound:,}`\nSelected Class: `{selectedClass.capitalize()}`",inline=False)
    for i in range(len(floorInfo)):
        floor = str(i)
        fastestTime = toTime(floorInfo[floor][1])
        fastestTimeS = toTime(floorInfo[floor][2])
        fastestTimeSPlus = toTime(floorInfo[floor][3])
        msg.add_field(name=f"__Floor {floor}__",value=f"Completions: `{floorInfo[floor][0]}`\nFastest: `{fastestTime}`\nFastest S: `{fastestTimeS}`\nFastest S+: `{fastestTimeSPlus}`",inline=True)
    msg.set_footer(text=footerText, icon_url=footerImage)
    await ctx.send(embed=msg)


bot.run(token)