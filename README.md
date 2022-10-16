# bazar-brecho
A second hand clothing marketplace

# Development

## Create or Update you virtual environment
This projet encourage the use of a virtual environment to ensure that everthing
will work properly. You will find a ´requiriment.txt´ and also a ´environment.yml´ 
which can be used to create/update your enviroment.

### Using Conda
Type the following commands at your shell to create/update using conda.

Create: 
´conda env create -f environment.yml´

Update:
´conda env update -f environment.yml´

After that, you can activate your conda environment using ´conda activate bazarbrecho´

### Using venv
Type the following commands at your shell to create/update using venv.

At directory where you want to have your environment.
Create:
Unix/MacOS: ´python3 -m venv env´ Win: ´py -m venv env´

Activate env:
Unix/MacOS: ´source env/bin/activate´ Win: ´.\env\Scripts\activate´

Update/Intalling packages:
Unix/MacOS: ´python3 -m pip install -r requirements.txt´ Win: ´py -m pip install -r requirements.txt´

## Installing githock
This Project has some usefull pre-commit at ´.pre-commit-config.yaml´. To have access to those hooks and use pre-commit in your local envirament you only need to go the source directory with your virtual environment active and run the following command: 

´pre-commit install´

After that, pre-commit will run the following usefull tools before each of your commits:

1. black (ensure a commum format)
2. isort (sort imports)

# Back-End development
Django-based back-end development details

## Configuring and testing the webserver

Inside the virtualenv:
1. Go to webserver/bazarbrecho
2. Run 'python manage.py makemigrations'
3. Run 'python manage.py migrate'
4. Run 'python manage.py runserver'


## Videos and tutorials:

The Net Ninja:
https://www.youtube.com/watch?v=n-FTlQ7Djqc&list=PL4cUxeGkcC9ib4HsrXEYpQnTOTZE1x0uc

Free Code Camp:
https://www.youtube.com/watch?v=F5mRW0jo-U4

Django best practices:
https://django-best-practices.readthedocs.io/en/latest/index.html

TO-DO item list (handling databases):
https://www.youtube.com/watch?v=ovql0Ui3n_I
