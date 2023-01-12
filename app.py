import numpy as np
import speech_recognition as sr
import cv2
import face_recognition
from datetime import datetime
from core import *
from db import *
from vars import *
from art import text2art


def startBot():
    print(hyfmt)
    print("🤖 Bot staring... ")

    if getUsers() == []:
        print("No users found. Please add a user first.")
        print(hyfmt)
        return
    # startMonitoring()
    name = "Raghav"
    print(f"Added Attendance for {name}")

    print(hyfmt)


def startMonitoring():
    video_capture = cv2.VideoCapture(0)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
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

                if name != "unknown":
                    alreadyLogged = False
                    todayUsers = getAttendancesForSpecificDate(
                        datetime.now().strftime('%Y-%m-%d'))
                    for i in todayUsers:
                        if i[0].lower() == name.lower():
                            alreadyLogged = True
                    if not alreadyLogged:
                        # print(f"Adding Attendance for {name}")
                        addAttendance(name, datetime.now(), True)
                        db.commit()
                        print(f"Added Attendance for {name}")
                    else:
                        pass
                        # print("User Already logged")

                name = "unknown"

        process_this_frame = not process_this_frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()


r = sr.Recognizer()
if __name__ == "__main__":
    print(text2art("Attendance Bot "))
    while True:
        print("1. Initialize DB \n2. Generate Demo Data \n3. Get Attendances \n4. Start Monitoring \n5. Add User \n6. Show Users \n7. Test User \n8. Exit")
        choice = input("Enter Your Choice: ")
        if choice == "1":
            initialize_db()
        elif choice == "2":
            generateDemoData()
        elif choice == "3":
            showAttendance()
        elif choice == "4":
            startBot()
        elif choice == "5":
            newUser()
        elif choice == "6":
            displayUsers()
        elif choice == "7":
            testFace()
        elif choice == "8":
            print(text2art("Good Bye!"))
            break
        else:
            print("Invalid Choice! \n")
        print("\n")
