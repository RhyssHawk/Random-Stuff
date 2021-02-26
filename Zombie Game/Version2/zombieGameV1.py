from appJar import gui
import random
from random import randint
import json
import math

# Another dumb attempt at a Zombie game
# Actually making use of Classes now
# Zombies have weaknesses and multiple attacks
# If a player attacks with a Zombie's weakness weapon, it deals double damage
# Zombies start with completely random stats
# Weapons and Healing rarities based off of weighted loot table
# Better inspect function
# General nicer looking everything
# Better gameplay


# Load files to make randomly generated names in the game
with open("zombiePrefixes.json","r") as a:
    zPrefixes = json.load(a)
with open("zombieSuffixes.json","r") as a:
    zSuffixes = json.load(a)
with open("namesList.json","r") as a:
    pName = random.choice(json.load(a))

# {Attack:Damage}
zAttacks = {"Bite":25,"Flail":0,"Charge":30,"Swing":25,"Spit":10,"Growl":0,"Rock Throw":20}

# Formatted as ["itemName", itemDamage, lootWeight]
weapons = [["Chainsaw", 30, 1],["Baseball Bat", 15, 3],["Knife", 10, 5],["Machete", 20, 2],["Sword", 25, 1],["Fists", 5, 0]]
healing = [["Roast Chicken",30,1],["Apple",15,3],["Rice Ball",10,4],["Lollypop",5,10],["Steak",50,1],["Twinkie",5,10]]

# Zombie Class
class Zombie():
    def __init__(self, name, hp, attacks, weaknesses):
        self.name = name
        self.hp = hp
        self.attacks = attacks
        self.weaknesses = weaknesses
    def getStats(self):
        a = f"{self.name}'s Stats:\n"
        a += f" - Health: {self.hp}\n"
        a += f" - Attacks: \n{printList(self.attacks)}\n"
        a += f" - Weaknesses: \n{printList(self.weaknesses)}"
        return a
    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            info(f"{self.name} has been defeated!")
            user.canMove = True
            disableButtons(["Attack"])
    def attack(self):
        attackChosen = random.choice(self.attacks)
        if attackChosen == "Flail":
            damage = math.ceil(random.randint(0,70) / 10) * 10
        else:
            damage = zAttacks[attackChosen]
        user.takeDamage(damage)
        updatePStats()
        if user.hp > 0:
            info(f"{self.name} used {attackChosen} and dealt\n{damage} damage to you!\n{self.getStats()}")
            

# Player Class
class Player():
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.weapons = ["Fists"]
        # {item:amount}
        self.healing = {"Apple":1}

        self.inspectedTiles = []

        self.canMove = True
    def getStats(self):
        a = f"{self.name}'s Stats:\n"
        a += f" - Health: {self.hp}\n"
        a += f" - Weapons:\n"
        a += printList(self.weapons) + "\n"
        a += f" - Healing:\n"
        a += printList(self.healing)
        return a
    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            endGame(f"You were killed by {zombie.name}!\n")
    def attack(self, weapon):
        for i in range(len(weapons)):
            if weapon == weapons[i][0]:
                if weapons[i][0] in zombie.weaknesses:
                    dmg = weapons[i][1] * 2
                else:
                    dmg = weapons[i][1]
                updatePStats()
                zombie.takeDamage(dmg)
                if zombie.hp > 0:
                    info(f"You used your {weapons[i][0]} and dealt {dmg} damage to {zombie.name}!\n{zombie.getStats()}")
                    zombie.attack()
                

    def inspect(self):
        if map.getCoords() in self.inspectedTiles:
            info("You have already inspected this area!\n\n\n\n")
            return
        wFound = []
        hFound = {}
        # Loot table for weapons
        for i in range(len(weapons)):
            for j in range(weapons[i][2]):
                if random.randint(0,10) == 1 and weapons[i][0] not in user.weapons:
                    # Add to inventory and temp search overview list
                    wFound.append(weapons[i][0])
                    user.weapons.append(weapons[i][0])
        # Loot table for healing
        for i in range(len(healing)):
            for j in range(healing[i][2]):
                if random.randint(0,8) == 1:
                    # Add to the player's inventory
                    if healing[i][0] not in user.healing:
                        user.healing[healing[i][0]] = 1
                    else:
                        user.healing[healing[i][0]] += 1
                    # Add to temp list to give search overview
                    if healing[i][0] not in hFound:
                        hFound[healing[i][0]] = 1
                    else:
                        hFound[healing[i][0]] += 1
        infoBox = "You inspected the area!\n"
        if len(wFound) > 0:
            infoBox += "Weapons Found:\n"
            infoBox += printList(wFound)
        
        if len(hFound) > 0:
            infoBox += "\nHealing Found:\n"
            infoBox += printList(hFound)
        user.inspectedTiles.append(map.getCoords())
        info(infoBox)
        updatePStats()
    def heal(self, item):
        if user.healing[item] > 1:
            user.healing[item] -= 1
        else:
            del user.healing[item]
        for i in range(len(healing)):
            if healing[i][0] == item:
                self.hp += healing[i][1]
                info(f"You ate 1x {item} and healed for {healing[i][1]} health!\n\n\n\n\n")
                updatePStats()
                self.setupHeal()
    def setupAttack(self):
        game.changeOptionBox("options", self.weapons)
    def setupHeal(self):
        if len(user.healing) == 0:
            info("You have no healing items left!\n\n\n\n\n")
            game.changeOptionBox("options",[""])
            return
        enableButtons(["Go"])
        game.changeOptionBox("options", list(user.healing.keys()))
        game.enableOptionBox("options")
# Map Class
class Map():
    def __init__(self):
        self.minX = 0
        self.minY = 0
        self.maxX = 5
        self.maxY = 5

        self.xPos = 2
        self.yPos = 2

        self.bunkers = []

    def getCoords(self):
        return f"({self.xPos},{self.yPos})"
    def setupMove(self):
        game.changeOptionBox("options",directions)
        game.enableOptionBox("options")
        enableButtons(["Go"])
    def move(self, direction):
        if user.canMove == False:
            return
        if direction == "North":
            if self.yPos < 5:
                self.yPos += 1
            else:
                info("You cannot move North any further!\n\n\n\n\n")
                return
        elif direction == "East":
            if self.xPos < 5:
                self.xPos += 1
            else:
                info("You cannot move East any further!\n\n\n\n\n")
                return
        elif direction == "South":
            if self.yPos > 0:
                self.yPos -= 1
            else:
                info("You cannot move South any further!\n\n\n\n\n")
                return
        elif direction == "West":
            if self.xPos > 0:
                self.xPos -= 1
            else:
                info("You cannot move West any further!\n\n\n\n\n")
                return
        updateCoords()
        if self.getCoords() in self.bunkers:
            endGame("You found a bunker!\n")
            return
        info(f"You moved {direction}!\n\n\n\n\n")
        if random.randint(0,3) == 1:
            global zombie
            zombie = genZombie()
            startBattle()
    def genBunkers(self):
        for i in range(3):
            x = random.randint(self.minX,self.maxX)
            y = random.randint(self.minY,self.maxY)
            self.bunkers.append(f"({x},{y})")
            print(f"Generated bunker at {self.bunkers[i]}")
directions = ["North","East","South","West"]

def genZombie():
    name = random.choice(zPrefixes) + " " + random.choice(zSuffixes)
    hp = math.ceil(random.randint(10,100) / 10) * 10
    attacks = getRandom(zAttacks, 3)
    weaponsNoStats = []
    for i in range(len(weapons)):
        weaponsNoStats.append(weapons[i][0])
    weaknesses = getRandom(weaponsNoStats, random.randint(0,3))
    if weaknesses == []:
        weaknesses = ["None"]
    return Zombie(name, hp, attacks, weaknesses)
# Print pretty list without line break at the end
def printList(x):
    a = ""
    if type(x) == list:
        for i in range(len(x)):
            if i != len(x) - 1:
                a += f"    - {x[i]}\n"
            else:
                a += f"    - {x[i]}"
    elif type(x) == dict:
        for i in range(len(list(x.keys()))):
            if i != len(list(x.keys())) - 1:
                a += f"    - {x[list(x.keys())[i]]}x {list(x.keys())[i]}\n"
            else:
                a += f"    - {x[list(x.keys())[i]]}x {list(x.keys())[i]}"
            
    return a
# Get x amount of any random values in a dict or list with no duplicates.
def getRandom(obj, amount):
    if len(obj) <= amount:
        return obj
    a = []
    while len(a) < amount:
        if type(obj) == dict:
            x = random.choice(list(obj.keys()))
            if x not in a:
                a.append(x)
        elif type(obj) == list:
            x = random.choice(obj)
            if x not in a:
                a.append(x)
    return a
def startBattle():
    infoBox = f"Uh oh! You encountered a {zombie.name}! Prepare for battle!\n"
    game.changeOptionBox("options",user.weapons)
    infoBox += zombie.getStats()
    info(infoBox)
    user.canMove = False
    enableButtons(["Attack"])    
def endGame(reason):
    info(reason + "\nGame Over!\n\n")
    disableButtons(["Move","Inspect","Attack","Heal","Go"])
    game.disableOptionBox("options")
    user.canMove = False
def press(x):
    if x == "Move":
        map.setupMove()
    elif x == "Inspect":
        user.inspect()
    elif x == "Attack":
        user.setupAttack()
    elif x == "Heal":
        user.setupHeal()   
def submit():
    ans = game.getOptionBox("options")
    if ans in directions:
        map.move(ans)
    elif ans in user.weapons:
        user.attack(ans)
    elif ans in user.healing:
        user.heal(ans)
def setup():
    print("\nSetting up the game!\n")

    game.addLabel("title","Zombie Game!",0,1).config(font=("Impact",30, "bold", "underline"))
    game.addLabel("lb1",f"Your name is now {user.name}!\nCoordinates: {map.getCoords()}\n",1,1)
    game.addLabel("pStats",user.getStats(),0,2,2,5)
    game.setLabelBg("pStats","#2e2e2e")

    game.addButtons(["Move","Inspect","Attack","Heal"],press,2,1)
    game.addOptionBox("options",[""],3,1)
    game.addButton("Go",submit,4,1)

    game.addLabel("info","\n\n\n\n\n\n\n",5,1,2,3)
    game.setLabelBg("info","#242424")
    enableButtons(["Move","Inspect"])
    disableButtons(["Go","Attack"])
    game.disableOptionBox("options")

    game.setSize("500x400")
    
    map.genBunkers()
    game.go()
def enableButtons(array):
    for i in array:
        game.enableButton(i)
def disableButtons(array):
    for i in array:
        game.disableButton(i)
def info(information):
    game.setLabel("info",information)
def updatePStats():
    game.setLabel("pStats",user.getStats())
def updateCoords():
    game.setLabel("lb1",f"\nCoordinates: {map.getCoords()}\n")
game = gui("Dumb Zombie Game", fg="#d9d9d9", bg="#363636")
user = Player(pName)
map = Map()

setup()
