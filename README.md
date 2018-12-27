# Flask Server Template
This is a Flask Server Template possible to working for API Server or Backend Server.
Working with Flask-RestPlus, Flask-JWT, Flask-Marshmallow, Celery, and also ready to deploy with Dockerfile available. This Flask Server running with gunicorn in port 8080.

## Structure Directory

### Main Directory (Top-level)
    .
    ├── project                 # Project Directory          
    ├── Dockerfile              # Dockerfile
    ├── .gitignore
    ├── LICENSE
    └── README.md

### Project Directory
    .
    ├── project                           
    │     ├── server                # Server Directory
    │     ├── config.py             # Config File
    │     ├── Makefile
    │     ├── manage.py             # Manage File for Development Purposes
    │     ├── requirements.txt      # Dependency lib
    │     ├── server.run.sh         # Script for running server
    │     └── worker.run.sh         # Script for running celery/worker
    │
    └── ...

### Server Directory
    .
    ├── project                           
    │     ├── server                
    │     │      ├── extensions        # Extensions Directory
    │     │      ├── main              # Main Directory (Modules, etc)
    │     │      ├── tests             # Test Directory (Unittest)
    │     │      ├── __init__.py       # Entrypoint file
    │     │      ├── app.py            # Flask App in Factory Pattern
    │     │      ├── worker.py         # Celery Entrypoint
    │     │      └── wsgi.py           # WSGIApp Entrypoint
    │     │
    │     └── ...
    └── ...

### Soon Update ...

### Usage (Development)
* Go over in `/project` - Project Directory
* `pip install -r requirements.txt` - Installing Dependency
* `python manage.py recreatedb` - Setup Local Database (make sure change your database default database will using sqlite.db)
* `python manage.py run` - Running Flask Server in `http://localhost:5000/api/v1/`

### Usage (Production)
* Go over in root directory
* `docker build -t ardikabs/flask-server-template . ` - Create Flask Server Template Image
* `docker run -d -p 8080:8080 --name flask-server ardikabs/flask-server-template` - Running Flask Server Template Container
