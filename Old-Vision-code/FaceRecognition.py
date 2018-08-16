
# Face Recognition with OpenCV
#
# Uses the files created by FaceRecognitionTraining.py 

#import OpenCV module
import cv2
#import os module for reading training data directories and paths
import os
#import numpy it is needed by OpenCV face recognizers
import numpy as np
import pickle

# Load the data created in training
faces = np.load('faces-data/faces.npy')
labels = np.load('faces-data/labels.npy')

# Load the subject names
with open ('faces-data/names', 'rb') as fp:
    subjects = pickle.load(fp)

# ### Train Face Recognizer

#create our LBPH face recognizer 
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

#or use EigenFaceRecognizer by replacing above line with 
#face_recognizer = cv2.face.EigenFaceRecognizer_create()

#or use FisherFaceRecognizer by replacing above line with 
#face_recognizer = cv2.face.FisherFaceRecognizer_create()


# Now that we have initialized our face recognizer we can give it the data 
face_recognizer.train(faces, labels)

#function to draw rectangle on image 
#according to given (x, y) coordinates and 
#given width and heigh
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
#function to draw text on give image starting from
#passed (x, y) coordinates. 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

# This function detects a face using OpenCV from the supplied image
def detect_face(img):
    face_data = []
    
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow Haar classifier
    face_cascade = cv2.CascadeClassifier('opencv-files/haarcascade_frontalface_alt.xml')

    #let's detect multiscale (some images may be closer to camera than others) images
    #result is a list of faces
    faces_detected = face_cascade.detectMultiScale(gray, 1.1, 5);
    
    #if no faces are detected then return None
    if (len(faces_detected) == 0):
        return None, None
    
    #under the assumption that there will be only one face in each training image
    #extract the face area from 
    (x, y, w, h) = faces_detected[0]
    
    #return only the face part of the image
    for face in faces_detected:
        (x, y, w, h) = face
        face_data.append(gray[y:y+w, x:x+h])

    # faces_detected is an array of rectangles where faces have been detected.
    # face_data is an array of the data for the faces detected
    
    return face_data, faces_detected

# Next is a function called by another model when it wants to check for a face
# This function recognizes the person in image passed
# and draws a rectangle around detected face with name of the 
# subject
def predict(test_img):
    #make a copy of the image as we don't want to change original image
    img = test_img.copy()
    #detect face from the image
    faces, rects = detect_face(img)
    
    if(faces != None):
        for index in range(len(faces)):
            #predict the image using our face recognizer 
            label, confidence = face_recognizer.predict(faces[index])
            
            #get name of respective label returned by face recognizer
            label_text = subjects[label]
    
            #draw a rectangle around face detected
            draw_rectangle(img, rects[index])
            #draw name of predicted person
            draw_text(img, label_text, rects[index,0], rects[index,1]-5)
            
    else:
        print("NONE")
    
    return img








