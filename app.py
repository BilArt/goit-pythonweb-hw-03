from flask import Flask, render_template, request
import os
import json
from datetime import datetime

app = Flask(__name__)

STORAGE_PATH = "storage/data.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")
        timestamp = datetime.now().isoformat()

        os.makedirs("storage", exist_ok=True)

        if not os.path.exists(STORAGE_PATH):
            with open(STORAGE_PATH, "w") as file:
                json.dump({}, file)

        with open(STORAGE_PATH, "r+") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
            data[timestamp] = {"username": username, "message": message}
            file.seek(0)
            json.dump(data, file, indent=4)

    return render_template("message.html")

@app.route("/read")
def read():
    os.makedirs("storage", exist_ok=True)
    if not os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "w") as file:
            json.dump({}, file)

    with open(STORAGE_PATH, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    return render_template("read.html", messages=data)

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html"), 404

if __name__ == "__main__":
    app.run(port=3000, debug=True)
