Project Manager Web App

A full-stack Project Management Web Application built using Flask and MongoDB with role-based access control

Features

- User Authentication (Signup/Login)
- Role-Based Access (Admin / Member)
- Project Creation & Management
- Task Creation & Assignment
- Task Status Tracking
- Dashboard Interface
- MongoDB Database Integration
- Railway Deployment

Tech Stack

- Python
- Flask
- MongoDB
- Bootstrap
- Railway
- GitHub

Project Structure

Project-manager
│
├── app.py
├── requirements.txt
├── Procfile
├── README.md
│
├── templates
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── projects.html
│   └── tasks.html


Live Deployment

https://project-manager-production-6d8c.up.railway.app


GitHub Repository
https://github.com/sumith29/project-manager
Installation & Setup

1.Clone the Repository
<bash>
git clone https://github.com/sumith29/project-manager.git

2.Navigate to Project Folder
<bash>
cd project-manager

3. Install Required Dependencies
<bash>
pip install -r requirements.txt

4. Run the Application
<bash>
python app.py

5. Open in Browser
<bash>
http://127.0.0.1:5000


Roles

Admin
- Create Projects
- Create Tasks
- Assign Tasks

Member
- View Tasks


Deployment

Application deployed using Railway with MongoDB integration.


