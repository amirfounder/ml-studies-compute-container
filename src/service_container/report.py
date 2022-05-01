from datetime import datetime


class ServiceReport:
    def __init__(self):
        self.status = 'RUNNING'
        self.start = datetime.now()
        self.end = None
        self.elapsed = None
        self.service_report = None
        self.exception = None

    def complete(self, service_report):
        self.status = 'SUCCESS'
        self.service_report = service_report
        self.end = datetime.now()
        self.elapsed = str(self.end - self.start)

    def fail(self, e):
        self.status = 'FAIL'
        self.exception = str(e)
        self.end = datetime.now()
        self.elapsed = str(self.end - self.start)

    def current_state(self):
        return {
            'status': self.status,
            'start': self.start.isoformat(),
            'end': self.end,
            'elapsed': self.elapsed or str(datetime.now() - self.start),
            'service_report': self.service_report,
            'exception': self.exception
        }