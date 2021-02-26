import discord
import requests
import math
from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix="*")
api_key = open("D:\Minecraft\Code Stuff\Discord Bot\API_KEY")
api_key = api_key.read()

guild = "Caped"
requiredGEXP = 50000

footerText = "Unclaimed is cool lol "
footerImage = "https://crafatar.com/avatars/307005e7f5474f46b258c9a8b84276c4"

@bot.event
async def on_ready():
    print("Bot is online!")

@bot.command()
async def commands(message):

    msg = "\n**"
    msg += "\n`*member <player>` - Guild stats of player"
    msg += "\n`*risk <player>` - See if a player is going to be kicked, demoted or promoted"
    msg += "\n`*promotes` - Shows list of players eligiable for promotions."
    msg += "\n`*demotes` - Shows a list of players eligible for demotes."
    msg += "\n`*kicks` - Shows a list of players eligable for kicks."
    msg += "\n**"

    fancy = discord.Embed(title="__Help List__")

    fancy.set_thumbnail(url="")

    fancy.set_footer(text=footerText, icon_url=footerImage)

    fancy.add_field(name="Commands:", value=msg)

    await message.send(embed=fancy)

@bot.command()
async def embed(message):
    emsg = discord.Embed(title="Even More Stuff")

    emsg.set_image(url="")
    emsg.set_thumbnail(url="")
    emsg.set_author(name="BIG Title!", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    emsg.set_footer(text="footer stuff", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    emsg.add_field(name="One", value="Stuff for one")
    emsg.add_field(name="Two", value="stuff for two")
    emsg.add_field(name="Three", value="stuff for three")
    emsg.add_field(name="Inline 1", value="Inline one lol", inline=True)
    emsg.add_field(name="Inline 2", value="Inline two nerd", inline=True)

    await message.send(embed=emsg)

@bot.command()
async def hello(message):

    msg = "Hello " + str(message.author.mention)
    await message.send(msg)

@bot.command()
async def risk(message, *, player):

    await message.send("Processing risk for " + str(player) + "...\n")
    try:
        mojangInfo = requests.get("https://api.mojang.com/users/profiles/minecraft/" + str(player)).json()
    except:
        print(player, "is not a real player")
        await message.send("Error: " + str(player) + " is not a real player")
        return
    uuid = mojangInfo["id"]

    guildInfo = requests.get("https://api.hypixel.net/guild?key=" + str(api_key) +"&player=" + str(uuid)).json()
    try:
        guildName = guildInfo["guild"]["name"]
    except:
        await message.send("Error: " + str(player) + " is not in a guild!")
        return

    if guildName != guild:
        await message.send("Error: " + str(player) + " is not in Caped.")
        return

    msg = "Risk for " + str(player) + ":\n"

    for i in range(len(guildInfo["guild"]["members"])):

        if guildInfo["guild"]["members"][i]["uuid"] == uuid:

            weeklyGEXP = guildInfo["guild"]["members"][i]["expHistory"]
            weeklyGEXP = sum(weeklyGEXP.values())

            playerRank = guildInfo["guild"]["members"][i]["rank"]

            joinDateRaw = guildInfo["guild"]["members"][i]["joined"] / 1000
            joinDate = datetime.fromtimestamp(joinDateRaw)

            dateNow = datetime.now()

            memberTime = dateNow - joinDate

    if playerRank == "Guild Master" or playerRank == "Admin" or playerRank == "Moderator":
        msg += str(player) + " is a staff member. No risk of being kicked or demoted."

    elif playerRank == "Member":
        if weeklyGEXP <= requiredGEXP:
            if memberTime.days < 7:
                msg += str(player) + " hasn't been in the guild for 7 days yet."
            elif weeklyGEXP > requiredGEXP:
                msg += str(player) + " is worthy of a promotion from [Member] to [Junior]"
            else:
                msg += str(player) + " is at risk of being **kicked** for Low GEXP!"
        else:
            msg += str(player) + " is worthy of a **promotion**."
    elif playerRank == "Junior" or playerRank == "Senior":
        if weeklyGEXP <= requiredGEXP:
            msg += str(player) + " is at risk of a **demotion**."
        else:
            msg += str(player) + " is safe from **kicks** and **demotions**."
    elif playerRank == "Junior" and weeklyGEXP >= requiredGEXP and memberTime.days >= 30:
        msg += str(player) + " is worthy of a promotion from [Junior] to [Senior]"

    await message.send(msg)

@bot.command()
async def member(message, *, player):

    await message.send("Getting guild stats for " + str(player) + "...")
    try:
        mojangInfo = requests.get("https://api.mojang.com/users/profiles/minecraft/" + str(player)).json()
    except:
        await message.send("Error: " + str(player) + " is not a real player")
        return
    uuid = mojangInfo["id"]

    guildInfo = requests.get("https://api.hypixel.net/guild?key=" + str(api_key) +"&player=" + str(uuid)).json()
    try:
        guildName = guildInfo["guild"]["name"]
    except:
        await message.send("Error: " + str(player) + " is not in a guild!")
        return

    if guildName != guild:
        status = "Not in " + str(guild)
        inCaped = False
    else:
        inCaped = True

    for i in range(len(guildInfo["guild"]["members"])):

        if guildInfo["guild"]["members"][i]["uuid"] == uuid:

            weeklyGEXPall = guildInfo["guild"]["members"][i]["expHistory"]
            weeklyGEXP = sum(weeklyGEXPall.values())

            playerRank = guildInfo["guild"]["members"][i]["rank"]

            joinDateRaw = guildInfo["guild"]["members"][i]["joined"] / 1000
            joinDate = datetime.fromtimestamp(joinDateRaw)

            dateNow = datetime.now()

            memberTime = dateNow - joinDate

            dailyGEXP = ""
            for j in weeklyGEXPall:
                day = guildInfo["guild"]["members"][i]["expHistory"][j]
                dailyGEXP += f"**{j}**: `{day}`\n"

            if inCaped == True:
                if playerRank == "Guild Master" or playerRank == "Admin" or playerRank == "Moderator":
                    status = "Safe"
                elif playerRank == "Member":
                    if weeklyGEXP <= requiredGEXP:
                        if memberTime.days < 7:
                            status = "New"
                        elif weeklyGEXP > requiredGEXP:
                            status = "Promote"
                        else:
                            status = "Kick"
                    else:
                        status = "Kick"
                elif playerRank == "Junior" or playerRank == "Senior":
                    if weeklyGEXP <= requiredGEXP:
                        status = "Demote"
                    else:
                        status = "Safe"
                elif playerRank == "Junior" and weeklyGEXP >= requiredGEXP and memberTime.days >= 30:
                    status = "Promote"

    fancy = discord.Embed(
        title=f"__{player} [{guild}]__",
        colour = discord.Color.dark_red()
    )
    fancy.set_thumbnail(url="https://crafatar.com/avatars/" + str(uuid))
    fancy.set_footer(text=footerText, icon_url=footerImage)

    fancy.add_field(name="__Joined__", value="`" + str(joinDate.strftime("%d %b %Y")) + "`\n `(" + str(memberTime.days) + " days)`")
    fancy.add_field(name="__Rank__", value="`[" + str(playerRank) + "]`")
    fancy.add_field(name="__Weekly GEXP__", value="`" + str(weeklyGEXP) + "`")
    fancy.add_field(name="__GEXP By Day__", value=str(dailyGEXP), inline=True)
    fancy.add_field(name="Status:", value="`" + str(status) + "`", inline=True)

    await message.send(embed=fancy)

@bot.command()
async def player(message, *, player):
    await message.send("Looking up info for " + str(player) + "...")
    try:
        mojangInfo = requests.get("https://api.mojang.com/users/profiles/minecraft/" + str(player)).json()
    except:
        print(player, "is not a real player")
        await message.send("Error: " + str(player) + " is not a real player")
        return
    uuid = mojangInfo["id"]

    mojangInfo = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + str(uuid)).json()
    playerName = mojangInfo["name"]

    guildInfo = requests.get("https://api.hypixel.net/guild?key=" + str(api_key) +"&player=" + str(uuid)).json()
    try:
        guildTag = guildInfo["guild"]["tag"]
    except:
        guildTag = ""

    guildName = guildInfo["guild"]["name"]

    playerInfo = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()

    lastLogin = datetime.fromtimestamp(playerInfo["player"]["lastLogin"] / 1000)
    lastLogin = str(lastLogin.strftime("%d %b %Y"))

    playerKarma = "{:,}".format(playerInfo["player"]["karma"])
    playerAP = "{:,}".format(playerInfo["player"]["achievementPoints"])
    playerXP = playerInfo["player"]["networkExp"]
    playerLevel = math.floor((math.sqrt((2 * playerXP) + 30625) / 50) - 2.5)

    fancy = discord.Embed(
        title = f"__{playerName}__ [{guildTag}]",
        colour = discord.Color.dark_red()
    )

    fancy.set_image(url="")
    fancy.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}")

    fancy.add_field(name="__Level__", value=f"`{playerLevel}`")
    fancy.add_field(name="__Karma__", value=f"`{playerKarma}`")
    fancy.add_field(name="__AP__", value=f"`{playerAP}`")
    fancy.add_field(name="__Last Login__", value=f"`{lastLogin}`")
    fancy.add_field(name="__Guild__", value=f"[{guildName}](https://plancke.io/hypixel/guild/name/{guildName})")

    fancy.set_footer(text=footerText, icon_url=footerImage)

    await message.send(embed=fancy)

@bot.command()
async def promotes(message):
    msg = "Getting promotions for Caped..."
    await message.send(msg)

    promoteList = []
    names = ""

    guildInfo = requests.get("https://api.hypixel.net/guild?key=" + str(api_key) +"&name=" + str(guild)).json()

    for i in range(len(guildInfo["guild"]["members"])):

        playerRank = guildInfo["guild"]["members"][i]["rank"]
        joinDateRaw = guildInfo["guild"]["members"][i]["joined"] / 1000
        weeklyGEXP = guildInfo["guild"]["members"][i]["expHistory"]
        uuid = guildInfo["guild"]["members"][i]["uuid"]

        weeklyGEXP = sum(weeklyGEXP.values())
        joinDate = datetime.fromtimestamp(joinDateRaw)
        dateNow = datetime.now()
        memberTime = dateNow - joinDate

        if playerRank == "Member":
            if memberTime.days < 7:
                continue
            elif weeklyGEXP >= requiredGEXP:
                mojangInfo = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + str(uuid)).json()
                playerName = mojangInfo["name"]
                promoteList.append(playerName)
                names += f"\n - `{playerName}` \t\t[Member] -> [Junior]"

        elif playerRank == "Junior":
            if memberTime.days >= 30:
                if weeklyGEXP >= requiredGEXP:
                    mojangInfo = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + str(uuid)).json()
                    playerName = mojangInfo["name"]
                    promoteList.append(playerName)
                    names += "\n - `" + str(playerName) + "` \t\t[Junior] -> [Senior]"

    fancy = discord.Embed(title="Promotes")

    if len(promoteList) == 0:
        fancy.add_field(name="Players:", value=f"There are no players\n eligible for promotions!\n All caught up!")
        fancy.set_footer(text=footerText, icon_url=footerImage)

    else:
        msg = "There are " + str(len(promoteList)) + " players who are eligible for promotions:\n"

        fancy.add_field(name="Players:", value=names)
        fancy.set_footer(text=footerText, icon_url=footerImage)

    await message.send(embed=fancy)

@bot.command()
async def demotes(message):
    msg = "Getting demotes for Caped..."
    await message.send(msg)

    demoteList = []
    names = ""

    guildInfo = requests.get("https://api.hypixel.net/guild?key=" + str(api_key) +"&name=" + str(guild)).json()

    for i in range(len(guildInfo["guild"]["members"])):

        playerRank = guildInfo["guild"]["members"][i]["rank"]
        weeklyGEXP = guildInfo["guild"]["members"][i]["expHistory"]
        uuid = guildInfo["guild"]["members"][i]["uuid"]

        weeklyGEXP = sum(weeklyGEXP.values())

        if playerRank == "Junior" or playerRank == "Senior":
            if weeklyGEXP <= requiredGEXP:
                mojangInfo = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + str(uuid)).json()
                playerName = mojangInfo["name"]
                demoteList.append(playerName)
                if playerRank == "Junior":
                    names += "\n - `" + str(playerName) + "` \t\t[Junior] -> [Member]"
                elif playerRank == "Senior":
                    names += "\n - `" + str(playerName) + "` \t\t[Senior] -> [Junior]"

    if len(demoteList) == 0:
        msg = "There are no players eligable for a demote in " + str(guild) + ". All caught up!"
    else:
        msg = "There are " + str(len(demoteList)) + " players who are eligible for demotions:\n"

    await message.send(str(msg) + str(names))

@bot.command()
async def kicks(message):
    msg = "Getting kicks for Caped..."
    await message.send(msg)

    kickList = []
    names = ""

    guildInfo = requests.get("https://api.hypixel.net/guild?key=" + str(api_key) +"&name=" + str(guild)).json()

    for i in range(len(guildInfo["guild"]["members"])):

        playerRank = guildInfo["guild"]["members"][i]["rank"]
        joinDateRaw = guildInfo["guild"]["members"][i]["joined"] / 1000
        weeklyGEXP = guildInfo["guild"]["members"][i]["expHistory"]
        uuid = guildInfo["guild"]["members"][i]["uuid"]

        weeklyGEXP = sum(weeklyGEXP.values())
        joinDate = datetime.fromtimestamp(joinDateRaw)
        dateNow = datetime.now()
        memberTime = dateNow - joinDate

        if playerRank == "Member":
            if memberTime.days > 7:
                if weeklyGEXP <= requiredGEXP:
                    mojangInfo = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + str(uuid)).json()
                    playerName = mojangInfo["name"]
                    kickList.append(playerName)
                    names += "\n - `" + str(playerName) + "`"

    if len(kickList) == 0:
        msg = "There are no players eligable for a kick in " + str(guild) + ". All caught up!"
    else:
        msg = "There are " + str(len(kickList)) + " players who are eligible for kicks:\n"

    await message.send(str(msg) + str(names))

bot.run("TOKEN")
