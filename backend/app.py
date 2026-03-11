from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
import cv2
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- DEHAZE FUNCTION ----------------

def dehaze_image(path):

    img = cv2.imread(path)

    # simple haze removal
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0)
    cl = clahe.apply(l)

    merged = cv2.merge((cl,a,b))
    result = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    new_path = path.replace(".jpg","_clear.jpg")
    cv2.imwrite(new_path,result)

    return new_path

# ---------------- SIGNUP ----------------

@app.route("/signup",methods=["POST"])
def signup():

    data = request.json
    user = data["username"]
    password = data["password"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("INSERT INTO users(username,password) VALUES (?,?)",(user,password))

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})

# ---------------- LOGIN ----------------

@app.route("/login",methods=["POST"])
def login():

    data = request.json
    user = data["username"]
    password = data["password"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",(user,password))
    result = c.fetchone()

    conn.close()

    if result:
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"fail"})

# ---------------- UPLOAD IMAGE ----------------

@app.route("/upload",methods=["POST"])
def upload():

    user = request.form["username"]
    file = request.files["image"]

    filename = str(uuid.uuid4())+".jpg"
    path = os.path.join(UPLOAD_FOLDER,filename)

    file.save(path)

    clear_path = dehaze_image(path)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("INSERT INTO history(username,image) VALUES (?,?)",(user,clear_path))

    conn.commit()
    conn.close()

    return send_file(clear_path,mimetype="image/jpeg")

# ---------------- HISTORY ----------------

@app.route("/history/<username>")
def history(username):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT image FROM history WHERE username=?",(username,))
    data = c.fetchall()

    conn.close()

    images = [x[0] for x in data]

    return jsonify(images)

# ---------------- DOWNLOAD ----------------

@app.route("/download")
def download():

    path = request.args.get("path")
    return send_file(path,mimetype="image/jpeg")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run()
