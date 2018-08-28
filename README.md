
# tool

## Introduction
 This project is aimed to build a network of tools. The tools vary from simple document conversion tools to real time advice tools. Users will be able to add new tools and interact socially with each other.

## Requirements

Python 3 and django 1.11

## Installation

### Setup the virtual environment
```
 virtualenv venv
 cd venv
 source bin/activate
```

### Clone the project
```
git clone  https://github.com/OpenGenus/tool.git
cd tool
pip install -r requirements.txt
```



### Install other dependencies
- #### Installing pandoc on Ubuntu
	- Install LaTeX: `sudo apt-get install texlive-full`
	- Install pandoc:  `sudo apt-get install pandoc`





## Running on localhost

In `settings.py` change DEBUG to True.
Before running the app make sure to migrate and run collectstatic
```
python manage.py makemigrations
python manage.py makemigrations mainapp
python manage.py migrate

python manage.py collectstatic

```
now run using `python manage.py runserver`

## Extra Requirements For some Tools

- #### Installing wkhtmltopdf on windows
	- by default the project contained a folder named wkhtmltopdf it will work without installations
	
- #### Installing wkhtmltopdf on linux
	- you could download a version  from  here `https://wkhtmltopdf.org/downloads.html`
	 after that replace the folder wkhtmltopdf with your wkhtmltopdf folder you need to have an executable file inside the bin folder 
	 so take care 
   
## Getting A Tool Running
This is a general overview of getting a tool running
1. If there is no admin user, create one using `python manage.py createsuperuser`
2. Start the development server using `python manage.py runserver`
3. Go to http://127.0.0.1:8000/admin and log in with the superuser credentials
4. Add a new user to the database from the admin panel
5. To get a new tool up and running, add its details to the database using the add tool option.
6. The details of the tool can be found in the `tools_data.csv` file. Details like the description can be left blank.
7. Once the tool is saved, it can be accessed from http://127.0.0.1:8000/