from flask import Flask, render_template,request, redirect
from flask_mysqldb import MySQL
from db import registerUser,loginUser
from flask import session
import wykresy as w


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
    plot_pol, plot_woj = w.create_plot_zalesienie()
    return render_template("zalesienie.html", plot_pol=plot_pol, plot_woj=plot_woj)

@app.route("/stany-lasow")
def stany():
    plot_pol = w.create_plot_sadzenie_pol()
    plot_woj = w.create_plot_sadzenie_woj()
    return render_template("stany.html", plot_pol=plot_pol, plot_woj=plot_woj)

@app.route("/pozary")
def pozary():
    plot_pol = w.create_plot_pozary_polska()
    plot_woj = w.create_plot_pozary_woj()
    return render_template("pozary.html", plot_pol=plot_pol, plot_woj=plot_woj)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")