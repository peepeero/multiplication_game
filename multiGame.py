#!/usr/bin/python3
import random
from database import my_db_manager as dbm
from datetime import datetime
import time

def getRandomValues():
   random.seed(datetime.now().timestamp())
   val1, val2, val3 = random.randint(0, 13), random.randint(0, 13), random.randint(0, 13) 
   return val1, val2, val3

def main():
    score = 0;
    rounds = 5;
    start = time.time();
    for i in range(rounds):
        val1, val2, val3 = getRandomValues()
        print(f"Numbers: {val1} {val2} {val3}")
        answer = int(input("Enter the answer: "))
        score = score + 1 if (val1 + val2 + val3) == answer else score
    end = time.time();
    myhelp = dbm.mysqlhelper()
    myhelp.insertSinglePlayerGame("Peter", score, end - start)
    print(f"It took you {end - start} seconds to score {score}/{rounds}")
    
if __name__ == "__main__":
    main()
