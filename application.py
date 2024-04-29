#!/usr/bin/python3
import customtkinter
import tkinter as tk
import random
from database import my_db_manager as dbm
import flaskrequests as fr
from datetime import datetime
import time
from functools import reduce
import pandas as pd
import matplotlib as pd


def getRandomValues():
   random.seed(datetime.now().timestamp())
   val1, val2, val3 = random.randint(0, 13), random.randint(0, 13), random.randint(0, 13) 
   return [val1, val2, val3]

class LogInFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = "Enter your login details"

        self.loginlabel = customtkinter.CTkLabel(self, text="Enter your login details")
        self.userNameEntry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.passWordEntry = customtkinter.CTkEntry(self, placeholder_text="Password")
        self.loginlabel.grid(row=0, column=0, padx=20, pady=(20,0), sticky="ew")
        self.userNameEntry.grid(row=1, column=0, padx=10, pady=(10,0), sticky="ew")
        self.passWordEntry.grid(row=2, column=0, padx=10, pady=(10,0), sticky="ew")

    def get(self):
        validation = []
        validation.append(self.userNameEntry.get())
        validation.append(self.passWordEntry.get())
        return validation
    
class GameGrid(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        master.geometry("800x360")
        self.values = values

        for i, value in enumerate(self.values):
            option = customtkinter.CTkButton(self, text=str(value))
            option.grid(row = 0, column=i, padx=10, pady=(10,0), sticky="ew")
        
        self.answer = customtkinter.CTkEntry(self, placeholder_text="Enter Answer here")
        self.answer.grid(row = 1, column=1, padx=10, pady=(10,0))
    
    def get(self):
        return self.answer.get()
    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.activeGrids = []

        self.title("Multiplication Game")
        self.geometry("400x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.loginFrame = LogInFrame(self)
        self.loginFrame.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.register_button = customtkinter.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew", columnspan=2)
        self.activeGrids.append(self.loginFrame)
        self.activeGrids.append(self.login_button)
        self.activeGrids.append(self.register_button)


    def forgetCurrentGrid(self):
        for frame in self.activeGrids:
            frame.grid_forget()
        self.activeGrids = []
        
    def showStartFrame(self):
        self.forgetCurrentGrid()
        self.startGameButton = customtkinter.CTkButton(self, text="Start Game", command=self.startGame)
        self.activeGrids.append(self.startGameButton)
        self.startGameButton.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.startMultiGameButton = customtkinter.CTkButton(self, text="Start Multiplayer Game", command=self.startMultiGame)
        self.activeGrids.append(self.startMultiGameButton)
        self.startMultiGameButton.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.scoreOverTimeButton = customtkinter.CTkButton(self, text="Show my score over time", command=self.showScoreOverTime)
        self.activeGrids.append(self.scoreOverTimeButton)
        self.scoreOverTimeButton.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)


    def showScoreOverTime(self):
        db = fr.getHistoricalData(self.username)
    def checkIfThereAreTwoUsers(self):
        print("it's checking if there are two users again")
        resp = fr.check_if_two_users()
        if resp["two"]:
            self.startGame(multiplayer=True)
        else:
            self.after(10000, self.checkIfThereAreTwoUsers)

    def startMultiGame(self):
        print("We've started the multi game")
        data = fr.initial_start_game(self.username)
        setofthree = data["values"].split("h")
        self.GameQuestions = []
        for value in setofthree:
            self.GameQuestions.append(value.split("z"))
        if data["first"] == True:
            self.first = True
            self.checkIfThereAreTwoUsers()
        else:
            self.first = False
            self.startGame(multiplayer=True)



    def startGame(self, multiplayer = False):
        self.multiplayer = multiplayer
        self.score = 0
        self.rounds = 5
        self.start = time.time()
        self.answer_button = customtkinter.CTkButton(self, text="Submit", command=self.submitAnswer)    
        self.answer_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.forgetCurrentGrid()
        if not multiplayer:
            self.GameQuestions = [getRandomValues(), getRandomValues(), getRandomValues(), getRandomValues(), getRandomValues()]
        self.gameGrid = GameGrid(self, self.GameQuestions[4])
        self.gameGrid.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")



    def showScore(self):
        user = self.username
        score = self.score
        time = self.end - self.start
        if not self.multiplayer:
            tk.messagebox.showinfo(title="Round complete", message=f"User {user} completed the test in {time} seconds and scored {score}")
        else:
            print("think")


        self = App()

    def submitAnswer(self):
        self.rounds -= 1
        useranswer = self.gameGrid.get()
        correctanswer = reduce(lambda x, y: int(x) * int(y), self.gameGrid.values)
        if (useranswer.isdigit() and int(useranswer) == correctanswer):
            self.score += 1
        if (self.rounds > 0):
            self.gameGrid = GameGrid(self, self.GameQuestions[self.rounds])
            self.gameGrid.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew", columnspan=3)
        else:
            self.end = time.time()
            self.gameGrid.grid_remove()
            self.answer_button.grid_remove()
            if not self.multiplayer:
                fr.insertSinglePlayerGame(self.username, self.score, self.end - self.start)
            else:
                fr.insertMultiPlayerGame(self.first, self.score, self.end - self.start)
                self.after(5000, self.getMultiResults)
            self.showScore()

    def getMultiResults(self):
        data = fr.get_multi_results()
        print("getting the multiresults again")
        if data["complete"]:
            user1score = data["value"][3]
            user2score = data["value"][4]
            user1time = data["value"][5]
            user2time = data["value"][6]
            username1 = data["user1username"]
            username2 = data["user2username"]
            tk.messagebox.showinfo(title="Multiplayer complete", message=f"User {username1} completed the test in {user1time} seconds and scored {user1score}, User {username2} completed the test in {user2time} seconds and scored {user2score}")
        else:
            self.getMultiResults()

    def login(self):
        values = self.loginFrame.get()
        self.username = values[0].strip()
        self.password = values[1].strip()
        userinfo = fr.get_user_info(self.username)
        if userinfo["id"] > 0 and userinfo["password"] == self.password:
            self.showStartFrame()
        else:
            tk.messagebox.showerror(title="Login Failed", message="Check your login, or sign up")

    def register(self):
        values = self.loginFrame.get()
        self.username = values[0].strip()
        self.password = values[1]
        userinfo = fr.get_user_info(self.username)
        if userinfo["id"] < 0:
            fr.insert_user(self.username, self.password)
        else:
            tk.messagebox.showerror(title="Register failed", message="username already exists in database")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
