# Welcome to Zones

By Santi Carniglia scarniglia@gmail.com.

## Example installation on Debian 9.7

### Required packages
* `$ sudo apt-get install postgresql` - install postgresql.
* `$ sudo apt-get install postgis` - install postgis.
* `$ sudo apt-get install python3-psycopg2` - Python 3 module for PostgreSQL
* `$ sudo apt-get install python3-virtualenv` - Python 3 Virtualenv
* `$ sudo apt-get install git` - GIT

### Database configuration
* `$ sudo su - postgres` - login as postgres user
* `$ psql` - access database
* `postgres# CREATE USER geodjango PASSWORD 'my_passwd';` - create user
* `postgres# CREATE DATABASE geodjango OWNER geodjango;` - create database
* `postgres# \c geodjango;` - connect to the geodjango database.
* `postgres# CREATE EXTENSION postgis;` - create postgis extension in geodjango
* `postgres# ALTER USER geodjango WITH SUPERUSER;` - necessary to run the tests
* `postgres# \q` - exit database
* `$ exit` - exit postgres console

### Create Django project
* `$ export PYTHONPATH=/usr/lib/python3/dist-packages`
* `$ python3 -m virtualenv -p /usr/bin/python3 venv`
* `$ source venv/bin/activate`
* `$ git clone https://github.com/scarniglia/django-zones.git geodjango`
* `$ cd geodjango`
* `$ pip install -r requirements.txt`
* `$ django-admin startproject geodjango .`

add in settings.py:

    ...
    INSTALLED_APPS = [
        ...
        'zones.apps.ZonesConfig',
        'django.contrib.gis',
        'rest_framework',
        'rest_framework_gis',
    ]
    
    ...
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'geodjango',
            'USER': 'geodjango',
            'PASSWORD': 'my_passwd',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 100
    }
    ...

and add to geodjango/urls.py:

    from django.contrib import admin
    from django.urls import path
    from django.conf.urls import include
    
    urlpatterns = [
        path('api/', include('zones.urls')),
        path('admin/', admin.site.urls),
    ]

* `$ python manage.py migrate`
* `$ python manage.py test`
* `$ python manage.py runserver`

Browse to http://localhost:8000/api