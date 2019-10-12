# College-ERP
A college management system built using Django framework. It is designed for interactions between students and teachers. Features include attendance, marks and time table.

## Installation

Python and Django need to be installed

```bash
pip install django
```

## Usage

Go to the College-ERP folder and run

```bash
python manage.py runserver
```

Then go to the browser and enter the url **http://127.0.0.1:8000/**


## Login

The login page is common for students and teachers.
The username is their name and password for everyone is 'project123'.
Example usernames:
student- 'anna'
teacher- 'trisila'

You can access the django admin page at **http://127.0.0.1:8000/admin** and login with username 'admin' and the above password.

Also a new admin user can be created using

```bash
python manage.py createsuperuser
```

## Users

New students and teachers can be added through the admin page. A new user needs to be created for each. 

The admin page is used to modify all tables such as Students, Teachers, Departments, Courses, Classes etc.

