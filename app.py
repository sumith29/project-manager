from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os
from datetime import datetime

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

        if user and bcrypt.check_password_hash(
            user["password"],
            password
        ):

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

        # Check if email already exists
        existing_user = users.find_one({
            "email": email
        })

        if existing_user:
            return "Email already registered"

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

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
        due_date = request.form["due_date"]

        tasks.insert_one({
            "title": title,
            "description": description,
            "assigned_to": assigned_to,
            "status": status,
            "due_date": due_date
        })

    all_tasks = list(tasks.find())

    today = datetime.today().date()

    for task in all_tasks:

        task["overdue"] = False

        if task.get("due_date"):

            due_date = datetime.strptime(
                task["due_date"],
                "%Y-%m-%d"
            ).date()

            if (
                due_date < today and
                task["status"] != "Completed"
            ):

                task["overdue"] = True

    return render_template(
        "tasks.html",
        tasks=all_tasks
    )

# REST API - GET ALL USERS
@app.route("/api/users", methods=["GET"])
def get_users():

    all_users = list(
        users.find(
            {},
            {
                "_id": 0,
                "password": 0
            }
        )
    )

    return jsonify(all_users)


# REST API - GET ALL PROJECTS
@app.route("/api/projects", methods=["GET"])
def get_projects():

    all_projects = list(
        projects.find(
            {},
            {
                "_id": 0
            }
        )
    )

    return jsonify(all_projects)


# REST API - GET ALL TASKS
@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    all_tasks = list(
        tasks.find(
            {},
            {
                "_id": 0
            }
        )
    )

    return jsonify(all_tasks)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )