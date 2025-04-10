from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/", methods=["POST", "GET"] )
def login():
    print(request.method)
    if request.method == "GET":
        print("1")
        return render_template("login.html")
    username = request.form.get("username")
    if not username:
        return render_template("error.html", message="missing name")
    password = request.form.get("password")
    if not password:
        return render_template("error.html", message="missing password")
    
    return render_template("login.html", name=username, password=password)
    
@app.route("/register", methods=["POST", "GET"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")
    mail=request.args.get("mail")
    print(request.method)
    
    if not mail:
        print("5")
        return render_template("error.html", message="missing mail")
    if not mail.endswith("@gmail.com"):
        return render_template("error.html", message="missing @gmail.com")
    print("6")
    username=request.args.get("username")
    if not username:
        return render_template("error.html", message="missing name")
    password=request.args.get("password")
    if not password:
        return render_template("error.html", message="missing password")
    if len(password) < 8:
        return render_template("error.html", message="password too short")
    #elif if u want to add a rule for password
    return render_template("register.html", name=username, mail=mail, password=password) 
@app.route("/insert")  
def insert():
    
    if request.method == "POST":
        print("1")
        return render_template("insert.html")
    if request.method == "GET":
        print("2")
        return render_template("insert.html")
    print(request.method)
    med_name=request.args.get("med_name")
    if not med_name:
        return render_template("error.html", message="missing med_name")
    if not med_name.isalpha():
        return render_template("error.html", message="med_name should be letters only")

    return render_template("insert.html")
@app.route("/interface", methods=["POST","GET"])
def interface():
    return render_template("interface.html")
@app.route("/delet", methods=["POST","GET"])
def delet():
    return render_template("delet.html")
@app.route("/update", methods=["POST","GET"])
def update():
    return render_template("update.html")
if __name__ == '__main__':
    debug=True # Enable debug mode
    app.run()


