from threading import Thread
from typing import Callable, List, Optional
from flask import request

from src.config import app
from src.service_container.report import ServiceReport

services = {}


class ServiceContainer:
    def __init__(self, service: Callable):
        self.service = service
        self.is_running = False
        self.reports: List[ServiceReport] = []
        self.current_run_report: Optional[ServiceReport] = None

        def callback():
            return self.flask_request_handler()

        callback.__name__ = self.service.__name__

        methods = ['POST', 'GET', 'PUT', 'DELETE']
        endpoint = '/' + self.service.__name__.replace('_', '-')

        app.route(endpoint, methods=methods)(callback)

    def wrapper(self, params):
        report = ServiceReport()
        self.current_run_report = report
        try:
            result = self.service(**params)
            report.complete(result)
        except Exception as e:
            report.fail(e)
            raise

        self.is_running = False
        self.current_run_report = None
        self.reports.append(report)

    def run(self, params):
        self.is_running = True
        thread = Thread(target=self.wrapper, args=(params,))
        thread.start()

    def current_state(self):
        return {
            'is_running': False,
            'current_run_report': self.current_run_report.current_state() if self.current_run_report else None,
            'reports': [report.current_state() for report in self.reports]
        }

    def flask_request_handler(self):
        params = request.json if request.is_json else {}

        if request.method == 'POST':
            if not self.is_running:
                self.run(params)
                return {'status': 'Started Successfully'}
            else:
                return self.current_run_report.current_state() if self.current_run_report else None

        if request.method == 'GET':
            return self.current_state()
