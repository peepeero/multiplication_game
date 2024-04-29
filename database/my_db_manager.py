#!/usr/bin/python3
import mysql.connector
from subprocess import Popen, PIPE
import pandas as pd


class mysqlhelper:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="172.30.112.1", user="pierre", password="one piece")


    def createUserTable(self):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        tableString = "CREATE TABLE IF NOT EXISTS Users (Id int NOT NULL AUTO_INCREMENT, UserName VARCHAR(255) NOT NULL, UserPassword VARCHAR(255) NOT NULL, PRIMARY KEY (Id))"
        cursor.execute(tableString)

    def createGameTable(self):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        tableString = "CREATE TABLE IF NOT EXISTS SinglePlayerGames (GameID int NOT NULL AUTO_INCREMENT, UserID int NOT NULL, Score int NOT NULL, time double NOT NULL, GameTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (GameID), CONSTRAINT FK_realPerson FOREIGN KEY (UserID) REFERENCES Users(Id))"
        cursor.execute(tableString)

    def createMultiGameTable(self):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        tableString = "CREATE TABLE IF NOT EXISTS MultiPlayerGames (GameID int NOT NULL AUTO_INCREMENT, User1ID int, User2ID int, User1Score int, User2Score int, User1Time double, User2Time double, Vals VARCHAR(255), GameTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (GameID), CONSTRAINT FK1_realPerson FOREIGN KEY (User1ID) REFERENCES Users(Id), CONSTRAINT FK2_realPerson FOREIGN KEY (User2ID) REFERENCES Users(Id))"
        cursor.execute(tableString)
        print("it's worked")

    def getUserIdFromuserName(self, userName):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        cursor.execute(f'SELECT Id FROM users WHERE UserName = "{userName}"')
        value = cursor.fetchone()
        return value[0] if value is not None else -1

    def getUserPasswordFromuserName(self, userName):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        cursor.execute(f'SELECT UserPassword FROM users WHERE UserName = "{userName}"')
        value = cursor.fetchone()
        return value[0] if value is not None else "Error" 

    def insertUser(self, name, password):
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("USE multiplication_game")
        insert_stmt = (
                "INSERT INTO users (UserName, UserPassword)"
                "VALUES (%s, %s)"
        )
        data = (name, password)
        cursor.execute(insert_stmt, data)
        select_stmt = "SELECT * FROM users"
        cursor.execute(select_stmt)
        self.mydb.commit()


    def insertSinglePlayerGame(self, userName, score, timetaken):
        cursor = self.mydb.cursor()
        userid = self.getUserIdFromuserName(userName)
        cursor.execute("USE multiplication_game")
        insert_stmt = (
                "INSERT INTO singleplayergames (UserID, Score, time)"
                "VALUES (%s, %s, %s)"
        )
        data = (userid, score, timetaken)
        cursor.execute(insert_stmt, data)
        select_stmt = "SELECT * FROM singleplayergames"
        cursor.execute(select_stmt)
        cursor.reset()
        self.mydb.commit()

    def insertMultiPlayerGame(self, first, score, timetaken):
        cursor = self.mydb.cursor()
        print("Pierre this is the first value ", first, " and teh type is ", type(first))
        cursor.execute("USE multiplication_game")
        cursor.execute("SELECT * FROM multiplayergames ORDER BY GameID DESC LIMIT 1")
        gameID = cursor.fetchone()[0]
        data = (score, timetaken)
        if first == "True":
            cursor.execute(f'UPDATE multiplayergames SET User1Score = {score}, User1Time = {timetaken} WHERE GameID = {gameID}')
        else:
            cursor.execute(f'UPDATE multiplayergames SET User2Score = {score}, User2Time = {timetaken} WHERE GameID = {gameID}')
        select_stmt = "SELECT * FROM singleplayergames"
        cursor.reset()
        self.mydb.commit()


    def insertFirstUserInfo(self, username, values):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        id = self.getUserIdFromuserName(username)
        cursor.execute(f'INSERT into multiplayergames (User1ID, Vals) VALUES ({id}, "{values}")')
        self.mydb.commit()

    def insertSecondUserInfo(self, username):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        id = self.getUserIdFromuserName(username)
        cursor.execute("SELECT * FROM multiplayergames ORDER BY GameID DESC LIMIT 1")
        gameID = cursor.fetchone()[0]
        cursor.execute(f'UPDATE multiplayergames SET User2ID = "{id}" WHERE GameID = {gameID}')
        self.mydb.commit()

    def checkIfTwo(self):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        cursor.execute("SELECT * FROM multiplayergames ORDER BY GameID DESC LIMIT 1")
        value = cursor.fetchone()
        if (value[2] == None):
            return False
        else:
            return True

    def get_multi_results(self):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        cursor.execute("SELECT * FROM multiplayergames ORDER BY GameID DESC LIMIT 1")
        value = cursor.fetchone()
        user1ID = value[1]
        user2ID = value[2]
        cursor.execute(f'SELECT UserName FROM users WHERE Id = {user1ID}')
        user1Username = cursor.fetchone()[0]
        cursor.execute(f'SELECT UserName FROM users WHERE Id = {user2ID}')
        user2Username = cursor.fetchone()[0]
        if value[3] != None and value[4] != None:
            return True, value, user1Username, user2Username
        else:
            return False, value, user1Username, user2Username

    def isFirstGame(self, username):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        cursor.execute("SELECT * FROM multiplayergames ORDER BY GameID DESC LIMIT 1")
        value = cursor.fetchone()
        if (value[2] == None or value[1] == username):
            return False
        else:
            return True

    def getLastValues(self):
        cursor = self.mydb.cursor()
        cursor.execute("USE multiplication_game")
        cursor.execute("SELECT * FROM multiplayergames ORDER BY GameID DESC LIMIT 1")
        value = cursor.fetchone()
        return value[7]

    def initdatabase(self):
        cursor = self.mydb.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS multiplication_game')
        self.mydb = mysql.connector.connect(host="172.30.112.1", user="pierre", password="one piece", database="multiplication_game")
        self.createUserTable()
        self.createGameTable()
        self.createMultiGameTable()

    def getHistoricalData(username):
        return "thing"


def main():
    shelp = mysqlhelper()
    shelp.initdatabase()


if __name__ == "__main__":
    main()
