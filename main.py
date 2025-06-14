from flask import Flask, render_template,request, redirect
from flask_mysqldb import MySQL
from db import registerUser,loginUser
from flask import session


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gusApp'
mysql=MySQL(app)

app.secret_key = "klucz_sesji"

@app.route("/",methods=['POST', 'GET'])
def hello_world():
    if request.method=="POST":
        login=request.form["login"]
        password=request.form["password"]
        action=request.form.get("action")
        if action=="register":
            if registerUser(login,password,mysql):
                session['username'] = login
                return redirect("/zalesienie")
            else:
                 return render_template("index.html", message="Taki użytkownik już istnieje")
        elif action=="login":
            if loginUser(login,password,mysql):
                session['username'] = login
                return redirect("/zalesienie")
            else:
                 return render_template("index.html", message="Nieprawidłowa nazwa użytkownika lub hasło")
        
        return redirect("/")
    return render_template('index.html')

@app.route("/main")
def main_dashboard():
    return redirect("/zalesienie")

@app.route("/zalesienie")
def zalesienie():
    return render_template("zalesienie.html")

@app.route("/stany-lasow")
def stany():
    return render_template("stany.html")

@app.route("/pozary")
def pozary():
    return render_template("pozary.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")