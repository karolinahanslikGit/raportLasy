from flask import Flask, render_template,request, redirect
from flask_mysqldb import MySQL
from db import registerUser,loginUser

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gusApp'
mysql=MySQL(app)
@app.route("/",methods=['POST', 'GET'])
def hello_world():
    if request.method=="POST":
        login=request.form["login"]
        password=request.form["password"]
        action=request.form.get("action")
        if action=="register":
            if registerUser(login,password,mysql):
                
                return redirect("/main")
            else:
                 return render_template("index.html", message="Taki użytkownik już istnieje")
        elif action=="login":
            if loginUser(login,password,mysql):
                
                return redirect("/main")
            else:
                 return render_template("index.html", message="Nieprawidłowa nazwa użytkownika lub hasło")
        
        return redirect("/")
    return render_template('index.html')
@app.route("/main")
def raport():
    return render_template("main.html")