from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home_user.html')
@app.route("/register", methods=["POST","GET"] )
def great():
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
        username=request.form.get("username")
        print(username)
        if not username:
            return render_template("error.html", message="missing name")
        password=request.form.get("password")
        if not password:
            return render_template("error.html", message="missing password")
        if len(password) < 8:
            return render_template("error.html", message="password too short")
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
        password=request.form.get("pass")
        if not password:
            return render_template("error.html", message="missing password")
        #elif if u want to add a rule for password
        return render_template("view.html") 
    return render_template("login.html")

@app.route("/insert", methods=["POST","GET"] )
def insert():
    print(request.method)
    if request.method == "POST":
        name= request.form.get("name") 
        print(request.method)
        print(name)
        if not name:
            return render_template("error.html", message="missing name")
        img=request.form.get("photo")
        if not img.endswith(".jpg"):
            return render_template("error.html", message="img should be .jpg")
        time=request.form.get("time")
        if not time:#I should creat that thing to only do mornning night
            return render_template("error.html", message="function not allowed")
        notes=request.form.get("notes", "there s no notes")
        #elif if u want to add a rule for password
        return render_template("index.html")
    return render_template("insert.html")

if __name__ == '__main__':
    app.run(debug=True)