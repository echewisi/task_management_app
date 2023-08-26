# Task Management App



Task Management App is a web application built using Django that allows users to manage their tasks. Users can create, update, delete, and view tasks. The app also sends email notifications for task reminders and deletions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Create, update, delete, and view tasks
- Task completion tracking
- Email notifications for reminders and deletions

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/echewisi/task_management_app.git
   
2. navigate to project directory:
  cd task_management_app

3. install required dependencies;
     pip install -r requirements.txt
   
4.  Set up your database and configure your email settings in settings.py.

5.  apply migrations:
    python manage.py makemigrations
     python manage.py migrate
    
6. run server:
    python manage.py runserver


## USAGE
Access the application by navigating to http://localhost:8000 in your web browser.
-Register or log in using your credentials.
-Create, update, delete, and view your tasks.
-Receive email notifications for reminders and deletions.

## CONTRIBUTING
Fork the repository.
-Create a new branch: git checkout -b feature/your-feature-name.
-Make your changes and commit them: git commit -m 'Add some feature'.
-Push to the branch: git push origin feature/your-feature-name.
-Open a pull request.

## LICENSE
This project is licensed under the MIT License.

## SUBNOTE
## API ENDPOINT:
POST /api/register/: User registration.
POST /api/login/: User login.
POST /api/logout/: User logout.
GET /api/tasks/: List tasks and create a new task.
GET /api/tasks/<task_id>/: Retrieve, update, or delete a task.
   
    
