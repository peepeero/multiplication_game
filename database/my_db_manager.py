#!/usr/bin/python3
import mysql.connector
from subprocess import Popen, PIPE


class mysqlhelper:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="172.30.112.1", user="pierre", password="one piece")

        self.initdatabase()

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
        self.mydb.commit();


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
        self.mydb.commit();

    def initdatabase(self):
        cursor = self.mydb.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS multiplication_game')
        self.mydb = mysql.connector.connect(host="172.30.112.1", user="pierre", password="one piece", database="multiplication_game")
        self.createUserTable()
        self.createGameTable()

def main():
    shelp = mysqlhelper()


if __name__ == "__main__":
    main()
