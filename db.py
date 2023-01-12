import mysql.connector as mysql
import requests
import random
import os
from utils import randomDateGenerator
db = mysql.connect(host="127.0.0.1",
                   user="root",
                   passwd="root",
                   port=3306,
                   database="main_test",
                   auth_plugin='mysql_native_password')
cur = db.cursor()


def initialize_db():
    cur.execute("CREATE DATABASE main_test")
    cur.execute("USE main_test")
    cur.execute(
        "CREATE TABLE users_attendance(name VARCHAR(225),date DATE, status BOOL)")
    db.commit()

    os.mkdir("out")
    print("Database Initialized Successfully ✅")


def addAttendance(name, date, status):
    cur.execute(
        f"INSERT INTO users_attendance VALUES('{name}','{date}','{0 if status == False else 1}')")


def getAttendances():
    cur.execute("SELECT * FROM users_attendance")
    data = cur.fetchall()
    return data


def getAttendancesForSpecificDate(date):
    cur.execute(
        f"SELECT * FROM users_attendance WHERE date  BETWEEN '{date}' AND '{date}'")
    return cur.fetchall()


def generateDemoData():
    n = 100
    req = requests.get(f"https://randomuser.me/api/?results={n}&nat=US")
    data = req.json()["results"]
    for num, i in enumerate(data):
        name = f"{i['name']['first']} {i['name']['last']}"
        for j in range(1):
            date = randomDateGenerator()
            status = random.choice([True, False])
            addAttendance(name, date, status)
    db.commit()
    print("Generated Demo Data ✔")
