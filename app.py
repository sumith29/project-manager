from flask import Flask, render_template, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

bcrypt = Bcrypt(app)

# MongoDB Connection
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(MONGO_URI)

db = client["project_manager"]

# Collections
users = db["users"]
projects = db["projects"]
tasks = db["tasks"]


# LOGIN
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({
            "email": email
        })

        if user and bcrypt.check_password_hash(user["password"], password):

            return render_template(
                "dashboard.html",
                user=user["name"],
                role=user["role"]
            )

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role
        })

        return "User Registered Successfully"

    return render_template("signup.html")


# PROJECT PAGE
@app.route("/projects", methods=["GET", "POST"])
def project_page():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        projects.insert_one({
            "title": title,
            "description": description
        })

    all_projects = list(projects.find())

    return render_template(
        "projects.html",
        projects=all_projects
    )


# TASK PAGE
@app.route("/tasks", methods=["GET", "POST"])
def task_page():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        assigned_to = request.form["assigned_to"]
        status = request.form["status"]

        tasks.insert_one({
            "title": title,
            "description": description,
            "assigned_to": assigned_to,
            "status": status
        })

    all_tasks = list(tasks.find())

    return render_template(
        "tasks.html",
        tasks=all_tasks
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )