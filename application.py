#!/usr/bin/python3
import customtkinter
import tkinter as tk
import random
from database import my_db_manager as dbm
from datetime import datetime
import time
from functools import reduce


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
            option.grid(row = 0, column=i, padx=10, pady=(10,0))
        
        self.answer = customtkinter.CTkEntry(self, placeholder_text="Enter Answer here")
        self.answer.grid(row = 1, column=2, padx=10, pady=(10,0))
    
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

    def startGame(self):
        self.score = 0
        self.rounds = 5
        self.start = time.time()
        self.answer_button = customtkinter.CTkButton(self, text="Submit", command=self.submitAnswer)    
        self.answer_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.forgetCurrentGrid()
        values = getRandomValues()
        self.gameGrid = GameGrid(self, values)
        self.gameGrid.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew", columnspan=3)

    def showScore(self):
        user = self.username
        score = self.score
        time = self.end - self.start
        tk.messagebox.showinfo(title="Round complete", message=f"User {user} completed the test in {time} seconds and scored {score}")
        self = App()

    def submitAnswer(self):
        self.rounds -= 1
        useranswer = self.gameGrid.get()
        correctanswer = reduce(lambda x, y: x * y, self.gameGrid.values)
        if (useranswer.isdigit() and int(useranswer) == correctanswer):
            self.score += 1
        if (self.rounds > 0):
            newval = getRandomValues()
            self.gameGrid = GameGrid(self, getRandomValues())
            self.gameGrid.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew", columnspan=3)
        else:
            self.end = time.time()
            self.gameGrid.grid_remove()
            self.answer_button.grid_remove()
            self.showScore()
            self.myhelp.insertSinglePlayerGame(self.username, self.score, self.end - self.start)
            

    def login(self):
        values = self.loginFrame.get()
        self.username = values[0]
        self.password = values[1]
        self.myhelp = dbm.mysqlhelper()
        if self.myhelp.getUserIdFromuserName(self.username.strip()) > 0 and self.myhelp.getUserPasswordFromuserName(self.username.strip()) == self.password:
            self.showStartFrame()
        else:
            tk.messagebox.showerror(title="Login Failed", message="Check your login, or sign up")

    def register(self):
        values = self.loginFrame.get()
        self.username = values[0]
        self.password = values[1]
        self.myhelp = dbm.mysqlhelper()
        if self.myhelp.getUserIdFromuserName(self.username) < 0:
            self.myhelp.insertUser(self.username.strip(), self.password.strip())
        else:
            tk.messagebox.showerror(title="Register failed", message="username already exists in database")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
