from flask import Flask, request, jsonify
import os
import sqlite3

from facenet_model import compare_faces
from enhance_gan import enhance_image
from age_gan import age_progression
from database import init_db

app = Flask(__name__)

init_db()

@app.route("/register_missing", methods=["POST"])
def register_missing():

    name = request.form["name"]
    location = request.form["location"]
    email = request.form["email"]

    image = request.files["image"]

    path = "uploads/missing/" + image.filename
    image.save(path)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO missing(name,location,email,image) VALUES (?,?,?,?)",
        (name, location, email, path)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Child registered"})
    

@app.route("/find_child", methods=["POST"])
def find_child():

    image = request.files["image"]

    path = "uploads/found/" + image.filename
    image.save(path)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM missing")

    rows = c.fetchall()

    for r in rows:

        id,name,loc,email,img = r

        if compare_faces(path, img):

            c.execute("DELETE FROM missing WHERE id=?", (id,))
            conn.commit()

            return jsonify({"result":"MATCH FOUND","name":name})

    # no match → age progression

    aged = age_progression(path)

    for r in rows:

        id,name,loc,email,img = r

        if compare_faces(aged, img):

            c.execute("DELETE FROM missing WHERE id=?", (id,))
            conn.commit()

            return jsonify({"result":"MATCH AFTER AGE PROGRESSION"})

    return jsonify({"result":"NOT FOUND"})


if __name__ == "__main__":
    app.run(debug=True)