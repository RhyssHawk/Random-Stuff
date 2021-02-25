import random
from appJar import gui

win = gui(bg="black",fg="white")

class Game():
    def __init__(self):
        self.tokens = [["Unicorn",5],["Zebra",0.5],["Donkey",0],["Horse",0.5]]
        self.balance = 0

game = Game()

def submit():
    token = random.choice(game.tokens)
    game.balance -= 1
    game.balance += token[1]
    win.setLabel("RESULT",f"You got a {token[0]} and won ${token[1]}")
    win.setLabel("Balance",f"Balance: ${game.balance:,}")

def exit():
    win.setLabel("RESULT","")
    win.setLabel("INFO",f"You chose to end the game \nAnd walked away with ${game.balance:,}.\nThanks for playing!")
    win.disableButton("Go")
    win.disableButton("Exit")

def setup():
    money = win.getEntry("$")
    try:
        float(money)
    except:
        win.setLabel("INFO","Please enter an actual number!")
        return

    game.balance = int(money)
    win.removeLabel("a")
    win.removeEntry("$")
    win.removeButton("Proceed")
    win.removeLabel("SPACER")
    

    win.setLabel("INFO","Press \"Go\" to generate a token!")
    win.addLabel("RESULT","")
    win.addButtons(["Go","Exit"],[submit,exit])
    win.addLabel("Balance",f"Balance: ${game.balance:,}")

win.addLabel("TITLE","Lucky Unicorn").config(font=("Impact","20","underline"))
win.addLabel("a","How much money would you like \nto start with?")
win.addLabel("INFO","")
win.addLabelEntry("$")
win.addLabel("SPACER","")
win.addButton("Proceed",setup)

win.go()