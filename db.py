from flask import Flask,render_template, request
from flask_mysqldb import MySQL

 

def registerUser(login,password,mysql):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username=%s',(login,))
    existing_login=cursor.fetchone()
    if existing_login:
        cursor.close()
        return False
    else:
        cursor.execute(''' INSERT INTO users (username,password) VALUES(%s,%s)''',(login,password))
        mysql.connection.commit()
        cursor.close()
        return True
def loginUser(login,password,mysql):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s',(login,password))
    existing_user=cursor.fetchone()
    if existing_user:
        cursor.close()
        return True
    else:
        cursor.close()
        return False
    