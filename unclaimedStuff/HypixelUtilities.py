import requests
from datetime import datetime
import math
import json
# Skill Name:Max Level
allSkills = {"taming":50, "farming":60, "mining":60, "combat":60, "foraging":50, "fishing":50, "enchanting":60, "alchemy":50, "carpentry":50, "runecrafting":25}
# All goes up to 50
dungeonSkills = ["catacombs", "mage", "archer", "berserk", "healer", "tank"]
# Skills that count towards Skill Average
skillAvgSkills = ["taming", "farming", "mining", "combat", "foraging", "fishing", "enchanting", "alchemy"]

slayerTypes = ["zombie", "spider", "wolf"]

skillProgression = [50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425, 97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425, 4722425, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425, 17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425, 38072425, 40972425, 44072425, 47472425, 51172425, 55172425, 59472425, 64072425, 68972425, 74172425, 79672425, 85472000, 91572425, 97972425, 104672425, 111672425]
runecraftingProgression = [0, 50, 150, 275, 435, 635, 885, 1200, 1600, 2100, 2725, 3510, 4510, 5760, 7325, 9325, 11825, 14950, 18950, 23950, 30200, 38050, 47850, 60100, 75400]
dungeonProgression = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640, 3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640, 453559640, 569809640]
wolfSlayerProgression = [10, 30, 250, 1500, 5000, 20000, 100000, 400000, 1000000]
otherSlayerProgression = [5, 25, 200, 1000, 5000, 20000, 100000, 400000, 1000000]

def getGuildNameInfo(key, guildName):
    """Gets the info for a guild via the name of the guild"""
    guildInfo = requests.get(f"https://api.hypixel.net/guild?key={key}&name={guildName.replace(' ', '%20')}").json()
    return guildInfo
def getGuildPlayerInfo(key, uuid):
    """Gets the info for a guild via the username of a player"""
    guildInfo = requests.get(f"https://api.hypixel.net/guild?key={key}&player={uuid}").json()
    return guildInfo
def getSBProfile(key, uuid):
    """Gets the most recent profile the player has played on"""
    skyblockData = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={uuid}").json()
    lastSaves = []
    correctProfile = 0
    try:
        for i in range(len(skyblockData["profiles"])):
            membersList = skyblockData["profiles"][i]["members"].keys()
            for x in membersList:
                if x == uuid:
                    try:
                        lastSaves.append([skyblockData["profiles"][i]["members"][x]["last_save"],i])
                    except:
                        next
    except:
        return "None"
    lastSaves.sort(reverse=True)
    correctProfile = lastSaves[0][1]
    recentProfile = skyblockData["profiles"][correctProfile]
    return recentProfile
def getSkillXP(sbProfile, uuid):
    """Gets all of a player's Skyblock Skills in an easier to read format"""
    skills = ["experience_skill_" + i for i in allSkills.keys()]
    xpData = []
    for i in skills:
        try:
            skillXP = round(sbProfile["members"][uuid][i], 2)
            xpData.append([i, skillXP])
        except:
            xpData.append([i, 0])
    return json.loads(json.dumps({i[0].replace("experience_skill_", "") + "XP":i[1] for i in xpData}))
def getSlayerXP(sbProfile, uuid):
    types = ["zombie", "spider", "wolf"]
    return json.loads(json.dumps({f"{bossType}XP":sbProfile["members"][uuid]["slayer_bosses"][bossType]["xp"] for bossType in types}))
def getDungeonXP(sbProfile, uuid):
    dungeonDir = sbProfile["members"][uuid]["dungeons"]
    cataDir = sbProfile["members"][uuid]["dungeons"]["dungeon_types"]["catacombs"]
    a = {"catacombsXP":round(cataDir["experience"], 2)}
    b = {f"{dungClass}XP":round(dungeonDir["player_classes"][dungClass]["experience"], 2) for dungClass in dungeonSkills if dungClass != "catacombs"}
    a.update(b)
    return a
def calcSkillLevel(skillName, skillXP):
    """Calculates the skill level of the given skill. Takes into account lvl 60 skills, dungeons and runecrafting. Uses the base skill name eg \"combat\". Works with Slayers."""
    skill = skillName.replace("XP", "").replace("skill_experience_", "").lower()
    # Runecrafting has a max level of 25 and a different XP increment per level
    if skill == "runecrafting":
        if skillXP >= 75400:
            return 25
        level = 0
        for i in skillProgression:
            if skillXP >= i:
                level += 1
            else:
                return level
    # Dungeons skills have different skill progression
    elif skill in dungeonSkills:
        if skillXP >= 569809640:
            return 50
        level = 0
        for i in dungeonProgression:
            if skillXP >= i:
                level += 1
            else:
                return level
    # The rest of the skills progress normally
    elif skill in allSkills.keys():
        if skillXP >= 111672425 and allSkills[skill] == 60:
            return 60
        elif skillXP >= 55172425 and allSkills[skill] == 50:
            return 50
        level = 0
        for i in skillProgression:
            if skillXP >= i:
                level += 1
            else:
                return level
    # If the skill is a slayer
    elif skill in slayerTypes:
        if skillXP >= 1000000:
            return 9
        level = 0
        if skill.lower() == "wolf":
            for i in wolfSlayerProgression:
                if skillXP >= i:
                    level += 1
                else:
                    return level
        elif skill.lower() == "zombie" or skill.lower() == "spider":
            for i in otherSlayerProgression:
                if skillXP >= i:
                    level += 1
                else:
                    return level
        else:
            return 0
def calcSkillAverage(skillXPData):
    """Calculates the skill average of a player using the data from getSkillXP() including level 60 skills & runecrafting"""
    # If a skill counts towards skill average (skillAvgSkills) then calculate what level it is and add it to a list
    skillLevels = [calcSkillLevel(i, skillXPData[i]) for i in skillXPData if i.replace('XP', '') in skillAvgSkills]
    return round(sum(skillLevels) / len(skillLevels), 2)
def calcHypixelLevel(networkXP):
    """Calculates the Hypixel Network Level via the amount of Network XP"""
    return int(math.floor((math.sqrt((2 * networkXP) + 30625) / 50) - 2.5))
def getPlayerInfo(key, uuid):
    """Returns the hypixel/player API information."""
    return requests.get(f"https://api.hypixel.net/player?key={key}&uuid={uuid}").json()
def getGuildMemberTime(joinDate):
    joinDate = datetime.fromtimestamp(joinDate)
    dateNow = datetime.now()
    memberTime = dateNow - joinDate
    return memberTime








