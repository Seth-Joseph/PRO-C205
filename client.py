import socket
from tkinter import *
import tkinter as tk
import random
from PIL import ImageTk, Image
from tkmacosx import Button  # For Mac users only
import platform

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None
canvas2 = None

playerName = None
nameEntry = None

nameWindow = None
gameWindow = None

screen_width = None
screen_height = None

ticketGrid  = []
currentNumberList = []
flashNumberList = []
flashNumberLabel = None

print('PRO-C205:TAMBOLA Stage-2')

def createTicket():
    global gameWindow
    global ticketGrid
    mainLabel  = Label(gameWindow,width=126,height=21,relief='ridge',borderwidth=5,bg="white")
    mainLabel.place(x=215,y=254)

    xPos = 223
    yPos = 264
    for row in range(0,3):
        rowList = []
        for col in range(0,9):
            if (platform.system() == 'Darwin'):
                #for Mac users
                boxButton = Button(gameWindow,font = ("Comic Sans MS", 18),borderwidth=1,pady=23,padx=22,bg="#FF835A",highlightbackground='#fff176',activebackground='#c5e1a5',width=3)
                boxButton.place(x=xPos,y=yPos)
            else:
                #for windows Users
                boxButton = tk.Button(gameWindow,font = ("Comic Sans MS", 18),borderwidth=1,pady=23,padx=22,bg="#FF835A",highlightbackground='#fff176',activebackground='#c5e1a5',width=3,bd=0)
                boxButton.place(x=xPos,y=yPos)
            rowList.append(boxButton)
            xPos += 98
        ticketGrid.append(rowList)
        xPos = 223
        yPos += 103

def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1

        numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50 , 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        }

        counter = 0
        while (counter < len(randomColList)):
            colNum = randomColList[counter]
            numbersListByIndex = numberContainer[str(colNum)]
            randomNumber = random.choice(numbersListByIndex)

            if(randomNumber not in currentNumberList):
                numberBox = ticketGrid[row][colNum]
                numberBox.configure(text=randomNumber, fg="black",bg="#fff176")
                currentNumberList.append(randomNumber)

                counter+=1

def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global flashNumberLabel

    gameWindow = Tk()
    gameWindow.title("Tambola Family Game")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/logo.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)
    canvas2.create_text(37,750, text = "Stage 2", font=("Comic Sans MS",15), fill="white")
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    createTicket()
    placeNumbers()

    flashNumberLabel = canvas2.create_text(160,13, text = "Waiting for other players to join...", font=("Comic Sans MS",15), fill="white")
    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def saveName():
    global SERVER
    global playerName 
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1 
    global screen_width
    global screen_height
    
    nameWindow = Tk()
    nameWindow.title("Tambola Family Game")
    nameWindow.attributes('-fullscreen',True)
    
    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/logo.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)

    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/4 +110, text = "Enter Name", font=("Comic Sans MS",30), fill="white")
    canvas1.create_text(37,750, text = "Stage 2", font=("Comic Sans MS",15), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Comic Sans MS', 25), bd=0, bg='white')
    nameEntry.place(x = screen_width/3+80, y=screen_height/2-20)
    nameEntry.focus()

    button = tk.Button(nameWindow, text="Save", font=("Comic Sans MS", 25),width=4, height=1,command=saveName, bg="#E38D65", fg='#FFF',bd=0)
    button.place(x = screen_width/2-50, y=screen_height/2 + 50)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    askPlayerName()

setup()