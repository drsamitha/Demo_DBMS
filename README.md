# Database Management System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/django-4.0%2B-green)

A powerful, intuitive web interface for managing database connections, executing ORM queries, and visualizing data with ease.

##  Screenshots

| Screenshot 1 | Screenshot 2 |
|--------------|--------------|
| ![n1](https://github.com/smtkanchana66/Demo_DBMS/raw/main/Readme_res/n1.png) | ![n2](https://github.com/smtkanchana66/Demo_DBMS/raw/main/Readme_res/n2.png) |

| Screenshot 3 | Screenshot 4 |
|--------------|--------------|
| ![n3](https://github.com/smtkanchana66/Demo_DBMS/raw/main/Readme_res/n3.png) | ![n4](https://github.com/smtkanchana66/Demo_DBMS/raw/main/Readme_res/n4.png) |
<!-- ![Database Management System Screenshot](/screenshots/dashboard.png) -->

## Features

- **Data Visualization**: Create charts and graphs from your database data
- **Migration Management**: Run and track database migrations
- **Security & Access Controls**: Manage permissions and track access logs

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation
#### For Linux:-
1. Clone the repository:
   ```bash
   git clone https://github.com/drsamitha/Demo_DBMS.git
   cd Demo_DBMS
   ```
   
2. Create and setup virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
   
3. Install dependencies from requirements file:
   ```bash
   pip install -r requrements.txt
   ```
   
4. Run the application:
   ```bash
    python3 ./manage.py makemigrations # (if change data base. must run this code 1)
    python3 ./manage.py migrate # (if change data base. must run this code 2)
    python3 ./manage.py runserver
   ```
5. Access the application at:
   ```
   http://localhost:8000/
   ```
   
#### For Windows:-
1. Clone the repository:
   ```bash
   git clone https://github.com/drsamitha/Demo_DBMS.git
   cd .\Demo_DBMS\
   ```
   
2. Set Up a Virtual Environment: 
   ```bash
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\venv\Scripts\activate
   ```
   
3. Install dependencies from requirements file:
   ```bash
   pip3 install -r .\requirements.txt
   ```

4. Run the application:
   ```bash
    python .\manage.py makemigrations (if change data base. must run this code 1)
    python .\manage.py migrate (if change data base. must run this code 2)
    python .\manage.py runserver
   ```

5. Access the application at:
   ```
   http://localhost:8000/
   ```
