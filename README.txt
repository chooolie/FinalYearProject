python manage.py runserver 
RUN THE DEVELOPMENT SERVE
python manage.py shell
RUN THE SHELL 
python manage.py makemigrations
MAKE MIGRATIONS
python manage.py migrate
MIGRATE
python manage.py check --deploy 
CHECK FOR ANY SECURITY ISSUES


SET DJANGO_SETTINGS_MODULE=tutorial.settings.dev
to set the new settings path before running the development server
OR 
python manage.py runserver --settings=tutorial.settings.dev