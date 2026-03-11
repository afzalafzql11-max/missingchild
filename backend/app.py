from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)
app.secret_key = "secret"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DATABASE
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image TEXT)""")

    conn.commit()
    conn.close()

init_db()


# SIMPLE DEHAZE FUNCTION
def dehaze_image(path):

    img = cv2.imread(path)

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0,tileGridSize=(8,8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl,a,b))
    final = cv2.cvtColor(limg,cv2.COLOR_LAB2BGR)

    new_path = path.replace("uploads","uploads/dehazed")
    os.makedirs("uploads/dehazed",exist_ok=True)

    cv2.imwrite(new_path,final)

    return new_path


# HOME
@app.route("/")
def home():
    return redirect("/login")


# SIGNUP
@app.route("/signup",methods=["GET","POST"])
def signup():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        c=conn.cursor()

        c.execute("INSERT INTO users(email,password) VALUES (?,?)",(email,password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# LOGIN
@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        c=conn.cursor()

        user=c.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password)).fetchone()

        conn.close()

        if user:
            session["user"]=user[0]
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard",methods=["GET","POST"])
def dashboard():

    if "user" not in session:
        return redirect("/login")

    if request.method=="POST":

        file=request.files["image"]

        path=os.path.join(UPLOAD_FOLDER,file.filename)
        file.save(path)

        new_path=dehaze_image(path)

        conn=sqlite3.connect("database.db")
        c=conn.cursor()

        c.execute("INSERT INTO history(user_id,image) VALUES (?,?)",(session["user"],new_path))
        conn.commit()
        conn.close()

        return send_file(new_path,as_attachment=True)

    return render_template("dashboard.html")


# HISTORY
@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    conn=sqlite3.connect("database.db")
    c=conn.cursor()

    data=c.execute("SELECT image FROM history WHERE user_id=?",(session["user"],)).fetchall()
    conn.close()

    return render_template("history.html",data=data)


# DOWNLOAD
@app.route("/download/<path:img>")
def download(img):

    return send_file(img,as_attachment=True)


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run()
