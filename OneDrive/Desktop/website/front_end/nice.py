from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home_page.html")

@app.route("/login", methods=["POST","GET"] )
def login():
    print(request.method)
    if request.method == "GET":
        print("2")
        return render_template("login.html")
    print(request.method)
    print("1")
    username = request.form.get("username")
    print(username)
    if not username:
        return render_template("error.html", message="missing name")
    password = request.form.get("password")
    if not password:
        return render_template("error.html", message="missing password")
    
    return render_template("login.html", name=username, password=password)
    
@app.route("/register", methods=["POST","GET"] )
def index():
    print(request.method)
    if request.method == "GET":
        print("3")
        return render_template("register.html")
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
    print
    if not username:
        return render_template("error.html", message="missing name")
    password=request.form.get("password")
    if not password:
        return render_template("error.html", message="missing password")
    if len(password) < 8:
        return render_template("error.html", message="password too short")
    #elif if u want to add a rule for password
    return render_template("register.html", name=username, mail=mail, password=password) 
@app.route("/insert")  
def insert():
    print(request.method)
    if request.method == "git":
        print("10")
        return render_template("insert.html")
    print(request.method)
    med_name=request.args.get("med_name")
    if not med_name:
        return render_template("error.html", message="missing med_name")
    if not med_name.isalpha():
        return render_template("error.html", message="med_name should be letters only")

    return render_template("insert.html")
@app.route("/delet", methods=["POST","GET"])
def delet():
    return render_template("delet.html")
@app.route("/view", methods=["POST","GET"])
def view():
    return render_template("view.html")
@app.route("/update", methods=["POST","GET"])
def update():
    return render_template("update.html")
if __name__ == '__main__':
    #debug=True # Enable debug mode
    app.run(debug=True)


