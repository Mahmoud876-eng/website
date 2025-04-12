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
user_collection= db["medicines"]



@app.route('/')
def index():
    return render_template('index.html')
@app.route("/register", methods=["POST","GET"] )
def register():
    print(request.method)
    
    if request.method == "POST":
        mail= request.form.get("mail") 
        print(request.method)
        print(mail)
        if not mail:
            print("5")
            return render_template("error.html", message="missing mail")
        if not mail.endswith("@gmail.com"):
            return render_template("error.html", message="missing @gmail.com")
        print("6")
        status= request.form.get("status")
        username=request.form.get("username")
        print(username)
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
            "status": status,
            "password": password
        }
        # Insert user data into the collection with auto-generated ObjectId
        inserted_user = users_collection.insert_one(user_data)
        session["user_id"] = str(inserted_user.inserted_id)
        print(session.get("user_id"))
        #elif if u want to add a rule for password
        return render_template("view.html") 
    return render_template("register.html")
@app.route("/login", methods=["POST","GET"] )
def login():
    print(request.method)
    if request.method == "POST":
        mail= request.form.get("mail") 
        print(request.method)
        print(mail)
        if not mail:
            return render_template("error.html", message="missing mail")
        if not mail.endswith("@gmail.com"):
            return render_template("error.html", message="missing @gmail.com")
        print("6")
        user_with_mail = users_collection.find_one({"email": mail})
        if not user_with_mail:
            return render_template("error.html", message="mail not found")
        username=request.form.get("name")
        if not user_with_mail['username'] == username:
            return render_template("error.html", message="name not found")
        password=request.form.get("pass")
        if not password:
            return render_template("error.html", message="missing password")
        if not user_with_mail['password'] == password:
            return render_template("error.html", message="password not found")
        session["user_id"] = user_with_mail['_id']  
        print(session.get("user_id")) 
        #elif if u want to add a rule for password
        return render_template("view.html") 
    return render_template("login.html")

@app.route("/insert", methods=["POST","GET"] )
def insert():
    print(request.method)
    
    if request.method == "POST":
        id= session.get("user_id")
        name= request.form.get("medname") 
        print(request.method)
        print(name)
        if not name:
            return render_template("error.html", message="missing name")
        img=request.form.get("photo")#img I have got a prob can t put an img
        time=request.form.get("time")
        if not time:#I should creat that thing to only do mornning night
            return render_template("error.html", message="function not allowed")
        notes=request.form.get("notes", "there s no notes")
        rest= request.form.get("rest")
        medine_data = {
            "id": id,
            "med_name": name,
            "img": img,
            "time": time,
            "notes": notes,
            "rest": rest
        }
        insert_med = user_collection.insert_one(medine_data)

        #elif if u want to add a rule for password
        return render_template("index.html")
    return render_template("insert.html")
@app.route("/update", methods=["POST","GET"] )
def update():
    print(request.method)
    
    if request.method == "POST":
        id= session.get("user_id")
        print(id)
        name= request.form.get("medname") 
        print(name)
        
        print(request.method)

        if not name:
            return render_template("error.html", message="name not found")
        update_result= users_collection.find_one({ "id": ObjectId(id), "name": name}) #it give me null
        print(update_result)
        if not update_result:
            return render_template("error.html", message="user not found")
        updated_data = {"$set": {"name": name}} 
        img=request.form.get("photo")
        if not img:
            updated_data = {"$set": {"img": img}}
            update_result = users_collection.update_one({"id": id, "name": name}, updated_data) 

        
        
        time=request.form.get("time")
        if not time:
            updated_data = {"$set": {"time": time}}
            update_result = users_collection.update_one({"id": id, "name": name }, updated_data) 
        notes=request.form.get("notes")
        if not notes:
            updated_data = {"$set": {"notes": notes}}
            update_result = users_collection.update_one({"id": id, "username": name}, updated_data) 
        rest= request.form.get("rest")
        if not rest:
            updated_data = {"$set": {"rest": rest}}
            update_result = users_collection.update_one({"id": id, "username": name}, updated_data)
        return redirect("/")
        
    return render_template("update.html")
            
if __name__ == '__main__':
    app.run(debug=True)