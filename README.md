# API - SoftDesk
An API to report issues on SoftDesk app


## Installation


### Clone this repository
``` 
git clone https://github.com/rhunold/projet10.git
```

### Create an environment at the root of the project
``` 
python3 -m venv env
```

### Activate the environment
``` 
python3 source env/bin/activate
```

### Install pip
``` 
python3 -m pip install 
```

### Install the requirements
``` 
pip install -r requirements.txt
```

## Database
You can use the database or create a new one (delete the db.sqlite3 file in the softdesk folder befor)

### Using the actual database

You can log after you run the server (see next 'Run server' instructions below.)
#### Access of the actual database
| typeUser | email | password | user_id 
|-|-|-|
| SuperUser | raphael.hunold@gmail.com | Héà2flzizl! | 1
| User | toto@gmail.com | tatatiti | 2
| User | max@gmail.com | maxpass8 | 3
| User | tom@gmail.com | tompass8 | 4

### Create a new database
To create the database, use theses line commands

#### Make migrations
```
python3 manage.py makemigrations api
```

#### Migrate
```
python3 manage.py migrate
```

Database is created.

You can create a superuser
```
python3 manage.py createsuperuser
```

## Run server

After environment is launch, use this command line to start the server
```
python3  manage.py runserver
```

Server adress : [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Actions and permissions

| Action | Permission |
|-|-|
| Signup | Everyone |
| Login | Everyone who had signup |
| Create a project | Every logged user |
| Add and remove contributors of a project | Project creator |
| Create issues and comments | Project contributor/creator |
| List and read issues | Project contributor/creator |
| List and read comments | Project contributor/creator |
| Modify or delete project, issue and comment | Project/Issue/Comment creator |
| All actions on all objects | Superuser |

## API documentation 
[https://documenter.getpostman.com/view/25526925/2s8ZDeSy1a](https://documenter.getpostman.com/view/25526925/2s8ZDeSy1a)

API documentation : 

## Other things about this project
This project use the module flake8 to respect pep8 guideline.
To test it by yourself, go to the root of the project and use this command line to generate a html file in the flake8 folder.
```
python3  flake8 --format=html --htmldir=flake8
```


