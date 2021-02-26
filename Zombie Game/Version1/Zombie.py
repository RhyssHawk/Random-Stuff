from appJar import gui
import random
import re

class Player():
    def __init__(self):
        self.hp = 20
        self.weapons = [["Fists",2,1]]
        self.healing = [["Apple",2,1]]

        self.moving = False
        self.healer = False
        self.battling = False
    def updateStats(self):
        info = "------------------------------------------------\n"
        info += "Your Stats:\n"
        info += f"Health: {self.hp} hp\n"
        info += "Weapons:\n"
        for i in self.weapons:
            info += f"  - x{i[2]} {i[0]} (+{i[1]} dmg)\n"
        info += "Healing:\n"
        for i in self.healing:
            info += f"  - x{i[2]} {i[0]} (+{i[1]} dmg)\n"
        info += "------------------------------------------------"
        win.setLabel("STATS",info)
    def heal(self):
        info = ""
        healingItem = win.getOptionBox("Options")
        for i in self.healing:
            chosenHealing = re.findall(i[0],healingItem)
            for x in chosenHealing:
                for y in self.healing:
                    if x == y[0]:
                        self.hp += y[1]
                        y[2] -= 1
                        info += f"You ate 1x {y[0]} for +{y[1]} hp!\n"
                        if y[2] == 0:
                            self.healing.remove(y)
        if len(player.healing) <= 0:
            info += "You have run out of healing!"
            win.setLabel("INFO",info)
            self.healer = False
            if player.battling == True:
                encounter()
            else:
                default()
        else:
            player.updateHealing()
        player.updateStats()
    def updateHealing(self):
        newList = []
        for i in player.healing:
            newList.append(f"x{i[2]} {i[0]} (+{i[1]} hp)")
        win.changeOptionBox("Options",newList)
    def updateWeapons(self):
        newList = []
        for i in player.weapons:
            newList.append(f"x{i[2]} {i[0]} (+{i[1]} dmg)")
        win.changeOptionBox("Options",newList)
    def attack(self):
        info = ""
        weapon = win.getOptionBox("Options")
        for i in self.weapons:
            chosenWeapon = re.findall(i[0],weapon)
            for x in chosenWeapon:
                for y in self.weapons:
                    if x == y[0]:
                        zombie.hp -= y[1]
                        y[2] -= 1
                        info += f"You used {y[0]} and\n dealt +{y[1]} damage!\n"
                        if y[2] == 0:
                            self.weapons.remove(y)
        if len(player.weapons) <= 0:
            player.weapons.append(["Fists",2,1])
            player.updateWeapons()
        else:
            player.updateWeapons()
        zombie.updateStats()
        if zombie.hp <= 0:
            info += "You killed the zombie!"
            self.attacking = False
            default()
            map.updatePosition()
        else:
            info += zombie.attack()
        win.setLabel("INFO",info)
        player.updateStats()

class Zombie():
    def __init__(self):
        self.hp = 10
        self.attacks = [["Flail",0],["Attack",7],["Growl",0]]
    def updateStats(self):
        win.setLabel("COORDS",f"Zombie Health: {self.hp} hp")
    def attack(self):
        chosenAttack = random.choice(self.attacks)
        if chosenAttack == "Flail":
            a = random.randint(0,15)
        else:
            a = chosenAttack[1]
        player.hp -= a
        info = f"Zombie used {chosenAttack[0]} \nand dealt {chosenAttack[1]} damage"
        return info

class Map():
    def __init__(self):
        self.rows = 10
        self.columns = 10
        self.xpos = 5
        self.ypos = 5

        self.bunkers = []
    def move(self):
        info = ""
        tooFar = False
        direction = win.getOptionBox("Options")
        if direction == "North":
            if self.ypos == self.columns:
                info = "You are too far North!"
                tooFar = True
            else:
                self.ypos += 1
                info = "You moved North"
        elif direction == "East":
            if self.xpos == self.rows:
                info = "You are too far East!"
                tooFar = True
            else:
                self.xpos += 1
                info = "You moved East"
            
        elif direction == "South":
            if self.ypos == 1:
                info = "You are too far South!"
                tooFar = True
            else:
                self.ypos -= 1
                info = "You moved South"

        elif direction == "West":
            if self.xpos == 1:
                info = "You are too far West!"
                tooFar = True
            else:
                self.xpos -= 1
                info = "You moved West"
        win.setLabel("INFO",info)
        map.updatePosition()
        if map.checkBunker() == True:
            return
        if tooFar == False:
            win.enableButton("Inspect")
            zombieChance = random.randint(1,5)
            if zombieChance == 1:
                encounter()
    def updatePosition(self):
        win.setLabel("COORDS",f"Location: ({self.xpos}, {self.ypos})")
    def genBunkers(self):
        for i in range(3):
            x = random.randint(1,self.rows)
            y = random.randint(1,self.columns)
            self.bunkers.append(f"({x},{y})")
            print(f"Generated a bunker at ({x},{y})")
    def checkBunker(self):
        currentPos = f"({self.xpos},{self.ypos})"
        for i in self.bunkers:
            if i == currentPos:
                endGameWin()
                return True
        return False

def default():
    win.changeOptionBox("Options",[""])
    win.disableButton("Cancel")
    win.enableButton("Inspect")
    win.enableButton("Move")
    win.enableButton("Heal")
    win.disableButton("Go")
    win.disableOptionBox("Options")
def inspect():
    info = "You inspected the area and found:\n"
    weapons = [["Chainsaw",10,1],["Baseball Bat",5,1],["Water Gun",0.5,1],["Knife",3,1]]
    healing = [["Roast Chicken",20,1],["Apple",4,1],["Lollypop",1,1],["Rice Ball",8,1]]
    foundWeapons = []
    foundHealing = []
    for i in range(len(weapons)):
        a = random.randint(0,3)
        if a == 1:
            dupe = False
            loot = random.choice(weapons)
            for x in foundWeapons:
                if loot[0] == x[0]:
                    x[2] += 1
                    dupe = True
            if dupe == False:
                foundWeapons.append(loot)
    for i in range(len(weapons)):
        a = random.randint(0,3)
        if a == 1:
            dupe = False
            loot = random.choice(healing)
            for x in foundHealing:
                if loot[0] == x[0]:
                    x[2] += 1
                    dupe = True
            if dupe == False:
                foundHealing.append(loot)
    
    for i in foundWeapons:
        dupe = False
        for x in player.weapons:
            if i[0] == x[0]:
                dupe = True
                x[2] += 1
        if dupe == False:
            player.weapons.append(i)

    for i in foundHealing:
        dupe = False
        for x in player.healing:
            if i[0] == x[0]:
                dupe = True
                x[2] += 1
        if dupe == False:
            player.healing.append(i)
        info += f"  - x{i[2]} {i[0]}\n"
    if len(foundHealing) == 0:
        info = "You inspected the area but\ndidn't find anything."
    win.disableButton("Inspect")
    win.setLabel("INFO",info)
    player.updateStats()
def move():
    player.moving = True
    win.enableButton("Go")
    win.disableButton("Heal")
    win.enableOptionBox("Options")
    win.setLabel("INFO","Pick a direction to move")
    win.enableButton("Cancel")
    win.disableButton("Move")
    win.changeOptionBox("Options",["North","East","South","West"])
def heal():
    if len(player.healing) == 0:
        info = "You have no healing items left!"
    else:
        info = "Choose a healing item"
        player.healer = True
        win.enableButton("Go")
        win.enableButton("Cancel")
        win.enableOptionBox("Options")
        win.disableButton("Heal")
        player.updateHealing()
    win.setLabel("INFO",info)
def submit(btn):
    if player.moving == True:
        map.move()
        return
    elif player.healer == True:
        player.heal()
        return
    elif player.battling == True:
        player.attack()
        return
    return
def cancel():
    if player.moving == True:
        player.moving = False
        info = "You cancelled moving"
        default()
    elif player.healer == True:
        player.healer = False
        info = "You cancelled healing"
        if player.battling == True:
            encounter()
        else:
            default()
    
    win.setLabel("INFO",info)
def encounter():
    player.moving = False
    win.setLabel("INFO","You have encountered a\nZombie! Prepare for battle!\nChoose an attack.")
    player.battling = True
    default()
    win.disableButton("Inspect")
    win.disableButton("Move")
    win.enableOptionBox("Options")
    win.enableButton("Go")
    zombie.updateStats()
    player.updateWeapons()
    

def endGameWin():
    default()
    win.disableButton("Inspect")
    win.disableButton("Move")
    win.disableButton("Heal")
    win.setLabel("INFO","Congratz!\nYou won the game!")

player = Player()
zombie = Zombie()
map = Map()

win = gui(fg="white",bg="black")
win.setSize("550x235")

win.addLabel("TITLE","Zombie Game").config(font=("impact","20","underline"))
win.addLabel("STATS","",0,2,0,10)
player.updateStats()
win.addLabel("INFO","Choose an action")
win.addOptionBox("Options",["One","Two","Three"])
win.addLabel("COORDS","")
map.updatePosition()
win.addButtons(["Inspect","Move","Heal"],[inspect, move, heal])
win.addButtons(["Go","Cancel"],[submit, cancel])
win.addLabel("SPACER","")
map.genBunkers()
default()

win.go()
