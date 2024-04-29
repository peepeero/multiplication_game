import requests

host="localhost"
port="5000"

def get_user_info(username):
    url = f"http://{host}:{port}/get-login-info/{username}"
    response = requests.get(url)
    return response.json()

def insert_user(username, password):
    url = f"http://{host}:{port}/insert-user/{username}/{password}"
    response = requests.post(url)
    return response.json()

def initial_start_game(username):
    url = f"http://{host}:{port}/starting-game/{username}"
    response = requests.get(url)
    return response.json()

def check_if_two_users():
    url = f"http://{host}:{port}/checkiftwo"
    response = requests.get(url)
    return response.json()

def get_multi_results():
    url = f"http://{host}:{port}/getmultiresults"
    response = requests.get(url)
    return response.json()

def insertSinglePlayerGame(username, score, time):
    url = f"http://{host}:{port}/insert-single-user-game/{username}/{score}/{time}"
    response = requests.post(url)
    return response.json()

def insertMultiPlayerGame(first, score, time):
    url = f"http://{host}:{port}/insert-multi-user-game/{first}/{score}/{time}"
    response = requests.post(url)
    return response.json()

def getHistoricalData(username):
    url = f"http://{host}:{port}/get-historical-data/{username}/"
    response = requests.get(url)
    return response.json()

