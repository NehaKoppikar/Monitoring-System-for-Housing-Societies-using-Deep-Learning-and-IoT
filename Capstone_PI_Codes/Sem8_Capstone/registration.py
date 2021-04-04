import streamlit as st
import cv2
from imutils.video import VideoStream
import pandas as pd
import time
from pymongo import MongoClient
import os
import datetime
from skimage import io


################ Database - MongoDB #####################
@st.cache(hash_funcs={MongoClient: id})
def get_client():
    return MongoClient("mongodb://localhost:27017/")

# Connect to client
client = get_client()

# Connect to DB
db = client.get_database('registration')

# Get the particular collection that contains the data
records = db.register

###############################################3

# @st.cache(allow_output_mutation=True)
# def get_data():
#     return []

# Taking Input from the front-end
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
option = st.radio(
    "What category do you see yourself most fit in?",
    ('Resident', 'Non-Resident', 'Frequenter'))

if option == 'Resident':
    st.write('You selected Resident.')
elif option == "Non-Resident":
    st.write('You selected Non-Resident.')
else:
    st.write("You didn't select comedy.")

user_found = records.find_one({'First Name': first_name, 'Last Name': last_name})
if user_found:
    st.write('There already is a record by that name')

# Add Non-Face (non-image) Data to the database
if st.button("Add row"):
    user_input = {'First Name': first_name, 'Last Name': last_name, 'category': option, 'date': datetime.datetime.today().strftime("%d %B, %Y") , "time": datetime.datetime.now().strftime("%H:%M:%S")}
    #insert it in the record collection
    records.insert_one(user_input)
    #get_data().append({"First Name": first_name, "Last Name":last_name})

#st.write(pd.DataFrame(get_data()[-1]))

@st.cache()
def get_data():
    all_records_df = pd.DataFrame.from_records(records.find())
    return all_records_df

df = pd.DataFrame(get_data())
# df.to_csv("Data.csv")

# Make directory
time.sleep(6)
parent_directory = "images"
directory = f"{first_name}_{last_name}"
# mode 
mode = 0o666
path = os.path.join(parent_directory, directory)
os.mkdir(path, mode)

# load OpenCV's Haar cascade for face detection from disk
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Extracting face
def face_extractor(img):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns the input image
    
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(img, 1.3, 5)
    
    if faces is ():
        return None
    
    # Crop all faces found
    for (x,y,w,h) in faces:
        x=x-10
        y=y-10
        cropped_face = img[y:y+h+50, x:x+w+50]

    return cropped_face

# initialize the video stream
"[INFO] starting video stream..."


@st.cache(allow_output_mutation=True)
def get_cap():
    return VideoStream(usePiCamera=1)

cap = get_cap()
count = 0

frameST = st.empty()


# loop over the frames from the video stream
while True:
    
        #ret, frame = cap.read()
        frame = cap.read()
        cv2.imwrite(f'../images/{first_name}_{last_name}/{count}.jpg', frame) # store images in file path 
        #orig = frame.copy()
        #io.imwrite(f'images/{first_name}_{last_name}/{count}.jpg', frame) # store image
        #orig = frame.copy()

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor = 1.1, 
            minNeighbors=5, minSize=(30, 30))

        if face_extractor(frame) is not None:
            count += 1
            
        if count==10:
            st.text('Collected 10 images')
            break



        # show the output frame
        frameST.image(frame, channels="BGR")