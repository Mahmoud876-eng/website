from flask import Flask, render_template, request , session, redirect,jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from flask_session import Session
import asyncio
from telegram import Bot , Update
import variable
#from flask_talisman import Talisman
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address
import logging
uri = variable.password
app = Flask(__name__)
#https
#Talisman(app)
#DOS attack
#limiter = Limiter(
#    key_func=get_remote_address
#)
#limiter.init_app(app)
#sert secret key for session management
app.config["SECRET_KEY"] = "your_secret_key_here"
#session 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session = Session(app)
# Connect to MongoDB server
client = MongoClient(uri, server_api=ServerApi('1'))

# my database
db = client["user_database"]

#my collection collection
users_collection = db["users"]
medecine_collection= db["medicines"]
doctor_collection= db["doctor"]
patient_collection= db["patient"]
id_collection= db["id"]
rendezvous_collection= db["rendezvous"]
approved_collection=db["approved_rendez"]
secretary_collection= db["secretary"]

#bot data

TOKEN = variable.TOKEN
CHAT_ID = variable.CHAT_ID 
bot = Bot(token=TOKEN)
#attack
@app.errorhandler(429)
def ratelimit_error(e):
    app.logger.warning("Warning: A possible DoS attack detected! Rate limit exceeded.")  # More detailed warning 

@app.route('/')
#@limiter.limit("5 per minute")
def index():
    status= session.get("status")
    if status == "doctor":
        username = session.get("username")
        return render_template("home_doctor.html", username=username)
    elif status == "user":
        username = session.get("username")
        return render_template("home_user.html", username=username)
    else:
        return render_template('index.html')
@app.route("/register", methods=["POST","GET"] )#connect the test1.py and the flask here got an error when u click the button in the middle
#@limiter.limit("5 per minute")
def register():
    
    if request.method == "POST":
        email= request.json.get("email") 
        password=request.json.get("password")
        status= request.json.get("status")
        username=request.json.get("username")
        if not email:
            return jsonify({"error": "missing email"}), 400
        if not status:
            return jsonify({"error": "missing status"}), 400
        if not username:
            return jsonify({"error": "missing username"}), 400
        if not password:
            return jsonify({"error": "missing password"}), 400
        
        user_with_mail = users_collection.find_one({"email": email})
        doctor_with_mail = doctor_collection.find_one({"email": email})
        if user_with_mail or doctor_with_mail:
            return jsonify({"error": "email already exists"}), 400
        
        if len(password) < 8:
            return jsonify({"error": "password must be at least 8 characters"}), 400
    
        
        user_data = {
                "username": username,
                "email": email,
                "status":  status,
                "password": password
            }
        if status == "doctor":
            
            inserted_user = doctor_collection.insert_one(user_data)
            session["user_id"] = str(inserted_user.inserted_id)
            session["status"] = status
            return render_template("home_doctor.html",username=username)
        else:
            
            inserted_user = users_collection.insert_one(user_data)
            session["user_id"] = str(inserted_user.inserted_id)
            return render_template("home_user.html",username=username)
        # Insert user data into the collection with auto-generated ObjectId
        
         
    return render_template("register.html")
@app.route("/register/patient", methods=["POST","GET"] )
#@limiter.limit("5 per minute")
def register_paient():
    id= session.get("user_id")
    status= session.get("status")
    if request.method== "POST":
        name= request.form.get("name")
        age= request.form.get("age")
        gender= request.form.get("gender")
        date= request.form.get("date")
        phone= request.form.get("contact")
        notes= request.form.get("notes")
        #patient_with_phone= patient_collection.find_one({ "phone": phone})
        #if patient_with_phone:
        #    if status == "doctor":         
         #       print("patient with phone already exists")  
          #      print(patient_with_phone)
           #     updated_data = {"$set": {"dr_id": id}}
            #    update_result = patient_collection.update_one({"phone": phone}, updated_data) 
             #   print(update_result)
              #  return render_template("home_doctor.html")
        #    else:
         #       print("patient already exists")
          #      updated_data = {"$set": {"user_id": id}}
           #     update_result = patient_collection.update_one({"phone": phone}, updated_data)
            #    print(update_result)
            #   return render_template("home_user.html")
        id_with_phone= id_collection.find_one({ "number": phone})
        print(id_with_phone)
        if id_with_phone:
            if status == "doctor":
                print("patient with phone already exists")  
                print(id_with_phone)
                updated_data = {"$set": {"dr_id": id}}
                update_result = id_collection.update_one({"number": phone}, updated_data) 
                print(update_result)
                return render_template("home_doctor.html")
            else:
                print("patient already exists")
                updated_data = {"$set": {"user_id": id}}
                update_result = id_collection.update_one({"number": phone}, updated_data)
                print(update_result)
                return render_template("home_user.html")
        print("great")
        if status == "doctor":
            patient_data = {
               # "dr_id": id,
                #"user_id": "",
                "name": name,
                "age": age,
               "gender": gender,
                "date": date,
                "phone": phone,
                "notes": notes
            }
            inserted_patient = patient_collection.insert_one(patient_data)
           
        elif status == "user":
            patient_data = {
             #   "dr_id": "",
             #   "user_id":id,
                "name": name,
                "age": age,
               "gender": gender,
                "date": date,
                "phone": phone,
                "notes": notes
            }
            inserted_patient = patient_collection.insert_one(patient_data)
           

        if status == "doctor":    
            id_data = {
                "number": phone, 
                "dr_id": id,
                "user_id": ""
            }
            inserted_id = id_collection.insert_one(id_data)
            return render_template("home_doctor.html")
        else:
            id_data = {
                "number": phone,
                "dr_id": "",
                "user_id": id
            }
            inserted_id = id_collection.insert_one(id_data)
            return render_template("home_user.html")
        return render_template("error.html", message="missing data")
        
    return render_template("patient1.html")
@app.route("/login", methods=["POST","GET"] )
#@limiter.limit("5 per minute")
def login():
    print(request.method)
    if request.method == "POST":
        #get the data from json 
        mail = request.json.get("email")
        password = request.json.get("password")

        if not password or not mail:
            return jsonify({"error": "Missing data"}), 400
        
        user_with_mail = users_collection.find_one({"email": mail})
        doctor_with_mail = doctor_collection.find_one({"email": mail})
        secretary_with_mail=secretary_collection.find_one({"email": mail})

        if not user_with_mail and not doctor_with_mail and not secretary_with_mail:
            return jsonify({"error": "Wrong Password or email"}), 400
        print(secretary_with_mail)
        
        if user_with_mail:    
            if not user_with_mail['password'] == password:
                return jsonify({"error": "Wrong Password"}), 400
            session["user_id"] = user_with_mail['_id']
            session["status"] = user_with_mail['status']
            session["username"] = user_with_mail['username']
            return jsonify({"status": "user","username": user_with_mail['username']}), 200
            #return render_template("home_usr.html",username=user_with_mail['username'])

        elif doctor_with_mail:
            if not doctor_with_mail['password'] == password:
                return jsonify({"error": "Wrong Password or email"}), 400
            session["user_id"] = doctor_with_mail['_id']
            session["status"] = doctor_with_mail['status']
            session["username"] = doctor_with_mail['username']
            return jsonify({"status": "doctor","username": doctor_with_mail['username']}), 200
            #return render_template("home_doctor.html",username=doctor_with_mail['username'])
        elif secretary_with_mail:
            if not secretary_with_mail['password'] == password:
                return jsonify({"error": "Wrong Password or email"}), 400
            print("5")
            session["user_id"] = secretary_with_mail['doc_id']
            session["status"] = secretary_with_mail['status']
            session["username"] = secretary_with_mail['username']
            #return jsonify({"status": "secretary","username": secretary_with_mail['username']}), 200
            #return render_template("home_secratary.html",username=secretary_with_mail['username'])
            return redirect("/sec")
        else:
            return render_template("error.html", message="mail not found")     
    return render_template("login.html")

@app.route("/doctor", methods=["POST","GET"] )#u aded a rendez vous data base
def doctor():
    id= session.get("user_id")
    id_with_id = id_collection.find({ "dr_id": id })
    

    numbers = [str(doc['number']).strip() for doc in id_with_id]
    print(numbers)
    
    patient_with_number = patient_collection.find({ "phone": { "$in": numbers } })
    rendez_with_number = approved_collection.find({ "number": { "$in": numbers } })
    rendez=list(rendez_with_number)
    patients = list(patient_with_number)
    return render_template("doctor.html",patients=patients,rendezs=rendez)
@app.route("/view", methods=["POST","GET"] )
def view():
    
    id= session.get("user_id")
    
    id_with_id = id_collection.find({ "user_id": id })

    numbers = [str(doc['number']).strip() for doc in id_with_id]
    print(numbers)
    
    patient_with_number = patient_collection.find({ "phone": { "$in": numbers } })

    patients = list(patient_with_number)
    patient = [c['name'] for c in patients]
    
    print(patients)
    medecines = list(medecine_collection.find({ "patient": { "$in": patient } }))
    print(medecines)
    return render_template("view1.html",medecines=medecines, patients=patients)
@app.route("/insert", methods=["POST","GET"] )#it got implented into the data base butit doesn t go to the html
def insert():
    print(request.method)
    id= session.get("user_id")
    status= session.get("status")
    if request.method == "POST":
        
        user_with_mail = users_collection.find_one({"_id": id})
        doctor_with_mail = doctor_collection.find_one({"_id": id})
        print(doctor_with_mail)
        print(user_with_mail)
        patient=request.form.get("patient")
        name= request.form.get("medname") 
        if not patient_collection.find_one({ "name": patient }):
            return render_template("error.html", message="patient not found")
        if status == "doctor":
            patient_with_id= patient_collection.find_one({ "name": patient })
            number=patient_with_id['phone']
        elif status == "user":
            patient_with_id= patient_collection.find_one({ "name": patient })
            number=patient_with_id['phone']
        
        print(number) 
        
        print(request.method)
        print(name)
        if not name:
            return render_template("error.html", message="missing name")
        img=request.files.get("photo")#img I have got a prob can t put an img
        time=request.form.get("time")
        if not time:#I should creat that thing to only do mornning night
            return render_template("error.html", message="function not allowed")
        notes=request.form.get("notes", "there s no notes")
        rest= request.form.get("rest")
        medine_data = {
            "id": id,
            "patient": patient,
            "med_name": name,
            "img": img,
            "time": time,
            "notes": notes,
            "rest": rest
        }
        medecine_collection.insert_one(medine_data)
        if status == "doctor":
            return render_template("home_doctor.html",username=doctor_with_mail['username'])
        elif status == "user":
            return render_template("home_user.html",username=user_with_mail['username'])
        #elif if u want to add a rule for password
    if status=="doctor":
        id_with_doctor=id_collection.find({"dr_id": id})   
        
        numbers = [str(doc['number']).strip() for doc in id_with_doctor]
        patients=list(patient_collection.find({"phone": {"$in": numbers}}))
        
    if status=="user":
        id_with_doctor=id_collection.find({"user_id": id})   
        
        numbers = [str(doc['number']).strip() for doc in id_with_doctor]
        patients=list(patient_collection.find({"phone": {"$in": numbers}}))
        
    return render_template("insert.html")#,patients=patients)
@app.route("/update", methods=["POST","GET"] )#correct the css
def update():
    print(request.method)
    
    if request.method == "POST":
        id= session.get("user_id")
        print(id)
        name= request.form.get("med_name") 
        print(name)
        
        print(request.method)

        if not name:
            return render_template("error.html", message="write the name of the medecine")
        update_result= medecine_collection.find_one({ "id": id, "med_name": name}) #it give me null
        print(update_result)
        if not update_result:
            return render_template("error.html", message="medecine not found")
        
        img=request.form.get("photo")
        
        updated_data = {"$set": {"img": img}}
        update_result = medecine_collection.update_one({"id": id, "med_name": name}, updated_data) 

        
        
        time=request.form.get("time")
        
        updated_data = {"$set": {"time": time}}
        update_result = medecine_collection.update_one({"id": id, "med_name": name }, updated_data) 
        notes=request.form.get("notes")
        if not notes:
            updated_data = {"$set": {"notes": notes}}
            update_result = medecine_collection.update_one({"id": id, "med_name": name}, updated_data) 
        rest= request.form.get("rest")
        if not rest:
            updated_data = {"$set": {"rest": rest}}
            update_result = medecine_collection.update_one({"id": id, "med_name": name}, updated_data)
        if update_result.modified_count > 0:
            print("Update successful")
            return render_template("home_user.html")
        else:
            return render_template("error.html", message="update failed")
        
        
    return render_template("update.html")
@app.route("/delete", methods=["POST","GET"] )#U need to add the patient name
def delete():

    if request.method == "POST":
        id= session.get("user_id")
        name= request.form.get("med_name") #it gicves none
        status= session.get("status")
        print(id)
        print(name)        
        delete_result = medecine_collection.delete_one({"id": id, "med_name": name})
        if delete_result.deleted_count > 0:
            if session["status"] == "doctor":
                return render_template("home_doctor.html")
            else:
                return render_template("home_user.html")
        else:
            return render_template("error.html", message="medecine name not found")
    return render_template("delete.html")
app.route("/files", methods=["POST","GET"] )#have an error
def files():
    id= session.get("user_id")
    
    if request.method == "POST":
        name= request.form.get("medname") 
        file = request.files['file']
        #file.save(f"static/uploads/{file.filename}")
        return render_template("home_doctor.html")
    
    return render_template("files.html")
@app.route("/book_rendezvous", methods=["POST","GET"] )#u haven t tested it yet
def book_rendezvous():
    id= session.get("user_id")
    status= session.get("status")
    if request.method == "POST":
        name= request.form.get("name") 
        number= request.form.get("Number")
        print(number)
        numb_with_id= id_collection.find_one({ "number": number})
        print(numb_with_id)
        #numb_with_id=True
        if not numb_with_id:
            return render_template("error.html", message="wrong data")   
        doctor= request.form.get("doctor")
        print(doctor)
        doctor_with_id= doctor_collection.find_one({ "username": doctor})
        print(doctor_with_id)
        if not doctor_with_id:
            return render_template("error.html", message="Doctor not found")


        date= request.form.get("date")
        time= request.form.get("time")
        notes= request.form.get("notes")
        if not name:
            return render_template("error.html", message="missing name")
        if not date:
            return render_template("error.html", message="missing date")
        if not time:
            return render_template("error.html", message="missing time")
        
        rendezvous_data = {
            "id": doctor_with_id['_id'],
            "user_id": numb_with_id["user_id"],
            "name": name,
            "number": number,
            "doctor": doctor,
            "date": date,
            "time": time,
            "notes": notes        }
        rendezvous_collection.insert_one(rendezvous_data)
        
        if status == "doctor":
            return render_template("home_doctor.html",username=name)
        elif status == "user":
            return render_template("home_user.html",username=name)
    if status=="doctor":
        id_with_doctor=id_collection.find({"dr_id": id})   
        
        numbers = [str(doc['number']).strip() for doc in id_with_doctor]
        patients=list(patient_collection.find({"phone": {"$in": numbers}}))
        
    if status=="user":
        id_with_doctor=id_collection.find({"user_id": id})   
        
        numbers = [str(doc['number']).strip() for doc in id_with_doctor]
        patients=list(patient_collection.find({"phone": {"$in": numbers}}))
        
    
        
    return render_template("rendez_vous.html",patients=patients)
@app.route("/sec")#need work
def sec():
    username= session.get("username")
    return render_template("home_secratary.html",username=username)
@app.route("/register/sec", methods=["POST","GET"])#need work
def registersec():
    if request.method=="POST":
        id=session.get("user_id")
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        
        secretary_with_mail = secretary_collection.find_one({"email": email})
        
        if secretary_with_mail:
            return render_template("error.html",message="mail already used")
        
        if len(password) < 8:
            return render_template("error.html",message="shortpassword")
        
        secretary_data = {
                "username": username,
                "email": email,
                "status":  "doctor",
                "doc_id": id,
                "password": password
            }
        
            
        secretary_collection.insert_one(secretary_data)
        doc_id=doctor_collection.find_one({"_id": id})
        doc=doc_id["username"]
        print(doc)
        return render_template("home_doctor.html",username=doc)
    return render_template("registersect.html")
@app.route("/logout" )
def logout():
    print(request.method)
    session.clear()
    return redirect("/")
@app.route("/send_reminder", methods=["POST","GET"])#U can t seee her name when u return to herpy and pls make it s css and make him talk to one patient
async def send_reminder():
    value=session.get("cool")
    id=session.get("user_id") 
    if request.method=="POST":
        
        t=request.form.get("message")
        await bot.send_message(chat_id=CHAT_ID, text=t)
        if value:
            session["cool"]=""
            return redirect("/view/ren")
        return render_template("send.html",username=value)
    
    id_with_doctor=id_collection.find({"dr_id": id})   
        
    numbers = [str(doc['number']).strip() for doc in id_with_doctor]
    patients=list(patient_collection.find({"phone": {"$in": numbers}}))
     
    
    return render_template("send.html",patients=patients,username=value)
@app.route("/view/ren", methods=["POST","GET"])   
def view_ren():
    id=session.get("user_id")
    rendez_with_id=rendezvous_collection.find({"id": id})
    if request.method=="POST":
        name=request.form.get("action")
        nom=request.form.get("delete")
        print(nom)
        print(name)
        if name:#u need to delet in here 
            rendez_with_nom=rendezvous_collection.find_one({"_id": ObjectId(name)})
            rendezvous_data = {
            "id": rendez_with_nom["id"],
            "user_id": rendez_with_nom["user_id"],
            "name": rendez_with_nom["name"],
            "number": rendez_with_nom["number"],
            "doctor":rendez_with_nom["doctor"],
            "date": rendez_with_nom["date"],
            "time": rendez_with_nom["time"],
            "notes": rendez_with_nom["notes"]
            }
            approved_collection.insert_one(rendezvous_data)
        
            delete_result = rendezvous_collection.delete_one({"_id": ObjectId(name)})
            if delete_result.deleted_count > 0:
                print("deleted")
            return render_template("viewrendez.html",rendezs=rendez_with_id)
        if nom:
            delete_result = rendezvous_collection.delete_one({"name": nom})
            if delete_result.deleted_count > 0:
                print("deleted")
            session["cool"]=nom
            return redirect("/send_reminder")
            


    
    
    return render_template("viewrendez.html",rendezs=rendez_with_id)
@app.route("/rendez_vous/sec",methods=["POST","GET"])
def rendez_sec():
    id=session.get("user_id")
    doctor_with_id=doctor_collection.find_one({"_id": id})
    value=doctor_with_id["username"]
    if request.method=="POST":
        name= request.form.get("name") 
        number= request.form.get("Number")
        print(number)
        numb_with_id= id_collection.find_one({ "number": number})
        print(numb_with_id)
        #numb_with_id=True
        if not numb_with_id:
            return render_template("error.html", message="wrong data")   
        
        date= request.form.get("date")
        time= request.form.get("time")
        notes= request.form.get("notes")
        if not name:
            return render_template("error.html", message="missing name")
        if not date:
            return render_template("error.html", message="missing date")
        if not time:
            return render_template("error.html", message="missing time")
        
        rendezvous_data = {
            "id": doctor_with_id['_id'],
            "user_id": numb_with_id["user_id"],
            "name": name,
            "number": number,
            "doctor": value,
            "date": date,
            "time": time,
            "notes": notes        
        }
        rendezvous_collection.insert_one(rendezvous_data)
        return redirect("/sec")
        
        
    id_with_doctor=id_collection.find({"dr_id": id})   
        
    numbers = [str(doc['number']).strip() for doc in id_with_doctor]
    patients=list(patient_collection.find({"phone": {"$in": numbers}}))
     
    
    return render_template("rendez_vous.html",patients=patients,username=value)
@app.route("/delete/sec",methods=["POST","GET"])
def deletsec():#still not tested and there is no template for it
    id=session.get("user_id")
    secretaire_with_id=secretary_collection.find({"doc_id": id})
    if request.method=="POST":
        nom=request.form.get("name")
        delete_result = secretary_collection.delete_one({"name": nom})
        if delete_result.deleted_count > 0:
            print("deleted")
    sect=list(secretaire_with_id)
    return render_template("delsec.html",user=sect)
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)
    #app.run(ssl_context='adhoc', debug=True)