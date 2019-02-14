from tutorial.settings.base import *
#later can override base settings here if needed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
try:
    from tutorial.settings.local import *
except:
    pass
