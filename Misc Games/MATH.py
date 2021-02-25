from appJar import gui
import random

class Numbers():
    def __init__(self):
        self.num1 = 0
        self.num2 = 0
        self.what = ["+","-","x"]
        self.answer = 0

        self.correct = 0
        self.incorrect = 0

        self.question = 0

num = Numbers()

def checkAnswer(btn):
    win.showLabel("INFO")
    playerAns = win.getEntry("ANSWER")
    try:
        float(playerAns)
    except:
        win.showLabel("INFO")
        win.setLabel("INFO","Enter an actual number!")
        win.clearEntry("ANSWER")
        return
    playerAns = int(playerAns)
    if playerAns == num.answer:
        win.setLabel("INFO","Correct!")
        num.correct += 1
    else:
        win.setLabel("INFO","Incorrect, try again!")
        num.incorrect += 1
        win.clearEntry("ANSWER")
        win.setFocus("ANSWER")
        updateScore()
        return

    genNumbers()
    makeQuestion()
    updateScore()

def updateScore():
    win.setLabel("SCORE",f"Correct: {num.correct}, Incorrect: {num.incorrect}")

def genNumbers():
    num.num1 = random.randint(0,12)
    num.num2 = random.randint(0,num.num1)

def makeQuestion():
    a = random.choice(num.what)
    if a == "x":
        ques = f"What is {num.num1} x {num.num2}?"
        num.answer = num.num1 * num.num2
        
    elif a == "+":
        ques = f"What is {num.num1} + {num.num2}?"
        num.answer = num.num1 + num.num2

    elif a == "-":
        ques = f"What is {num.num1} - {num.num2}?"
        num.answer = num.num1 - num.num2
    
    win.setLabel("QUESTION",ques)
    win.clearEntry("ANSWER")

win = gui(bg="black", fg="white", size="250x150")

win.setTitle("Math Game!")
win.addLabel("TITLE","Math Game").config(font=("Impact", "20", "underline"))
win.addLabel("QUESTION","Question")
win.addLabel("INFO","")
win.hideLabel("INFO")
win.addEntry("ANSWER")
win.addButton("Go", checkAnswer)
win.addLabel("SCORE",f"Correct: {num.correct}, Incorrect: {num.incorrect}")

win.setFocus("ANSWER")

genNumbers()
makeQuestion()
updateScore()

win.go()
