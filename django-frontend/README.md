# DJANGO FRONTEND
## Description
This is a Django instance for manage the frontend of the project.
## Dependencies
- [Django](https://www.djangoproject.com/)

## Project setup before docker
### 0. Ressouces
- [Django Documentation](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
### 1. Create a virtual environment
```bash
python3.12 -m venv .venv    # Create a virtual environment
source .venv/bin/activate   # Activate the virtual environment
```
### 2. Install the dependencies
```bash
pip install django
```
### 3. Freeze the dependencies
```bash
pip freeze > requirements.txt
```
### 4. Create the Django project
```bash
django-admin startproject app
```
