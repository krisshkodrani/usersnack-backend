# UserSnack Django REST Backend

## Setup

Create and activate a virtual environment (Python3) using your preferred method. This functionality is [built into](https://docs.python.org/3/tutorial/venv.html) Python, if you do not have a preference.

From the command line, type:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open your browser to http://localhost:8000 and you should see the browsable version of the API.

## Test

To run all tests

```
python manage.py test
```