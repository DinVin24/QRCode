# https://developers.redhat.com/articles/2023/08/17/how-deploy-flask-application-python-gunicorn#the_application
import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
bind = os.environ.get('GUNICORN_BIND', '127.0.0.1:8080')
