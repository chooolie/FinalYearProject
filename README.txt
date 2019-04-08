python manage.py shell
RUN THE SHELL
python manage.py makemigrations
MAKE MIGRATIONS
python manage.py migrate
MIGRATE
python manage.py check --deploy
CHECK FOR ANY SECURITY ISSUES
python manage.py dbshell
MAKE ANY CHANGES TO THE DB

SET DJANGO_SETTINGS_MODULE=tutorial.settings.dev
to set the new settings path before running the development server
OR
To run on local machine
python manage.py runserver --settings=tutorial.settings.dev

To run on digital ocean -
python manage.py runserver 0.0.0.0:8080 --settings=tutorial.settings.dev


!!All python requirements for this project are in the requirements.txt file!!
