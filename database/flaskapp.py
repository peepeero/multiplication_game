from flask import Flask, request, jsonify, Response
import random
from datetime import datetime
import my_db_manager
import pandas as pd

def getRandomValues():
   random.seed(datetime.now().timestamp())
   val1, val2, val3 = random.randint(0, 13), random.randint(0, 13), random.randint(0, 13) 
   return [val1, val2, val3]

def getRandomJointValues():
    random.seed(datetime.now().timestamp())
    delima = "h"
    store = []
    for i in range(5):
        thing = str(random.randint(0, 13)) + "z" + str(random.randint(0,13)) + "z" + str(random.randint(0,12))
        store.append(thing)
    return delima.join(store)

app = Flask(__name__)
dbman = my_db_manager.mysqlhelper()


@app.route("/")
def hello_world():
    return "Hello world"


@app.route("/get-login-info/<username>", methods=["GET"])
def get_login_info(username):
    if not request.method == "GET":
        return
    userid = dbman.getUserIdFromuserName(username)
    userpassword = dbman.getUserPasswordFromuserName(username)
    data = {
        "id" : userid,
        "password": userpassword
    }
    return jsonify(data), 201

@app.route("/insert-user/<username>/<password>", methods=["POST"])
def create_user(username, password):
    if not request.method == "POST":
        return
    dbman.insertUser(username, password)
    data = {
        "id" : username,
        "password": password
    }
    return jsonify(data), 201

@app.route("/starting-game/<username>", methods=["GET"])
def starting_game(username):
    print("it's looking for starting game")
    if not request.method == "GET":
        return
    firstGame = dbman.isFirstGame(username)
    print("was it the first game: ", firstGame)
    if firstGame:
        values = getRandomJointValues()
        dbman.insertFirstUserInfo(username, values)
        data = {
            "first" : firstGame,
            "values" : values
        }
        return jsonify(data), 201
    else:
        values = dbman.getLastValues()
        dbman.insertSecondUserInfo(username)
        data = {
            "first" : firstGame,
            "values" : values
        }
        return jsonify(data), 201
    
@app.route("/checkiftwo", methods=["GET"])
def check_if_two():
    two = dbman.checkIfTwo()
    data = {
        "two": two
    }
    return jsonify(data), 201

@app.route("/getmultiresults", methods=["GET"])
def get_multi_results():
    complete, value, user1username, user2username = dbman.get_multi_results()
    data = {
        "complete" : complete,
        "value": value,
        "user1username": user1username,
        "user2username": user2username
    }
    return jsonify(data), 201

@app.route("/insert-single-user-game/<username>/<score>/<time>", methods=["POST"])
def insert_single_user_game(username, score, time):
    if not request.method == "POST":
        return
    dbman.insertSinglePlayerGame(username, score, time)
    data = {
        "score" : username,
        "time": score
    }
    return jsonify(data), 201

@app.route("/insert-multi-user-game/<first>/<score>/<time>", methods=["POST"])
def insert_multi_player_game(first, score, time):
    if not request.method == "POST":
        return
    dbman.insertMultiPlayerGame(first, score, time)
    data = {
        "score" : score,
        "time": time
    }
    return jsonify(data), 201

@app.route("/get-historical-data/<username>", methods=["GET"])
def get_historical_data(username):
    df = dbman.getHistoricalData(username)
    print("did we at least get the dataframe")
    return Response(df.to_json(orient='values'), mimetype='application/json')

if __name__ == "__main__":
    app.run()

