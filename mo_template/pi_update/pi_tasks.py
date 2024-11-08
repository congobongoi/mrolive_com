import os
os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "mo_template.settings"
#from polls.models import WOStatus,StatusSelection
from celery import Celery,task
from datetime import datetime
import sys
sys.path.append(os.path.realpath(''))
import importlib
connector = importlib.import_module('connector')
from connector import cx_Oracle
import logging
logger = logging.getLogger(__name__)
#Rabbit - celery = Celery('tasks', broker='amqp://localhost')
#celery = Celery('tasks', broker='amqp://localhost', backend="celery.backends.amqp:AMQPBackend")
celery = Celery('pi_tasks', broker='redis://localhost:6379/0', backend="rpc://")
celery.conf.update(accept_content = ['json','pickle'],accept_results = ['json','pickle'],broker_heartbeat = 15,acks_late=True)