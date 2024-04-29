import requests
import pandas as pd


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
    url = f"http://{host}:{port}/get-historical-data/{username}"
    print(url)
    response = requests.get(url)
    thing = str(response.json())
    print(thing)
    dty=["GameID", "Score", "time", "UserId", "OrderTimestamp"]
    df = pd.read_json(thing, orient='values')
    df.columns=dty
    print(df)
    df["OrderTimestamp"] = pd.to_datetime(df["OrderTimestamp"], unit='ms')
    return df

def main():
    resp = getHistoricalData("Peter")
    print(resp)

if __name__ == "__main__":
    main()

