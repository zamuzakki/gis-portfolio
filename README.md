## Simple GIS Portfolio App"

> **NOTE**: This open source project is built using [DjangoX](https://github.com/wsvincent/djangox) as template.

## Demo

![Demo Video](https://github.com/zamuzakki/gis-portfolio/blob/master/demo.gif)

## Features

* [x] Django 2.2 & Python 3.6
* [x] Custom user model
* [x] Email/password for user registration and log in
* [x] Static files properly configured, including Favicon
* [x] User Profile auto-create, view, and edit
* [x] Leaflet Map to locate user Profile
* [x] [django-allauth](https://github.com/pennersr/django-allauth) for authentication
* [x] [Bootstrap](https://github.com/twbs/bootstrap) for UI
* [x] [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar) for debugging
* [x] [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) for DRY forms
* [x] [django-leaflet](https://github.com/makinacorpus/django-leaflet) for displaying Leaflet map
* [x] [dj-database-url](https://github.com/jacobian/dj-database-url) for easy database settings
* [x] [python-decouple](https://github.com/henriquebastos/python-decouple) for settings separation from code
* [x] [Leaflet.fullscreen](https://github.com/Leaflet/Leaflet.fullscreen) for showing fullscreen Leaflet map
* [x] [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) for grouping Leaflet marker


## First-time setup

1.  Make sure Python 3.6x, Pip, and Virtualenv are already installed. 
See [here](https://robbinespu.gitlab.io/blog/2019/07/23/Python-36-with-VirtualEnv/) and [here](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) for help.

2.  Clone the repo and configure the virtual environment:

```
$ git clone https://github.com/zamuzakki/gis-portfolio.git
$ cd gis-portfolio
$ virtualenv --python=/usr/bin/python3.6 venv
$ source /venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

3. Make sure Spatialite or PostGIS (and PostgreSQL) is already installed. You can also use Kartoza PostGIS
docker. [See here for help](https://hub.docker.com/r/kartoza/postgis/)

4. Configure environment variables using `.env` file. Check `.env_example`
[here](https://github.com/zamuzakki/gis-portfolio/blob/dev/.env_example).

5.  Set up the initial migration for our custom user models in `users` and migrate the database.

```
(venv) $ python manage.py makemigrations users
(venv) $ python manage.py migrate
```

6.  Create a superuser:

```
(venv) $ python manage.py createsuperuser
```

7.  Confirm everything is working:

```
(venv) $ python manage.py runserver
```

Load the site at [http://localhost:8000](http://localhost:8000).

8. Create some Expertise object to be used in Profile via admin page


## Additional Notes

- This app uses `django.core.mail.backends.console.EmailBackend` by default, so instead of being sent,
the email is printed on the console. You can update [EMAIL_BACKEND](https://docs.djangoproject.com/en/3.0/topics/email/#module-django.core.mail) 
to configure an SMTP backend
- User created from signup will have `is_staff` field set to `True`, so they can login to admin page only to edit
their own Profile.