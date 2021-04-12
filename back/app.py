from flask import Flask, redirect, url_for, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json
# import pyodbc
import cv2
import base64

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#db config
client = MongoClient('mongodb://127.0.0.1:27017')

db= client.mvt2
admin= db.admin
employee= db.employee
image= db.image

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font= cv2.FONT_HERSHEY_SIMPLEX
count=0

user= db.user
@app.route('/signin', methods=['POST'])
def signin():
    login_json= request.get_json() # si l app n a pas recu des donnees
    if not login_json:
        return jsonify({'msg': 'error'})

    else:
        email= login_json.get('email')
        password= login_json.get('password')
        print(email)
        print(password)

        if admin.find_one({"email": email, "password": password}):
            return jsonify({'msg': 'success'})    
        else:
            return jsonify({'msg': 'error'}) 

        return jsonify({'msg': 'success'})

@app.route('/delete', methods=['GET'])
def delete():
    image.drop()
    employee.drop()
    return jsonify({'response': 'true'})



@app.route('/getAllEmployee', methods=['GET'])
def getEmployee():
    allEmployee= []
    if employee.find({}):
        for empl in employee.find({}).sort('matricules'):
            allEmployee.append({"matricules": empl['matricules'], "nom": empl['nom'], "prenom": empl['prenom'], "email": empl['email']})
    
    return jsonify([allEmployee])

@app.route('/addOneImage', methods=['GET'])
def addOneImage():
    filename= "img.jpg"
    matricules="M03"
    try:
        with open(filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        image.insert({"image":encoded_string, "matricules": matricules})
        print(matricules)
    except e:
        print('An exception occured')
        print(e)
        
    return jsonify({"response": "success"})

@app.route('/webcam', methods=['POST'])
def launchWebcam():
    employee_json= request.get_json()

    nom= employee_json.get('nom')
    prenom= employee_json.get('prenom')
    email= employee_json.get('email')
    matricules= employee_json.get('matricules')

    count = 1
    print(count)
    id = count
    cam = cv2.VideoCapture(0)
    cam.set(3, 1000)  # set video widht
    cam.set(4, 900)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    nbImg = 0
    while True:
        ret, img = cam.read()
        # img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        for (x, y, w, h) in faces:
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            nbImg += 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite("img.jpg", img[y:y+ h, x:x+w])
            filename= "img.jpg"
            try:
                with open(filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())

                image.insert({"image":encoded_string, "matricules": matricules})
                print(matricules)
            except e:
                print('An exception occured')
                print(e)

           
            # name="Karin"
            # cv2.imwrite("images/" + name + "." + str(nbImg) + ".jpg",
            #             gray[y:y + h, x:x + w])

    
            # cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        elif nbImg >= 30:  # Take 30 face sample and stop video
            break

        faces_imgsave = faceCascade.detectMultiScale(
        img,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces_imgsave:

            name="Karin_imgsave"
            cv2.imwrite("images/" + name + ".jpg",
                         img[y:y + h, x:x + w])
 
            cv2.imshow('image', img)
           
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

    employee.insert({"matricules": matricules, "nom": nom.lower(), "prenom": prenom, "email": email})

    return jsonify({'answers': 'ok'})

def updateTrainFace():
    data= image.find({})
    for img in image.find({}):
        pass
        #convert a binary image into png in python


if __name__ == "__main__":
    app.run(debug=True)