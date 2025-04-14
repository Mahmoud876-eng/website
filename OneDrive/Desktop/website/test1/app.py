from flask import Flask, render_template, request , session, redirect
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from flask_session import Session
import variable

uri = variable.password
app = Flask(__name__)
#sert secret key for session management
app.config["SECRET_KEY"] = "your_secret_key_here"
#session 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session = Session(app)
# Connect to MongoDB server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a database
db = client["user_database"]

# Create a collection
users_collection = db["users"]
medecine_collection= db["medicines"]
doctor_collection= db["doctor"]
patient_collection= db["patient"]
id_collection= db["id"]



@app.route('/')
def index():
    status= session.get("status")
    if status == "doctor":
        return render_template("home_doctor.html")
    elif status == "user":
        return render_template("home_user.html")
    else:
        return render_template('index.html')
@app.route("/register", methods=["POST","GET"] )#connect the test1.py and the flask here got an error when u click the button in the middle
def register():
    print(request.method)
    
    if request.method == "POST":
        mail= request.form.get("mail") 
        user_with_mail = users_collection.find_one({"email": mail})
        doctor_with_mail = doctor_collection.find_one({"email": mail})
        if user_with_mail or doctor_with_mail:
            return render_template("error.html", message="mail already exists")
        status= request.form.get("status")
        username=request.form.get("username")
        
        if not username:
            return render_template("error.html", message="missing name")
        password=request.form.get("password")
        if not password:
            return render_template("error.html", message="missing password")
        if len(password) < 8:
            return render_template("error.html", message="password too short")
    
        
        user_data = {
                "username": username,
                "email": mail,
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
def login():
    print(request.method)
    if request.method == "POST":
        mail= request.form.get("mail") 
        print(request.method)
        print(mail)

        print("6")
        user_with_mail = users_collection.find_one({"email": mail})
        doctor_with_mail = doctor_collection.find_one({"email": mail})
        if not user_with_mail and not doctor_with_mail:
            return render_template("error.html", message="mail not found")
        username=request.form.get("name")
        if user_with_mail:    
            if not user_with_mail['username'] == username:
                return render_template("error.html", message="name not found")
            password=request.form.get("pass")
            if not password:
                return render_template("error.html", message="missing password")
            if not user_with_mail['password'] == password:
                return render_template("error.html", message="password not found")
            session["user_id"] = user_with_mail['_id']
            session["status"] = user_with_mail['status']
            return render_template("home_user.html",username=user_with_mail['username']) 
        
        elif doctor_with_mail:
            if not doctor_with_mail['username'] == username:
                return render_template("error.html", message="name not found")
            password=request.form.get("pass")
            if not password:
                return render_template("error.html", message="missing password")
            if not doctor_with_mail['password'] == password:
                return render_template("error.html", message="password not found")
            session["user_id"] = doctor_with_mail['_id']
            session["status"] = doctor_with_mail['status']
            return render_template("home_doctor.html",username=doctor_with_mail['username'])
        else:
            return render_template("error.html", message="mail not found")     
    return render_template("login.html")

@app.route("/doctor", methods=["POST","GET"] )
def doctor():
    id= session.get("user_id")
    id_with_id = id_collection.find({ "dr_id": id })

    numbers = [str(doc['number']).strip() for doc in id_with_id]
    print(numbers)
    
    patient_with_number = patient_collection.find({ "phone": { "$in": numbers } })

    patients = list(patient_with_number)
    return render_template("doctor.html",patients=patients)
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
    
    if request.method == "POST":
        id= session.get("user_id")
        status= session.get("status")
        user_with_mail = users_collection.find_one({"-id": id})
        doctor_with_mail = doctor_collection.find_one({"-id": id})
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
        
    return render_template("insert.html")
@app.route("/update", methods=["POST","GET"] )
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
@app.route("/delete", methods=["POST","GET"] )#have an error not sure if it s fixed pls test it
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
@app.route("/logout" )
def logout():
    print(request.method)
    session.clear()
    return redirect("/")

    
if __name__ == '__main__':
    app.run(debug=True)