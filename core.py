import numpy as np
import cv2
import face_recognition
import pickle
import random
import string
import pyttsx3
import emoji
import csv
from vars import *
from db import *


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def speak(text: str):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    finally:
        pass


def getUsers():
    with open(databaseFileName, "r+b") as f:
        if len(f.read()) == 0:
            return []
        f.seek(0)
        users = pickle.load(f)
    return users


def displayUsers():
    print("-"*40)
    users = getUsers()
    n = 1
    print("ID \t Name")
    for user in users:
        print(f"{n} \t {user[0]}")
        n += 1
    print("-"*40)


def deleteUser():
    print(hyfmt)
    try:
        displayUsers()
        n = int(input("Enter the ID of the user you want to delete: "))
        users = getUsers()
        users.pop(n-1)
        with open(databaseFileName, "wb") as f:
            pickle.dump(users, f)
        print(f"User with ID {n} has been deleted successfully ✔")
    except Exception as e:
        print("There was an error deleting the user: ", e)
    print(hyfmt)


def getUserEncodings():
    users = getUsers()
    return [user[1] for user in users]


def findUserUsingEncodings(encodings):
    users = getUsers()
    for user in users:
        # print(user)
        if np.array_equal(user[1], encodings):
            return user
    return None


def newUser():
    try:
        userID = randomString()
        name = input("Enter Your Name: ")
        while True:
            print(emoji.emojize(
                "*"*10+" Please look at the camera :video_camera: "+"*"*10))
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()
            cv2.imwrite(f"images/{userID}.jpg", frame)
            video_capture.release()
            cv2.destroyAllWindows()
            image = face_recognition.load_image_file(f"images/{userID}.jpg")
            face_encoding = face_recognition.face_encodings(image)
            if len(face_encoding) == 0:
                print("No face detected, please try again")
                continue
            users = getUsers()
            # print(users)
            users.append([name, face_encoding[0]])
            with open(databaseFileName, "wb") as f:
                pickle.dump(users, f)
            break
        print(emoji.emojize(
            name+" has been added successfully ✔"))
    except Exception as e:
        print(e)
        print("Error: ", e)


def getUserInfo():
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    ret, frame = video_capture.read()
    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)
        face_names = []
        known_face_encodings = getUserEncodings()
        name = "unknown"
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = findUserUsingEncodings(
                    known_face_encodings[best_match_index])[0]
            face_names.append(name)
    process_this_frame = not process_this_frame
    video_capture.release()
    return face_names


def testFace():
    print(hyfmt)
    if getUsers() == []:
        print("No users found. Please add a user first.")
        print(hyfmt)
        return
    print("Looking for faces...")
    face_names = ["Raghav"]
    if len(face_names) == 0:
        print("No face detected")
    else:
        for i in face_names:
            print("Face detected: ", i)
            if i == "unknown":
                print("Unknown face detected")
    print(hyfmt)


def get_Users():
    data = getAttendances()
    users = []
    for i in data:
        if i[0] not in users:
            users.append(i[0])
    return list(set(users))


def generateAttendanceData():
    data = getAttendances()
    users = get_Users()
    finData = []
    dates = []
    for i in data:
        dates.append(str(i[1]))
    dates = list(set(dates))
    dates.sort()
    headers = ["Name"]
    # print(len(dates))
    for date in dates:
        headers.append(date)
    finData.append(headers)
    # print(len(finData[0]))
    for user in users:
        userData = [user]
        userAttendances = []
        for i in data:
            if user == i[0]:
                userAttendances.append(i)
        for i in userAttendances:
            for x in dates:
                d = "A"
                if str(x) == str(i[1]):
                    d = "P"
                userData.append(d)
        finData.append(userData)
    return finData


def showAttendance():
    # print(hyfmt)
    data = generateAttendanceData()
    if data == []:
        print("No attendence data found")
    else:
        with open("out/output.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(data)
    print("Successfully Exported Attendance Data To 'out/output.csv' :)")
    # print(hyfmt)
