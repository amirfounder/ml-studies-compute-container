from datetime import datetime
from threading import Thread
from typing import Callable
from flask import request

from src.config import app

services = {}

def register(func: Callable):
    n = func.__name__

    service_data = {
        'caller': None,
        'is_running': False,
        'all_runs': [],
        'latest_run': {}
    }
    
    endpoint = '/' + n.replace('_', '-')
    methods = ['POST', 'GET', 'PUT', 'DELETE']

    def service_wrapper(*args, **kwargs):
        start = datetime.now()
        latest_run = {
            'status': 'running',
            'start': start,
            'end': None,
            'elapsed': '0',
            '_elapsed': 0,
            'result': None
        }

        service_data['latest_run'].update(latest_run)
        service_data['all_runs'].append(latest_run)

        result = func(*args, **kwargs)
        end = datetime.now()
        service_data['is_running'] = False

        latest_run = {
            'status': 'done',
            'start': start,
            'result': result,
            'end': end,
            'elapsed': str(end - start),
            '_elapsed': (end - start).total_seconds()
        }

        service_data['latest_run'].update(latest_run)
        service_data['all_runs'][-1].update(latest_run)

    def thread_wrapper(*args, **kwargs):
        t = Thread(target=service_wrapper, args=args, kwargs=kwargs)
        t.start()

    service_data['caller'] = thread_wrapper

    def flask_callback(*args, **kwargs):

        if request.method == 'POST':
            if not service_data['is_running']:
                service_data['is_running'] = True
                service_data['caller'](*args, **kwargs)

                return {
                    'status': 'Task started',
                }
            else:
                return service_data['latest_run']

        if request.method == 'GET':
            return_value = {}
            for k, v in service_data.items():
                if k != 'caller':
                    return_value[k] = v
            return return_value

    flask_callback.__name__ = n

    services[n] = service_data

    app.route(endpoint, methods=methods)(flask_callback)
