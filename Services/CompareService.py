from .ImageService import load_image_file
import cv2
#import numpy as np
import face_recognition

class CompareImg:
    def compare(self, mainImage = 'image/_ASHU.jpg', newImage = 'image/ASHU.jpg'):
        # Subject image to be fetched from DB linked with card
        imgSubject = load_image_file(mainImage)
        imgSubject = cv2.cvtColor(imgSubject,cv2.COLOR_BGR2RGB)

        # Image recieved from Frontend (image undergoing examiation)
        # for this PBL review it is currently asking fixed absolute path
        # in the next review, we will be able to make use of live image captured 
        imgSubjectTest = load_image_file(newImage)
        imgSubjectTest = cv2.cvtColor(imgSubjectTest,cv2.COLOR_BGR2RGB)

        try:
            faceLoc = face_recognition.face_locations(imgSubject)[0]
            encodeSubject = face_recognition.face_encodings(imgSubject)[0]
            cv2.rectangle(imgSubject,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
 
            faceLocTest = face_recognition.face_locations(imgSubjectTest)[0]
            encodeSubjectTest = face_recognition.face_encodings(imgSubjectTest)[0]
            cv2.rectangle(imgSubjectTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
 
            # results = face_recognition.compare_faces([encodeSubject],encodeSubjectTest)
            faceDis = face_recognition.face_distance([encodeSubject],encodeSubjectTest)

            print(faceDis)
            return faceDis

        except IndexError:
            raise RuntimeError('[Error] Coudn\'t find face in one of Images.')