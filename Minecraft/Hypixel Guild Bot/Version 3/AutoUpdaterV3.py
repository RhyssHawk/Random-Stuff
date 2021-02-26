
import MinecraftUtils as mc
import HypixelUtils as hy
import json
import requests
import time

guildName = "Caped"
with open("apiKey","r") as key:
    key = key.read()

#Check if a uuid is in the database already
def inDatabase(data, uuid):
    for i in range(len(data["players"])):
        if data["players"][i]["uuid"] == uuid:
            return True
    return False
#Write data to the file
def writeData(data):
    with open("playerInfo.json","w") as dbFile:
        json.dump(data, dbFile)
def removePlayer(uuid):
    with open("playerInfo.json","r") as a:
        a = json.load(a)
        for i in range(len(a["players"])):
            if a["players"][i]["uuid"] == uuid:
                del a["players"][i]
                writeData(a)
                return
#If file doesn't exist or badly formatted then make a fresh one
try:
    with open("playerInfo.json","r") as playerInfo:
        playerInfo = json.load(playerInfo)
        x = len(playerInfo["players"])
except:
    with open("playerInfo.json","w") as playerInfo:
        json.dump({"players":[]}, playerInfo)

while True:
    guildInfo = requests.get(f"https://api.hypixel.net/guild?key={key}&name={guildName}").json()
    total = len(guildInfo["guild"]["members"])
    #Loop through every member in the guild
    for i in range(total):
        print(f"{i+1}/{total}")
        uuid = guildInfo["guild"]["members"][i]["uuid"]
        playerName = mc.getPlayerName(uuid)
        playerInfo = {
            "uuid":uuid,
            "playerName":playerName
        }
        try:
            #Try getting skyblock data of the player
            sbProfile = hy.getRecentProfile(key, uuid)
            sbData = {
                "skyblock":{
                    "stats":{
                        "highestCrit":sbProfile["members"][uuid]["stats"]["highest_critical_damage"]
                    },
                    "skills":hy.getSkyblockSkills(sbProfile, uuid),
                    "slayer":{
                        "zombieXP":sbProfile["members"][uuid]["slayer_bosses"]["zombie"]["xp"],
                        "spiderXP":sbProfile["members"][uuid]["slayer_bosses"]["spider"]["xp"],
                        "wolfXP":sbProfile["members"][uuid]["slayer_bosses"]["wolf"]["xp"]
                    }
                }
            }
            playerInfo.update(sbData)
        except:
            pass
        #Load the "playerInfo.json" file
        with open("playerInfo.json","r") as db:
            db = json.load(db)
            #If the player is already in the database then update their data
        if inDatabase(db, uuid):
            #Go through all players in "playerInfo.json" file
            for i in range(len(db["players"])):
                #If player in file matches uuid
                if db["players"][i]["uuid"] == uuid:
                    #Update their data
                    db["players"][i] = playerInfo
                    #Write a new file with updated data
                    writeData(db)
        else:
            #Add the player onto the data and write to file
            db["players"].append(playerInfo)
            writeData(db)
            #Debug
            print(f"Added {playerName} to the database!")
    #Remove players who are not in the guild from the "playerInfo.json" file
    #Load file
    with open("playerInfo.json","r") as db:
        db = json.load(db)
    removeList = []
    for i in range(len(db["players"])):
        inGuild = False
        for j in range(len(guildInfo["guild"]["members"])):
            if db["players"][i]["uuid"] == guildInfo["guild"]["members"][j]["uuid"]:
                inGuild = True
                break
        if inGuild == False:
            removeList.append(db["players"][i]["uuid"])
    for i in removeList:
        removePlayer(i)
        print(f"Removed {i} from database!")
    
    #Wait 10 mins before looping again
    print("Done Cycle, waiting 10 minutes!")
    time.sleep(600)

