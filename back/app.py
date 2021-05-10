from flask import Flask, redirect, url_for, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from PIL import Image, ImageTk
import numpy as np
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
presence= db.presence

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font= cv2.FONT_HERSHEY_SIMPLEX
count=0


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

@app.route('/update', methods=['POST'])
def update():
    emp_json_list= request.get_json()
    if not emp_json_list:
        return jsonify({'response': 'error'})
    
    else:
        emp_json= emp_json_list[0]
        email= emp_json.get('email')
        matr= emp_json.get('matricules')
        nom= emp_json.get('nom')
        prenom= emp_json.get('prenom')

        try:
            employee.update(
                {"matricules": matr},
                {"matricules":matr, "email": email, "nom": nom, "prenom": prenom}
                )
        except:
            print('An exception occured')
        
        # print(emp_json[0]['matricules'])
        # response= emp_json[0]
        # email= response.get('matricules')
        return jsonify({'response': 'success'})

@app.route('/delete', methods=['GET'])
def delete():
    # image.drop()
    # employee.drop()
    image.drop()
    employee.drop()
    presence.drop()
    return jsonify({'response': 'true'})


@app.route('/getOneEmployee/<matricules>', methods=['GET'])
def getEmployee(matricules):
    empl= []
    print(matricules)
    for emp in employee.find({"matricules": matricules}):
        empl.append({"nom": emp['nom'],"prenom":emp["prenom"], "email": emp['email'], "matricules": emp['matricules']})
    return jsonify([empl])

@app.route('/getAllEmployee', methods=['GET'])
def getAllEmployee():
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

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    nbImg = 0
    nbEmployee= employee.find({}).count()
    nbEmployee+=1
    employee.insert({"matricules": matricules, "nom": nom.lower(), "prenom": prenom, "email": email, "id":nbEmployee, "image": ""})

    # getName= pd.read_csv('UserDetails/userdetails.csv')
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
            nbImg += 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite("img.jpg", img[y:y+ h, x:x+w])
            filename= "img.jpg"
            try:
                with open(filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
               
                if employee.find({"matricules": matricules}):
                    for emp in employee.find({"matricules": matricules}):
                        id= emp['id']
                        print(id)

                image.insert({"image":encoded_string, "matricules": matricules, "id":id })
                print(matricules)
            except e:
                print('An exception occured')
                print(e)
            
        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
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

            name="img_new"
            cv2.imwrite("images/" + name + ".jpg",
                         img[y:y + h, x:x + w])
            
            filename= "images/img_new.jpg"
            try:
                with open(filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
               

                employee.update(
                        {"matricules": matricules},
                        {"matricules": matricules, "nom": nom.lower(), "prenom": prenom, "email": email, "id":nbEmployee, "image":encoded_string }
                    )
                # print(matricules)
            except e:
                print('An exception occured')
                print(e)

 


    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    return jsonify({'answers': 'ok'})

def updateTrainFace():
    faces, ids= getImage()
    recognizer= cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))

    recognizer.write('trainer/trainer.yml')
    return jsonify({'response': 'ok'})

def getImage():
    ids= []
    facesamples= []
    data = image.find({})
    for img in image.find({}):
        # decoded_image= img['image'].decode()
        # print(decoded_image)
        converted_string= img['image']
        id= img['id']
    # img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decoded_image)

    # return jsonify({'imageTag': img_tag})
        with open('encode.bin', 'wb') as file:
            file.write(converted_string)

        file= open('encode.bin', 'rb')
        byte= file.read()
        file.close()

        decodeit = open('hello_level.jpg', 'wb')
        decodeit.write(base64.b64decode((byte)))
        decodeit.close()

        PIL_img= Image.open('hello_level.jpg').convert('L')
        img_numpy= np.array(PIL_img, 'uint8')
        #matricule= matricules
        faces= faceCascade.detectMultiScale(img_numpy)
        for(x, y, w,h) in faces:
            facesamples.append(img_numpy[y: y+h, x:x +w])
            ids.append(id)
    
    return facesamples, ids

@app.route('/countEmployee', methods=['GET'])
def countEmployee():
    nbEmployee= employee.find({}).count()
    
    if nbEmployee == 0:
        json_response= jsonify({'employee': 'zero'})
    else:
        json_response= jsonify({'employee': 'no zero'})
    return json_response

@app.route('/findAllPresence', methods=['GET'])
def findAll():
    all_presence=[]
    if(presence.find({})):
        for pre in presence.find().limit(3):
            ids= pre['id_emp']
            print(ids)
            if employee.find({'id': ids}):
                for emp in employee.find({'id': ids}):
                    all_presence.append({'matricules': emp['matricules'], 'nom': emp['nom'], 'prenom': emp['prenom'], 'email': emp['email']})
    return jsonify([all_presence])
    
@app.route('/recognition', methods=['GET'])
def recognition():
    presence_emp=[]
    idEmp= 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    # iniciate id counter
    #id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    # names = ['None', 'Marcelo', 'Paula', 'Ilza', 'Z', 'W']

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    # getName= pd.read_csv('UserDetails/userdetails.csv')
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

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                # aa= getName.loc[getName['face_id']==id]['Name'].values
                # tt= str(id)+"-"+aa
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
            idEmp=id

        if(presence.find_one({'id_emp': idEmp})):
            print('I\'m here so you got error')
            # for pre in presence.find({'id': 2}):
            #     print(pre['id_emp'])
        
        else:
            try:
                presence.insert({'id': 2, 'id_emp': idEmp})
            except e:
                print(e)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

    #list= listeEmployee()
    return jsonify({'response': 'success'})

if __name__ == "__main__":
    app.run(debug=True)